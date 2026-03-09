# Contributing to PDF Downloader

Thank you for your interest in contributing to PDF Downloader! We welcome contributions from everyone. This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Pull Request Process](#pull-request-process)

## 🤝 Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and adhere to our code of conduct:

- **Be respectful** - Treat all contributors with respect and kindness
- **Be inclusive** - Welcome people of all backgrounds and experience levels
- **Be collaborative** - Work together to solve problems
- **Be professional** - Keep discussions focused and productive

## 🎯 How to Contribute

There are many ways to contribute to PDF Downloader:

1. **Report Bugs** - Found an issue? Let us know!
2. **Suggest Features** - Have an idea? We'd love to hear it!
3. **Write Documentation** - Help improve our docs
4. **Fix Bugs** - Submit pull requests for known issues
5. **Add Features** - Implement new functionality
6. **Improve Tests** - Enhance test coverage
7. **Optimize Performance** - Help make it faster

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account
- Basic understanding of Python and Tkinter

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/YOUR_USERNAME/pdf-downloader.git
cd "Pdf Downloader"
```

3. Add upstream remote:
```bash
git remote add upstream https://github.com/original-repo/pdf-downloader.git
```

## 🛠️ Development Setup

### 1. Create a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Development Tools

```bash
pip install pytest pytest-cov black flake8 mypy
```

### 4. Run the Application

```bash
python pdf_downloads.py
```

## 📝 Coding Standards

### Python Style Guide

We follow PEP 8 with these conventions:

1. **Indentation**: Use 4 spaces (no tabs)
2. **Line Length**: Maximum 88 characters (Black default)
3. **Imports**: Organize in sections (stdlib, third-party, local)
4. **Naming**: 
   - Functions/variables: `snake_case`
   - Classes: `PascalCase`
   - Constants: `UPPER_CASE`

### Code Quality

#### Use Type Hints
```python
def download_pdfs(base_url: str, output_folder: str, max_depth: int) -> None:
    """Download PDFs from a URL"""
    pass
```

#### Add Docstrings
```python
def find_pdfs(url: str, depth: int = 0, max_depth: int = 2) -> None:
    """
    Recursively find PDF links in directories.
    
    Args:
        url: Website URL to scan
        depth: Current recursion depth
        max_depth: Maximum recursion depth
    
    Returns:
        None (modifies global pdf_links list)
    """
    pass
```

#### Error Handling
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.RequestException as e:
    log_callback(f"Error fetching {url}: {e}\n")
```

### Code Formatting

1. **Format Code with Black:**
```bash
black pdf_downloads.py
```

2. **Check with Flake8:**
```bash
flake8 pdf_downloads.py
```

3. **Type Check with MyPy:**
```bash
mypy pdf_downloads.py
```

## 📤 Submitting Changes

### Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number
```

### Commit Messages

Write clear, descriptive commit messages:

```
feat: Add download speed throttling option
fix: Resolve duplicate filename handling
docs: Update README with new features
refactor: Simplify PDF finding logic
test: Add unit tests for download function
```

**Format:**
- First line: 50 characters or less
- Blank line
- Detailed explanation if needed (wrapped at 72 characters)

Example:
```
Add pause/resume functionality for downloads

- Implements pause button in GUI
- Adds resume capability without losing progress
- Stores download state in global variables
- Updates progress tracking to show paused state

Fixes #42
```

### Keep Your Branch Updated

```bash
git fetch upstream
git rebase upstream/main
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Title**: Clear, descriptive title
2. **Description**: What happened vs. what you expected
3. **Steps to Reproduce**: Exact steps to recreate the issue
4. **Environment**: OS, Python version, browser (if applicable)
5. **Logs/Screenshots**: Any error messages or visual evidence
6. **Attempts**: What you've already tried

**Bug Report Template:**
```
Title: [Brief description]

**Description:**
What happened...

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Behavior:**
What should happen...

**Actual Behavior:**
What actually happened...

**Environment:**
- OS: Windows/Linux/macOS
- Python: 3.x
- Version: current

**Logs:**
[Error messages or logs]
```

## 💡 Suggesting Features

When suggesting features, please include:

1. **Use Case**: Why is this useful?
2. **Description**: What should it do?
3. **Example**: How would users interact with it?
4. **Alternatives**: Have you considered other solutions?

**Feature Request Template:**
```
Title: [Feature idea]

**Use Case:**
Describe the problem this solves...

**Description:**
How should this feature work?

**Example:**
Show how users would use it...

**Alternatives:**
Other ways to solve this problem...
```

## 🔄 Pull Request Process

### Before Submitting

1. **Test Your Changes**: Make sure everything works
   ```bash
   python pdf_downloads.py
   ```

2. **Run Tests**: Add tests for new functionality
   ```bash
   pytest
   ```

3. **Format Code**: Use Black and Flake8
   ```bash
   black pdf_downloads.py
   flake8 pdf_downloads.py
   mypy pdf_downloads.py
   ```

4. **Update Documentation**: Add/update docstrings and comments
5. **Update README**: If your changes affect functionality
6. **Sync with Main**: Make sure you're up-to-date
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

### Submit Pull Request

1. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub:
   - Clear title describing the change
   - Reference any related issues (#42)
   - Describe what changes were made
   - Explain why these changes are needed

3. **Pull Request Template**:
   ```
   ## Description
   Brief explanation of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement
   
   ## Related Issues
   Closes #issue_number
   
   ## Testing
   How was this tested?
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Comments added
   - [ ] Documentation updated
   - [ ] Tests added/updated
   - [ ] No new warnings
   ```

### Review Process

- Maintainers will review your PR
- Changes may be requested
- Once approved, your PR will be merged
- You'll be credited as a contributor

## 🐛 Testing

### Run Tests

```bash
pytest
```

### Coverage Report

```bash
pytest --cov=. --cov-report=html
```

### Add Tests

Create tests for new functionality:

```python
# tests/test_pdf_downloads.py
import pytest
from pdf_downloads import download_single_pdf

def test_valid_pdf_download():
    """Test downloading a valid PDF"""
    result = download_single_pdf("http://example.com/test.pdf", "./temp")
    assert result is not None

def test_invalid_url():
    """Test handling of invalid URLs"""
    result = download_single_pdf("invalid-url", "./temp")
    assert result is None
```

## 📚 Documentation

- Update docstrings for code changes
- Update README.md for user-facing changes
- Add comments for complex logic
- Update this file if contribution process changes

## 🏆 Recognition

Contributors will be:
- Listed in a CONTRIBUTORS.md file
- Credited in release notes
- Recognized in the GitHub repository

## ❓ Questions?

- Check existing issues and discussions
- Review the documentation
- Open a discussion issue
- Contact the maintainers

## 📄 License

By contributing to PDF Downloader, you agree that your contributions will be licensed under the same open source license as the project.

---

**Thank you for contributing to PDF Downloader!** 🎉

We appreciate all contributions, no matter how big or small. Your effort helps make this project better for everyone!

**Happy Coding!** 💻
