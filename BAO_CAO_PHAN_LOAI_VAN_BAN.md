# BÁO CÁO: PHÂN LOẠI VĂN BẢN TIN TỨC TÀI CHÍNH TIẾNG VIỆT (ARGUMENT CLASSIFICATION)

---

## 1. TỔNG QUAN DỰ ÁN

### 1.1 Mục tiêu

Xây dựng và so sánh hiệu suất của các mô hình Deep Learning trong bài toán **phân loại văn bản tiếng Việt** - cụ thể là phân loại các đoạn tin tức tài chính thành các loại lập luận (Argument Classification).

### 1.2 Bộ dữ liệu

- **Nguồn dữ liệu**: File Excel chứa tin tức tài chính tiếng Việt
- **Tổng mẫu ban đầu**: 16,975 mẫu
- **Sau khi làm sạch**: 16,959 mẫu (loại bỏ 16 mẫu có giá trị thiếu)
- **Các cột dữ liệu chính**: `text` (nội dung văn bản), `argument_classification_label` (nhãn phân loại)

### 1.3 Phân bố nhãn (3 lớp)

| Nhãn         | Số lượng | Tỷ lệ  |
| ------------ | -------- | ------ |
| **Tiền đề**  | 11,547   | 68.09% |
| **Kịch bản** | 3,150    | 18.57% |
| **Kết luận** | 2,262    | 13.34% |

> **Nhận xét**: Dữ liệu có sự mất cân bằng đáng kể, với lớp "Tiền đề" chiếm đa số (~68%).

### 1.4 Thống kê văn bản

- Độ dài trung bình: **386.7 ký tự**
- Số từ trung bình: **84.5 từ**
- Số từ tối đa: **1,083 từ**
- Phân vị 95%: **178 từ**

---

## 2. PHƯƠNG PHÁP THỰC HIỆN

### 2.1 Tiền xử lý dữ liệu

1. Loại bỏ giá trị thiếu
2. Làm sạch văn bản (lowercase, loại bỏ ký tự đặc biệt)
3. Mã hóa nhãn bằng `LabelEncoder`
4. Xây dựng từ điển từ tập huấn luyện (từ xuất hiện ≥ 2 lần)

### 2.2 Tham số cấu hình

| Tham số                | Giá trị |
| ---------------------- | ------- |
| Kích thước từ điển     | 5,543   |
| Độ dài chuỗi tối đa    | 100     |
| Embedding dimension    | 128     |
| Số heads (Transformer) | 8       |
| Feed-forward dimension | 256     |

### 2.3 Chia tập dữ liệu

| Tập        | Số lượng | Tỷ lệ |
| ---------- | -------- | ----- |
| Training   | 11,871   | 70%   |
| Validation | 2,544    | 15%   |
| Test       | 2,544    | 15%   |

---

## 3. CÁC MÔ HÌNH ĐÃ XÂY DỰNG

### 3.1 LSTM (Long Short-Term Memory)

- 2 lớp LSTM với 256 units mỗi lớp
- Dropout: 0.3
- Optimizer: Adam (lr=0.001)

### 3.2 BiLSTM (Bidirectional LSTM)

- 2 lớp Bidirectional LSTM với 256 units
- Dropout: 0.3
- Optimizer: Adam (lr=0.001)

### 3.3 GRU (Gated Recurrent Unit)

- 2 lớp GRU với 256 units mỗi lớp
- Dropout: 0.3
- Optimizer: Adam (lr=0.001)

### 3.4 Transformer

- 2 Transformer blocks
- Multi-Head Attention (8 heads)
- Global Average Pooling
- Dropout: 0.3

### 3.5 PhoBERT

- Pretrained model: `vinai/phobert-base`
- Fine-tuning với classification head
- Optimizer: Adam (lr=2e-5)
- Batch size: 16 (nhỏ hơn do giới hạn bộ nhớ)

---

## 4. QUÁ TRÌNH HUẤN LUYỆN

### 4.1 Cấu hình huấn luyện

- **Epochs**: 30
- **Batch size**: 32 (16 cho PhoBERT)
- **Callbacks**: ReduceLROnPlateau (factor=0.5, patience=2, min_lr=1e-6)

### 4.2 Thời gian huấn luyện (GPU T4)

- LSTM: ~7s/epoch
- BiLSTM: ~13s/epoch
- GRU: ~6s/epoch
- Transformer: ~8s/epoch
- PhoBERT: ~105s/epoch

---

## 5. KẾT QUẢ ĐÁNH GIÁ TRÊN TẬP TEST

### 5.1 Bảng so sánh hiệu suất

| Mô hình     | Accuracy   | F1-Score   | Số tham số |
| ----------- | ---------- | ---------- | ---------- |
| LSTM        | 0.7614     | 0.7548     | 1,629,827  |
| BiLSTM      | 0.7535     | 0.7464     | 3,074,435  |
| **GRU** 🏆  | **0.7704** | **0.7664** | 1,401,475  |
| Transformer | 0.7653     | 0.7595     | 1,897,731  |
| PhoBERT     | 0.6808     | 0.5515     | 2,307\*    |

> \*PhoBERT chỉ đếm tham số của classification head (pretrained weights bị đóng băng)

### 5.2 Phân tích kết quả

#### 🏆 Mô hình tốt nhất: **GRU**

- **F1-Score**: 0.7664
- **Accuracy**: 77.04%
- **Số tham số**: Ít nhất trong các mô hình RNN (1.4M)

#### Nhận xét:

1. **GRU** đạt hiệu suất cao nhất với số tham số ít nhất → hiệu quả nhất
2. **LSTM và Transformer** có hiệu suất tương đương (~75.5% F1)
3. **BiLSTM** không cải thiện so với LSTM đơn hướng, có thể do overfitting
4. **PhoBERT** đạt kết quả thấp nhất (68% accuracy, 55% F1) - điều này bất thường và có thể do:
   - Learning rate quá cao/thấp
   - Cần fine-tuning cả pretrained layers
   - Dữ liệu domain-specific không phù hợp với pretrained weights chung

---

## 6. HÌNH ẢNH TRỰC QUAN

Notebook đã tạo các biểu đồ sau:

1. **label_distribution.png** - Phân bố nhãn
2. **training_history.png** - Loss và Accuracy theo epoch
3. **confusion_matrices.png** - Ma trận nhầm lẫn cho từng mô hình
4. **model_comparison.png** - So sánh hiệu suất các mô hình

---

## 7. THỬ NGHIỆM DỰ ĐOÁN (INFERENCE DEMO)

Một số ví dụ dự đoán với mô hình GRU:

| Văn bản                                                                 | Dự đoán  |
| ----------------------------------------------------------------------- | -------- |
| "Chúng tôi khuyến nghị MUA cổ phiếu VNM với giá mục tiêu 85,000 VND..." | Kết luận |
| "Doanh thu quý 3 tăng 25% so với cùng kỳ năm trước..."                  | Tiền đề  |
| "Nếu lãi suất tiếp tục tăng trong 6 tháng tới..."                       | Kịch bản |
| "Công ty hoạt động trong lĩnh vực sản xuất thép"                        | Tiền đề  |

---

## 8. CÁC FILE ĐẦU RA

| File                      | Mô tả                             |
| ------------------------- | --------------------------------- |
| `lstm_model.keras`        | Mô hình LSTM đã huấn luyện        |
| `bilstm_model.keras`      | Mô hình BiLSTM đã huấn luyện      |
| `gru_model.keras`         | Mô hình GRU đã huấn luyện         |
| `transformer_model.keras` | Mô hình Transformer đã huấn luyện |
| `phobert_model.keras`     | Mô hình PhoBERT đã huấn luyện     |
| `model_comparison.csv`    | Bảng so sánh kết quả              |
| `training_history.png`    | Biểu đồ quá trình training        |
| `confusion_matrices.png`  | Ma trận nhầm lẫn                  |
| `model_comparison.png`    | Biểu đồ so sánh mô hình           |
| `label_distribution.png`  | Biểu đồ phân bố nhãn              |

---

## 9. KẾT LUẬN VÀ KHUYẾN NGHỊ

### 9.1 Kết luận

1. **GRU** là mô hình tối ưu nhất cho bài toán này với hiệu suất cao và số tham số ít
2. Các mô hình RNN truyền thống (LSTM, GRU) hoạt động tốt hơn Transformer và PhoBERT trên tập dữ liệu này
3. PhoBERT cần được điều chỉnh thêm để đạt hiệu suất tốt hơn

### 9.2 Khuyến nghị cải thiện

1. **Xử lý mất cân bằng dữ liệu**: Sử dụng class weights hoặc oversampling
2. **Fine-tuning PhoBERT**: Thử các learning rate khác nhau (1e-5, 5e-6)
3. **Data augmentation**: Paraphrase hoặc back-translation
4. **Ensemble**: Kết hợp nhiều mô hình để cải thiện hiệu suất
5. **Cross-validation**: Đánh giá độ ổn định của mô hình

---

## 10. THÔNG TIN KỸ THUẬT

- **Framework**: TensorFlow 2.19.0
- **GPU**: Tesla T4 (Google Colab)
- **Pretrained Model**: vinai/phobert-base
- **Environment**: Google Colab

---

_Báo cáo được tạo tự động từ notebook `Untitled2.ipynb`_
