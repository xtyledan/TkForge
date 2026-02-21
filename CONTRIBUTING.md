# Contributing to TkForge

First off, thank you for considering contributing to TkForge! 🎉 It's people like you that make TkForge such a great tool.

## 🌟 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** - Include code snippets, screenshots, or GIFs
- **Describe the behavior you observed** and what you expected to see
- **Include details about your environment**: OS, Python version, etc.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List any similar features** in other tools

### Pull Requests

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow the existing code style
   - Add comments where necessary
   - Update documentation as needed

3. **Test your changes**
   - Ensure the application runs without errors
   - Test edge cases
   - Verify existing features still work

4. **Commit your changes**
   ```bash
   git commit -m "Add some amazing feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Include screenshots if applicable

## 🎨 Code Style Guidelines

- Use meaningful variable and function names
- Write docstrings for functions and classes
- Keep functions focused on a single responsibility
- Use type hints where appropriate
- Follow PEP 8 style guide

### Example:
```python
def calculate_widget_center(x: int, y: int, width: int, height: int) -> tuple:
    """
    Calculate the center point of a widget.
    
    Args:
        x: X coordinate of top-left corner
        y: Y coordinate of top-left corner
        width: Widget width
        height: Widget height
    
    Returns:
        Tuple of (center_x, center_y)
    """
    center_x = x + width // 2
    center_y = y + height // 2
    return center_x, center_y
```

## 🏗️ Project Structure

```
TkForge/
├── main.py                    # Main application entry point
├── example_generated.py       # Example of generated code
├── template_login_form.json   # Sample template
├── README.md                  # Project documentation
├── QUICKSTART.md             # Quick start guide
├── CONTRIBUTING.md           # This file
├── LICENSE                   # MIT License
└── requirements.txt          # Dependencies (minimal)
```

## 🔍 Areas Needing Contribution

We especially welcome contributions in these areas:

1. **Widget Support**
   - Adding new widget types
   - Enhancing existing widget properties

2. **Layout Managers**
   - Implementing grid layout support
   - Implementing pack layout support

3. **User Interface**
   - Improving the visual design
   - Adding keyboard shortcuts
   - Implementing undo/redo

4. **Code Generation**
   - Improving generated code quality
   - Adding code templates
   - Supporting different coding styles

5. **Documentation**
   - Writing tutorials
   - Creating video guides
   - Improving code comments

6. **Testing**
   - Writing unit tests
   - Integration testing
   - Bug fixing

## 💬 Questions?

Don't hesitate to ask questions! You can:
- Open an issue with the `question` label
- Start a discussion in GitHub Discussions
- Comment on existing issues or pull requests

## 📜 Code of Conduct

Be respectful and constructive in all interactions. We're all here to learn and build something great together!

### Our Standards

- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

## 🎯 Getting Started

Ready to contribute? Here's a quick start:

1. **Set up your development environment**
   ```bash
   git clone https://github.com/yourusername/TkForge.git
   cd TkForge
   python main.py
   ```

2. **Make a small change** to get familiar with the codebase
3. **Test thoroughly**
4. **Submit your first PR!**

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making TkForge better! 🚀**
