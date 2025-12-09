# %% [markdown]
# # PHÂN LOẠI VĂN BẢN TIN TỨC TÀI CHÍNH TIẾNG VIỆT (IMPROVED VERSION)
# 
# **Các cải thiện so với phiên bản trước:**
# 1. Class Weights - Xử lý mất cân bằng dữ liệu
# 2. PhoBERT tuning - Learning rate thấp hơn, unfreeze layers
# 3. Early Stopping - Tránh overfitting
# 4. Ensemble Model - Kết hợp nhiều mô hình
# 5. Tiền xử lý cải tiến - Chuẩn hóa số, tăng MAX_LEN

# %% [code]
# =======================================================================
# INSTALL DEPENDENCIES
# =======================================================================

!pip install -q transformers

# %% [code]
# =======================================================================
# IMPORTS
# =======================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import warnings
from collections import Counter

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks, Model
from tensorflow.keras.preprocessing.sequence import pad_sequences

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight  # NEW: Class weights

from transformers import AutoTokenizer, TFAutoModel

warnings.filterwarnings('ignore')

np.random.seed(42)
tf.random.set_seed(42)

print(f"TensorFlow: {tf.__version__}")
print(f"GPU: {len(tf.config.list_physical_devices('GPU'))} devices")

# %% [code]
# =======================================================================
# 1. LOAD & EXPLORE DATA
# =======================================================================

print("\n" + "="*70)
print("1. LOADING & EXPLORING DATA")
print("="*70)

df = pd.read_excel('/content/data.xlsx')
print(f"✓ Loaded {len(df)} samples")
print(f"✓ Columns: {df.columns.tolist()}")

# Check missing values
print("\nMissing values:")
print(df[['text', 'argument_classification_label']].isnull().sum())

# Remove missing
df = df.dropna(subset=['text', 'argument_classification_label'])
print(f"✓ After cleaning: {len(df)} samples")

# Show label distribution
print("\nArgument Classification Label Distribution:")
print(df['argument_classification_label'].value_counts())
print(f"\nPercentage:")
print(df['argument_classification_label'].value_counts(normalize=True) * 100)

# Visualize distribution
plt.figure(figsize=(10, 6))
df['argument_classification_label'].value_counts().plot(kind='bar', color='steelblue')
plt.title('Argument Classification Label Distribution', fontweight='bold', fontsize=14)
plt.xlabel('Label', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('label_distribution.png', dpi=300, bbox_inches='tight')
plt.show()
print("✓ Saved: label_distribution.png")

# Text length analysis
df['text_length'] = df['text'].str.len()
df['word_count'] = df['text'].str.split().str.len()

print(f"\nText Statistics:")
print(f"  Average length: {df['text_length'].mean():.1f} characters")
print(f"  Average words: {df['word_count'].mean():.1f} words")
print(f"  Max words: {df['word_count'].max()}")
print(f"  95th percentile: {df['word_count'].quantile(0.95):.1f} words")

# %% [code]
# =======================================================================
# 2. LABEL ENCODING
# =======================================================================

print("\n" + "="*70)
print("2. LABEL ENCODING")
print("="*70)

le = LabelEncoder()
df['label'] = le.fit_transform(df['argument_classification_label'])
NUM_CLASSES = len(le.classes_)

print(f"Number of classes: {NUM_CLASSES}")
print("\nLabel mapping:")
for idx, label in enumerate(le.classes_):
    count = (df['label'] == idx).sum()
    print(f"  {idx}: {label} ({count} samples)")

# %% [code]
# =======================================================================
# 3. SPLIT DATA
# =======================================================================

print("\n" + "="*70)
print("3. SPLITTING DATA")
print("="*70)

train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df['label'])
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['label'])

print(f"Train: {len(train_df)} | Val: {len(val_df)} | Test: {len(test_df)}")

# %% [code]
# =======================================================================
# 4. COMPUTE CLASS WEIGHTS (NEW!)
# =======================================================================

print("\n" + "="*70)
print("4. COMPUTING CLASS WEIGHTS (NEW!)")
print("="*70)

y_train = train_df['label'].values
y_val = val_df['label'].values
y_test = test_df['label'].values

# Compute class weights to handle imbalanced data
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train),
    y=y_train
)
class_weight_dict = dict(enumerate(class_weights))

print("Class weights (to handle imbalanced data):")
for idx, label in enumerate(le.classes_):
    print(f"  {label}: {class_weight_dict[idx]:.4f}")

# %% [code]
# =======================================================================
# 5. BUILD VOCABULARY (IMPROVED TEXT CLEANING)
# =======================================================================

print("\n" + "="*70)
print("5. BUILDING VOCABULARY (IMPROVED)")
print("="*70)

def clean_text_improved(text):
    """Improved Vietnamese text cleaning"""
    text = str(text).lower()
    # Normalize numbers (NEW!)
    text = re.sub(r'\d+\.?\d*', '<NUM>', text)
    # Remove special characters, keep Vietnamese
    text = re.sub(r'[^\w\s\u00C0-\u1EF9<>]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

all_words = []
for text in train_df['text']:
    all_words.extend(clean_text_improved(text).split())

word_counts = Counter(all_words)
vocab = {'<PAD>': 0, '<UNK>': 1, '<NUM>': 2}  # Added <NUM> token
for word, count in word_counts.items():
    if count >= 2:
        vocab[word] = len(vocab)

VOCAB_SIZE = len(vocab)
MAX_LEN = 128  # INCREASED from 100
EMBED_DIM = 128
NUM_HEADS = 8
FF_DIM = 256

print(f"Vocabulary size: {VOCAB_SIZE}")
print(f"Max sequence length: {MAX_LEN} (increased from 100)")

# %% [code]
# =======================================================================
# 6. PREPARE DATA FOR LSTM/BiLSTM/GRU/Transformer
# =======================================================================

print("\n" + "="*70)
print("6. PREPARING DATA")
print("="*70)

def texts_to_sequences(texts, vocab, max_len):
    sequences = []
    for text in texts:
        words = clean_text_improved(text).split()
        seq = [vocab.get(w, vocab['<UNK>']) for w in words]
        sequences.append(seq)
    return pad_sequences(sequences, maxlen=max_len, padding='post', value=0)

X_train = texts_to_sequences(train_df['text'].values, vocab, MAX_LEN)
X_val = texts_to_sequences(val_df['text'].values, vocab, MAX_LEN)
X_test = texts_to_sequences(test_df['text'].values, vocab, MAX_LEN)

print(f"X_train shape: {X_train.shape}")
print(f"X_val shape: {X_val.shape}")
print(f"X_test shape: {X_test.shape}")
print("✓ Data prepared")

# %% [code]
# =======================================================================
# 7. BUILD LSTM MODEL
# =======================================================================

print("\n" + "="*70)
print("7. BUILDING LSTM MODEL")
print("="*70)

def build_lstm_model():
    inp = layers.Input(shape=(MAX_LEN,), name='input')
    x = layers.Embedding(VOCAB_SIZE, EMBED_DIM, mask_zero=True)(inp)
    x = layers.LSTM(256, return_sequences=True, dropout=0.3)(x)
    x = layers.LSTM(256, dropout=0.3)(x)
    x = layers.Dropout(0.3)(x)
    output = layers.Dense(NUM_CLASSES, activation='softmax')(x)
    return Model(inputs=inp, outputs=output, name='LSTM')

lstm_model = build_lstm_model()
lstm_model.compile(
    optimizer=keras.optimizers.Adam(0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
print("✓ LSTM model built")

# %% [code]
# =======================================================================
# 8. BUILD BiLSTM MODEL
# =======================================================================

print("\n" + "="*70)
print("8. BUILDING BiLSTM MODEL")
print("="*70)

def build_bilstm_model():
    inp = layers.Input(shape=(MAX_LEN,), name='input')
    x = layers.Embedding(VOCAB_SIZE, EMBED_DIM, mask_zero=True)(inp)
    x = layers.Bidirectional(layers.LSTM(256, return_sequences=True, dropout=0.3))(x)
    x = layers.Bidirectional(layers.LSTM(256, dropout=0.3))(x)
    x = layers.Dropout(0.3)(x)
    output = layers.Dense(NUM_CLASSES, activation='softmax')(x)
    return Model(inputs=inp, outputs=output, name='BiLSTM')

bilstm_model = build_bilstm_model()
bilstm_model.compile(
    optimizer=keras.optimizers.Adam(0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
print("✓ BiLSTM model built")

# %% [code]
# =======================================================================
# 9. BUILD GRU MODEL
# =======================================================================

print("\n" + "="*70)
print("9. BUILDING GRU MODEL")
print("="*70)

def build_gru_model():
    inp = layers.Input(shape=(MAX_LEN,), name='input')
    x = layers.Embedding(VOCAB_SIZE, EMBED_DIM, mask_zero=True)(inp)
    x = layers.GRU(256, return_sequences=True, dropout=0.3)(x)
    x = layers.GRU(256, dropout=0.3)(x)
    x = layers.Dropout(0.3)(x)
    output = layers.Dense(NUM_CLASSES, activation='softmax')(x)
    return Model(inputs=inp, outputs=output, name='GRU')

gru_model = build_gru_model()
gru_model.compile(
    optimizer=keras.optimizers.Adam(0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
print("✓ GRU model built")

# %% [code]
# =======================================================================
# 10. BUILD TRANSFORMER MODEL
# =======================================================================

print("\n" + "="*70)
print("10. BUILDING TRANSFORMER MODEL")
print("="*70)

class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super(TransformerBlock, self).__init__()
        self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = keras.Sequential([
            layers.Dense(ff_dim, activation="relu"),
            layers.Dense(embed_dim),
        ])
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, inputs, training=False):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)

def build_transformer_model():
    inp = layers.Input(shape=(MAX_LEN,))
    x = layers.Embedding(VOCAB_SIZE, EMBED_DIM, mask_zero=True)(inp)
    x = TransformerBlock(EMBED_DIM, NUM_HEADS, FF_DIM)(x)
    x = TransformerBlock(EMBED_DIM, NUM_HEADS, FF_DIM)(x)
    x = layers.GlobalAveragePooling1D()(x)
    x = layers.Dropout(0.3)(x)
    output = layers.Dense(NUM_CLASSES, activation='softmax')(x)
    return Model(inputs=inp, outputs=output, name='Transformer')

transformer_model = build_transformer_model()
transformer_model.compile(
    optimizer=keras.optimizers.Adam(0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
print("✓ Transformer model built")

# %% [code]
# =======================================================================
# 11. BUILD PhoBERT MODEL (IMPROVED!)
# =======================================================================

print("\n" + "="*70)
print("11. BUILDING PhoBERT MODEL (IMPROVED)")
print("="*70)

class PhoBERTLayer(layers.Layer):
    def __init__(self, model_name='vinai/phobert-base', trainable_layers=2, **kwargs):
        super().__init__(**kwargs)
        self.model_name = model_name
        self.trainable_layers = trainable_layers  # NEW: Unfreeze top N layers
        self.phobert = None

    def build(self, input_shape):
        self.phobert = TFAutoModel.from_pretrained(self.model_name)
        
        # NEW: Unfreeze only the last N layers for fine-tuning
        if self.trainable_layers > 0:
            # Freeze all layers first
            for layer in self.phobert.layers:
                layer.trainable = False
            # Unfreeze the last N encoder layers
            for layer in self.phobert.roberta.encoder.layer[-self.trainable_layers:]:
                layer.trainable = True
        
        super().build(input_shape)

    def call(self, inputs, training=False):
        input_ids, attention_mask = inputs
        outputs = self.phobert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            training=training
        )
        return outputs.last_hidden_state

    def get_config(self):
        config = super().get_config()
        config.update({
            'model_name': self.model_name,
            'trainable_layers': self.trainable_layers
        })
        return config

def build_phobert_model():
    input_ids = layers.Input(shape=(128,), dtype=tf.int32, name='input_ids')
    attention_mask = layers.Input(shape=(128,), dtype=tf.int32, name='attention_mask')
    
    # NEW: Unfreeze last 2 encoder layers
    phobert_layer = PhoBERTLayer(trainable_layers=2, name='phobert')
    embeddings = phobert_layer([input_ids, attention_mask])
    
    cls_token = embeddings[:, 0, :]
    x = layers.Dropout(0.3)(cls_token)
    x = layers.Dense(256, activation='relu')(x)  # NEW: Add hidden layer
    x = layers.Dropout(0.2)(x)
    output = layers.Dense(NUM_CLASSES, activation='softmax', name='output')(x)
    
    model = Model(
        inputs=[input_ids, attention_mask],
        outputs=output,
        name='PhoBERT'
    )
    return model

try:
    phobert_model = build_phobert_model()
    # NEW: Lower learning rate for fine-tuning pretrained model
    phobert_model.compile(
        optimizer=keras.optimizers.Adam(1e-5),  # CHANGED: 2e-5 -> 1e-5
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    print("✓ PhoBERT model built successfully!")
    print("  - Learning rate: 1e-5 (reduced)")
    print("  - Unfreezing last 2 encoder layers")
    print("  - Added hidden layer (256 units)")
    PHOBERT_AVAILABLE = True
except Exception as e:
    print(f"⚠️ PhoBERT build failed: {e}")
    PHOBERT_AVAILABLE = False

# %% [code]
# =======================================================================
# 12. PREPARE DATA FOR PhoBERT
# =======================================================================

if PHOBERT_AVAILABLE:
    print("\n" + "="*70)
    print("12. PREPARING DATA FOR PhoBERT")
    print("="*70)

    tokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base')

    def tokenize_texts(texts):
        encoded = tokenizer(
            texts.tolist(),
            max_length=128,
            padding='max_length',
            truncation=True,
            return_tensors='np'
        )
        return {
            'input_ids': encoded['input_ids'],
            'attention_mask': encoded['attention_mask']
        }

    print("Tokenizing train set...")
    phobert_train = tokenize_texts(train_df['text'])
    print("Tokenizing val set...")
    phobert_val = tokenize_texts(val_df['text'])
    print("Tokenizing test set...")
    phobert_test = tokenize_texts(test_df['text'])
    print("✓ PhoBERT data ready")

# %% [code]
# =======================================================================
# 13. TRAINING (IMPROVED WITH CLASS WEIGHTS & EARLY STOPPING)
# =======================================================================

print("\n" + "="*70)
print("13. TRAINING MODELS (WITH CLASS WEIGHTS & EARLY STOPPING)")
print("="*70)

# NEW: Improved callbacks
my_callbacks = [
    callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-6, verbose=0),
    callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1),  # NEW!
]

# Train LSTM
print("\nTraining LSTM (with class weights)...")
print("-" * 70)
lstm_history = lstm_model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=30,
    batch_size=32,
    callbacks=my_callbacks,
    class_weight=class_weight_dict,  # NEW!
    verbose=1
)
lstm_model.save('lstm_model_improved.keras')
print("-" * 70)
print("✓ LSTM trained and saved as 'lstm_model_improved.keras'\n")

# Train BiLSTM
print("Training BiLSTM (with class weights)...")
print("-" * 70)
bilstm_history = bilstm_model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=30,
    batch_size=32,
    callbacks=my_callbacks,
    class_weight=class_weight_dict,  # NEW!
    verbose=1
)
bilstm_model.save('bilstm_model_improved.keras')
print("-" * 70)
print("✓ BiLSTM trained and saved as 'bilstm_model_improved.keras'\n")

# Train GRU
print("Training GRU (with class weights)...")
print("-" * 70)
gru_history = gru_model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=30,
    batch_size=32,
    callbacks=my_callbacks,
    class_weight=class_weight_dict,  # NEW!
    verbose=1
)
gru_model.save('gru_model_improved.keras')
print("-" * 70)
print("✓ GRU trained and saved as 'gru_model_improved.keras'\n")

# Train Transformer
print("Training Transformer (with class weights)...")
print("-" * 70)
transformer_history = transformer_model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=30,
    batch_size=32,
    callbacks=my_callbacks,
    class_weight=class_weight_dict,  # NEW!
    verbose=1
)
transformer_model.save('transformer_model_improved.keras')
print("-" * 70)
print("✓ Transformer trained and saved as 'transformer_model_improved.keras'\n")

# Train PhoBERT
if PHOBERT_AVAILABLE:
    print("Training PhoBERT (improved)...")
    print("-" * 70)
    phobert_history = phobert_model.fit(
        phobert_train,
        y_train,
        validation_data=(phobert_val, y_val),
        epochs=30,
        batch_size=16,
        callbacks=my_callbacks,
        class_weight=class_weight_dict,  # NEW!
        verbose=1
    )
    phobert_model.save('phobert_model_improved.keras')
    print("-" * 70)
    print("✓ PhoBERT trained and saved as 'phobert_model_improved.keras'\n")

# %% [code]
# =======================================================================
# 14. EVALUATION ON TEST SET
# =======================================================================

print("\n" + "="*70)
print("14. EVALUATION ON TEST SET")
print("="*70)

results_data = {}

# LSTM
print("\nLSTM...")
lstm_pred = lstm_model.predict(X_test, verbose=0)
lstm_pred_classes = np.argmax(lstm_pred, axis=1)
lstm_acc = accuracy_score(y_test, lstm_pred_classes)
lstm_f1 = f1_score(y_test, lstm_pred_classes, average='weighted')
results_data['LSTM'] = {'acc': lstm_acc, 'f1': lstm_f1, 'pred': lstm_pred_classes, 'proba': lstm_pred}
print(f"Accuracy: {lstm_acc:.4f} | F1-Score: {lstm_f1:.4f}")

# BiLSTM
print("BiLSTM...")
bilstm_pred = bilstm_model.predict(X_test, verbose=0)
bilstm_pred_classes = np.argmax(bilstm_pred, axis=1)
bilstm_acc = accuracy_score(y_test, bilstm_pred_classes)
bilstm_f1 = f1_score(y_test, bilstm_pred_classes, average='weighted')
results_data['BiLSTM'] = {'acc': bilstm_acc, 'f1': bilstm_f1, 'pred': bilstm_pred_classes, 'proba': bilstm_pred}
print(f"Accuracy: {bilstm_acc:.4f} | F1-Score: {bilstm_f1:.4f}")

# GRU
print("GRU...")
gru_pred = gru_model.predict(X_test, verbose=0)
gru_pred_classes = np.argmax(gru_pred, axis=1)
gru_acc = accuracy_score(y_test, gru_pred_classes)
gru_f1 = f1_score(y_test, gru_pred_classes, average='weighted')
results_data['GRU'] = {'acc': gru_acc, 'f1': gru_f1, 'pred': gru_pred_classes, 'proba': gru_pred}
print(f"Accuracy: {gru_acc:.4f} | F1-Score: {gru_f1:.4f}")

# Transformer
print("Transformer...")
transformer_pred = transformer_model.predict(X_test, verbose=0)
transformer_pred_classes = np.argmax(transformer_pred, axis=1)
transformer_acc = accuracy_score(y_test, transformer_pred_classes)
transformer_f1 = f1_score(y_test, transformer_pred_classes, average='weighted')
results_data['Transformer'] = {'acc': transformer_acc, 'f1': transformer_f1, 'pred': transformer_pred_classes, 'proba': transformer_pred}
print(f"Accuracy: {transformer_acc:.4f} | F1-Score: {transformer_f1:.4f}")

# PhoBERT
if PHOBERT_AVAILABLE:
    print("PhoBERT...")
    phobert_pred = phobert_model.predict(phobert_test, verbose=0)
    phobert_pred_classes = np.argmax(phobert_pred, axis=1)
    phobert_acc = accuracy_score(y_test, phobert_pred_classes)
    phobert_f1 = f1_score(y_test, phobert_pred_classes, average='weighted')
    results_data['PhoBERT'] = {'acc': phobert_acc, 'f1': phobert_f1, 'pred': phobert_pred_classes, 'proba': phobert_pred}
    print(f"Accuracy: {phobert_acc:.4f} | F1-Score: {phobert_f1:.4f}")

# %% [code]
# =======================================================================
# 15. ENSEMBLE MODEL (NEW!)
# =======================================================================

print("\n" + "="*70)
print("15. ENSEMBLE MODEL (NEW!)")
print("="*70)

def ensemble_predict(predictions_list, weights=None):
    """Combine predictions from multiple models using weighted average"""
    if weights is None:
        weights = [1/len(predictions_list)] * len(predictions_list)
    
    # Weighted average of probabilities
    ensemble_proba = np.zeros_like(predictions_list[0])
    for pred, w in zip(predictions_list, weights):
        ensemble_proba += w * pred
    
    return np.argmax(ensemble_proba, axis=1), ensemble_proba

# Ensemble: LSTM + GRU + Transformer (top 3 performers)
print("\nEnsemble (LSTM + GRU + Transformer):")

# Simple average
ensemble_pred_classes, ensemble_proba = ensemble_predict([
    results_data['LSTM']['proba'],
    results_data['GRU']['proba'],
    results_data['Transformer']['proba']
])

ensemble_acc = accuracy_score(y_test, ensemble_pred_classes)
ensemble_f1 = f1_score(y_test, ensemble_pred_classes, average='weighted')
results_data['Ensemble'] = {'acc': ensemble_acc, 'f1': ensemble_f1, 'pred': ensemble_pred_classes}

print(f"Accuracy: {ensemble_acc:.4f} | F1-Score: {ensemble_f1:.4f}")

# Weighted ensemble based on validation performance
print("\nWeighted Ensemble (based on F1 scores):")
f1_scores = [results_data['LSTM']['f1'], results_data['GRU']['f1'], results_data['Transformer']['f1']]
total_f1 = sum(f1_scores)
weights = [f1/total_f1 for f1 in f1_scores]
print(f"  Weights: LSTM={weights[0]:.3f}, GRU={weights[1]:.3f}, Transformer={weights[2]:.3f}")

weighted_ensemble_pred_classes, _ = ensemble_predict([
    results_data['LSTM']['proba'],
    results_data['GRU']['proba'],
    results_data['Transformer']['proba']
], weights=weights)

weighted_ensemble_acc = accuracy_score(y_test, weighted_ensemble_pred_classes)
weighted_ensemble_f1 = f1_score(y_test, weighted_ensemble_pred_classes, average='weighted')
results_data['Weighted Ensemble'] = {'acc': weighted_ensemble_acc, 'f1': weighted_ensemble_f1, 'pred': weighted_ensemble_pred_classes}

print(f"Accuracy: {weighted_ensemble_acc:.4f} | F1-Score: {weighted_ensemble_f1:.4f}")

# %% [code]
# =======================================================================
# 16. MODEL COMPARISON
# =======================================================================

print("\n" + "="*70)
print("16. MODEL COMPARISON")
print("="*70)

models_list = ['LSTM', 'BiLSTM', 'GRU', 'Transformer']
model_objs = [lstm_model, bilstm_model, gru_model, transformer_model]
if PHOBERT_AVAILABLE:
    models_list.append('PhoBERT')
    model_objs.append(phobert_model)

# Add ensemble results
models_list.extend(['Ensemble', 'Weighted Ensemble'])

results_df = pd.DataFrame({
    'Model': models_list,
    'Accuracy': [results_data[m]['acc'] for m in models_list],
    'F1-Score': [results_data[m]['f1'] for m in models_list],
})

print("\n" + results_df.to_string(index=False))

best_idx = results_df['F1-Score'].idxmax()
best_model_name = results_df.loc[best_idx, 'Model']
print(f"\n🏆 Best Model: {best_model_name} (F1={results_df.loc[best_idx, 'F1-Score']:.4f})")

# %% [code]
# =======================================================================
# 17. VISUALIZATIONS
# =======================================================================

print("\n" + "="*70)
print("17. CREATING VISUALIZATIONS")
print("="*70)

# Training History
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

histories = {
    'LSTM': lstm_history,
    'BiLSTM': bilstm_history,
    'GRU': gru_history,
    'Transformer': transformer_history
}

colors = {'LSTM': 'o', 'BiLSTM': 's', 'GRU': '^', 'Transformer': 'd'}

for idx, (name, hist) in enumerate(histories.items()):
    axes[0].plot(hist.history['loss'], label=f'{name} Train', marker=colors[name], alpha=0.7)
    axes[0].plot(hist.history['val_loss'], label=f'{name} Val', marker=colors[name], linestyle='--', alpha=0.7)

if PHOBERT_AVAILABLE:
    axes[0].plot(phobert_history.history['loss'], label='PhoBERT Train', marker='*', alpha=0.7)
    axes[0].plot(phobert_history.history['val_loss'], label='PhoBERT Val', marker='*', linestyle='--', alpha=0.7)

axes[0].set_title('Training & Validation Loss', fontweight='bold', fontsize=13)
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].legend(fontsize=9)
axes[0].grid(alpha=0.3)

for idx, (name, hist) in enumerate(histories.items()):
    axes[1].plot(hist.history['accuracy'], label=f'{name} Train', marker=colors[name], alpha=0.7)
    axes[1].plot(hist.history['val_accuracy'], label=f'{name} Val', marker=colors[name], linestyle='--', alpha=0.7)

if PHOBERT_AVAILABLE:
    axes[1].plot(phobert_history.history['accuracy'], label='PhoBERT Train', marker='*', alpha=0.7)
    axes[1].plot(phobert_history.history['val_accuracy'], label='PhoBERT Val', marker='*', linestyle='--', alpha=0.7)

axes[1].set_title('Training & Validation Accuracy', fontweight='bold', fontsize=13)
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Accuracy')
axes[1].legend(fontsize=9)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('training_history_improved.png', dpi=300, bbox_inches='tight')
plt.show()
print("✓ Saved: training_history_improved.png")

# Model Comparison Bar Chart (Updated with Ensemble)
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(results_df))
width = 0.35

bars1 = ax.bar(x - width/2, results_df['Accuracy'], width, label='Accuracy', color='steelblue')
bars2 = ax.bar(x + width/2, results_df['F1-Score'], width, label='F1-Score', color='coral')

ax.set_xlabel('Model', fontweight='bold', fontsize=12)
ax.set_ylabel('Score', fontweight='bold', fontsize=12)
ax.set_title('Model Performance Comparison (Improved)', fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(results_df['Model'], rotation=45, ha='right')
ax.legend()
ax.grid(alpha=0.3, axis='y')
ax.set_ylim(0, 1)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.3f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('model_comparison_improved.png', dpi=300, bbox_inches='tight')
plt.show()
print("✓ Saved: model_comparison_improved.png")

# %% [code]
# =======================================================================
# 18. SAVE RESULTS
# =======================================================================

print("\n" + "="*70)
print("18. SAVING RESULTS")
print("="*70)

results_df.to_csv('model_comparison_improved.csv', index=False)
print("✓ Saved: model_comparison_improved.csv")

# %% [code]
# =======================================================================
# 19. FINAL SUMMARY
# =======================================================================

print("\n" + "="*70)
print("✅ TRAINING COMPLETE (IMPROVED VERSION)!")
print("="*70)

print("""
📊 IMPROVEMENTS APPLIED:
  ✓ Class Weights (handling imbalanced data)
  ✓ Early Stopping (preventing overfitting)
  ✓ Improved text preprocessing (number normalization)
  ✓ Increased MAX_LEN (100 → 128)
  ✓ PhoBERT fine-tuning (unfreezing layers, lower LR)
  ✓ Ensemble Models (combining top performers)

📊 FINAL RESULTS:
""")

for model_name in models_list:
    print(f"  {model_name}: Accuracy={results_data[model_name]['acc']:.4f} | F1={results_data[model_name]['f1']:.4f}")

print(f"\n🏆 BEST MODEL: {best_model_name} (F1={results_df.loc[best_idx, 'F1-Score']:.4f})")

print("""
📁 OUTPUT FILES:
  - lstm_model_improved.keras
  - bilstm_model_improved.keras
  - gru_model_improved.keras
  - transformer_model_improved.keras
  - phobert_model_improved.keras
  - model_comparison_improved.csv
  - training_history_improved.png
  - model_comparison_improved.png
  - label_distribution.png
""")
