# Contributing to CanvasTUI

Thank you for your interest in contributing to CanvasTUI! This document provides guidelines and instructions for contributing.

## 🌟 Ways to Contribute

- **Bug Reports**: Submit issues for bugs you encounter
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit pull requests with bug fixes or new features
- **Documentation**: Help improve or translate documentation
- **Testing**: Test new releases and report issues

## 🐛 Bug Reports

When submitting a bug report, please include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: OS, Python version, terminal emulator
6. **Screenshots**: If applicable

## 💡 Feature Requests

For feature requests, please include:

1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: Any alternative solutions considered?

## 🔧 Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- A terminal with ANSI color support

### Setup Steps

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/CanvasTUI.git
cd CanvasTUI

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check canvastui
mypy canvastui
```

## 📝 Commit Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only changes |
| `style` | Changes that do not affect code meaning |
| `refactor` | Code change without fix or feature |
| `test` | Adding or modifying tests |
| `chore` | Changes to build process or auxiliary tools |

### Examples

```bash
feat: add node editing capability
fix: resolve canvas loading issue with empty files
docs: update installation instructions
refactor: improve search performance
test: add unit tests for canvas parser
```

## 🔀 Pull Request Process

1. **Create a Branch**: Create a feature branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**: Implement your changes with clear commits

3. **Run Tests**: Ensure all tests pass
   ```bash
   pytest
   ```

4. **Run Linting**: Ensure code quality
   ```bash
   ruff check canvastui
   mypy canvastui
   ```

5. **Update Documentation**: Update docs if needed

6. **Submit PR**: Open a pull request with:
   - Clear title following commit convention
   - Description of changes
   - Reference to related issues

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow convention

## 📚 Code Style

### Python

- Follow PEP 8 guidelines
- Use type hints for all public functions
- Maximum line length: 100 characters
- Use docstrings for modules, classes, and functions

### Example

```python
def search_nodes(self, query: str) -> list[CanvasNode]:
    """
    Search nodes by text content.
    
    Args:
        query: Search query string
        
    Returns:
        List of matching nodes
    """
    query_lower = query.lower()
    return [
        node for node in self.nodes
        if query_lower in node.text.lower()
    ]
```

## 🌍 Translations

We welcome translations! To add a new language:

1. Copy `README.md` to `README_XX.md` (where XX is language code)
2. Translate the content
3. Update the language links in all README files
4. Submit a pull request

## 📋 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community

## ❓ Questions?

Feel free to open an issue for any questions or reach out to the maintainer.

---

Thank you for contributing to CanvasTUI! 🎨
