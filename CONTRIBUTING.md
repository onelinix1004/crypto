# 🤝 Contributing to Crypto Tracker

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🌟 Ways to Contribute

- 🐛 **Report bugs** via GitHub Issues
- 💡 **Suggest features** or enhancements
- 📝 **Improve documentation**
- 🔧 **Submit bug fixes** or new features
- 🎨 **Improve UI/UX design**
- ✅ **Write tests**

## 🚀 Getting Started

### 1. Fork & Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/crypto-tracker.git
cd crypto-tracker

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/crypto-tracker.git
```

### 2. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b fix/bug-description
```

### 3. Make Changes

- Write clean, readable code
- Follow existing code style
- Add comments for complex logic
- Update documentation if needed

### 4. Test Your Changes

```bash
# Run the dev server
npm run dev

# Run linting
npm run lint

# Build to ensure no errors
npm run build
```

### 5. Commit & Push

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add portfolio tracking feature"

# Push to your fork
git push origin feature/your-feature-name
```

### 6. Submit Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Provide a clear description of changes
4. Reference any related issues
5. Wait for review

## 📋 Code Style Guidelines

### TypeScript

```typescript
// ✅ Good: Use explicit types
const fetchData = async (): Promise<Crypto[]> => {
  // ...
};

// ❌ Bad: Implicit any
const fetchData = async () => {
  // ...
};
```

### React Components

```typescript
// ✅ Good: Functional components with TypeScript
export const CryptoCard: React.FC<CryptoCardProps> = ({ crypto }) => {
  return <div className="crypto-card">{/* ... */}</div>;
};

// ❌ Bad: Class components (avoid unless necessary)
```

### Naming Conventions

| Type        | Convention | Example                |
| ----------- | ---------- | ---------------------- |
| Components  | PascalCase | `CryptoCard.tsx`       |
| Functions   | camelCase  | `fetchCryptos()`       |
| Constants   | UPPER_CASE | `BASE_URL`             |
| Interfaces  | PascalCase | `interface CryptoData` |
| CSS Classes | kebab-case | `.crypto-card`         |

### File Organization

```
src/
├── components/     # Reusable UI components
├── pages/         # Full page components
├── services/      # API calls and external services
├── utils/         # Helper functions
├── layout/        # Layout components
└── styles/        # CSS files
```

## 📝 Commit Message Format

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type       | Description                      |
| ---------- | -------------------------------- |
| `feat`     | New feature                      |
| `fix`      | Bug fix                          |
| `docs`     | Documentation changes            |
| `style`    | Code style changes (formatting)  |
| `refactor` | Code refactoring                 |
| `perf`     | Performance improvements         |
| `test`     | Adding tests                     |
| `chore`    | Build process or tooling changes |

### Examples

```bash
feat(chart): add 30-day price history option
fix(search): resolve case-sensitive search issue
docs(readme): update installation instructions
style(crypto-card): improve hover animation
refactor(api): simplify error handling logic
```

## 🐛 Reporting Bugs

When reporting bugs, include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Detailed steps
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Screenshots**: If applicable
6. **Environment**: OS, browser, Node version

### Bug Report Template

```markdown
**Description**
Brief description of the bug

**Steps to Reproduce**

1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior**
What you expected to happen

**Screenshots**
Add screenshots if helpful

**Environment**

- OS: Windows 11
- Browser: Chrome 120
- Node: v18.17.0
```

## 💡 Suggesting Features

When suggesting features:

1. **Use Case**: Explain why this feature is needed
2. **Proposed Solution**: How you think it should work
3. **Alternatives**: Other solutions you've considered
4. **Mockups**: Visual designs if applicable

## ✅ Pull Request Checklist

Before submitting, ensure:

- [ ] Code follows project style guidelines
- [ ] All existing tests pass
- [ ] New features have appropriate documentation
- [ ] Commit messages follow conventions
- [ ] No console errors or warnings
- [ ] TypeScript types are properly defined
- [ ] UI is responsive (test on mobile)
- [ ] Changes are backward compatible

## 🎨 Design Guidelines

### Colors

```css
/* Primary Colors */
--primary: #add8e6; /* Light Blue */
--background: #010203; /* Dark Background */
--text-primary: #e0e0e0; /* Light Gray */
--text-secondary: #9ca3af; /* Medium Gray */

/* Status Colors */
--positive: #2ed573; /* Green for positive changes */
--negative: #ff4757; /* Red for negative changes */
```

### Spacing

- Use multiples of 0.25rem (4px)
- Common values: 0.5rem, 1rem, 1.5rem, 2rem

### Animations

- Use `transition: all 0.3s ease` for smooth effects
- Hover states should be subtle but noticeable

## 🧪 Testing Guidelines

While we don't have tests yet, when adding them:

### Unit Tests

Test individual functions and utilities:

```typescript
// Example test structure
describe("formatPrice", () => {
  it("should format large prices correctly", () => {
    expect(formatPrice(43250.5)).toBe("$43,250.50");
  });

  it("should show 8 decimals for small prices", () => {
    expect(formatPrice(0.0000125)).toBe("0.00001250");
  });
});
```

### Integration Tests

Test component interactions and API calls.

## 📚 Documentation

When updating documentation:

- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Update both English and Vietnamese docs if applicable

## 🔍 Code Review Process

1. **Automated Checks**: Linting and build must pass
2. **Review**: Maintainer reviews code for quality
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, PR will be merged
5. **Thanks**: Your contribution is appreciated! 🎉

## ❓ Questions?

- 💬 Open a [Discussion](https://github.com/OWNER/crypto-tracker/discussions)
- 📧 Contact maintainer
- 📖 Check existing [Issues](https://github.com/OWNER/crypto-tracker/issues)

## 🙏 Recognition

Contributors will be:

- Listed in the README
- Credited in release notes
- Appreciated by the community! ❤️

---

**Thank you for contributing to Crypto Tracker!** 🚀
