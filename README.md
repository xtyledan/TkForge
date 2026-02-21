# 🎨 TkForge - Visual Tkinter GUI Builder

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com)

**TkForge** is a powerful visual GUI designer for Python's Tkinter framework. Build beautiful desktop applications with a simple drag-and-drop interface - no design skills required! Similar to Tkinter Designer, but with real-time visual editing and live preview capabilities.

### 🎯 Why TkForge?

Creating Tkinter UIs traditionally requires writing lots of boilerplate code and constantly running your script to see changes. **TkForge changes that.** Design visually, preview instantly, and generate production-ready Python code in seconds.

---

## 🎬 Demo

*Demo GIF and screenshots coming soon!*

### Example: Login Form in 2 Minutes
Check out our [Quick Start Guide](QUICKSTART.md) to build your first GUI in under 3 minutes!

## Features

✨ **Visual Widget Palette** - Add buttons, labels, entries, text boxes, checkbuttons, radiobuttons, listboxes, comboboxes, frames, and canvases with a single click

🎨 **Drag-and-Drop Canvas** - Position widgets visually by dragging them on a grid-aligned canvas

⚙️ **Properties Panel** - Customize widget properties including:
- Text content
- Position (X, Y coordinates)
- Size (Width, Height)
- Colors (Background and Foreground)
- Delete widgets

💾 **Save/Load Projects** - Save your GUI designs as JSON files and load them later for editing

🐍 **Python Code Generation** - Automatically generate clean, ready-to-use Python/Tkinter code from your design

👁️ **Live Preview** - Preview your GUI in real-time before generating code

---

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- Tkinter (comes pre-installed with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/TkForge.git
   cd TkForge
   ```

2. **Run TkForge**
   ```bash
   python main.py
   ```

That's it! No dependencies to install. 🎉

### Your First GUI in 60 Seconds

```bash
# 1. Start TkForge
python main.py

# 2. Click "Add Button" from the left palette
# 3. Drag it on the canvas
# 4. Customize properties on the right
# 5. Click Generate → Generate Python Code
# 6. Save and run your new GUI!
```

### Creating a GUI

1. **Add Widgets**: Click on widget buttons in the left panel to add them to the canvas
2. **Position Widgets**: Drag widgets on the canvas to position them (snaps to grid)
3. **Customize Properties**: Click on a widget to select it, then edit its properties in the right panel
4. **Save Project**: File → Save Project to save your design as JSON
5. **Generate Code**: Generate → Generate Python Code to create Tkinter code
6. **Preview**: Generate → Preview GUI to see how your GUI will look

### Generated Code

The generated code is production-ready and includes:
- All widget definitions with your custom properties
- Proper placement using `.place()` geometry manager
- A standalone Python file that can be run immediately

### Example Workflow

1. Add a Label widget for a title
2. Add Entry widgets for user input
3. Add a Button widget for submission
4. Customize colors, text, and positions
5. Preview the GUI
6. Generate Python code
7. Save to a .py file and run it!

## Keyboard Shortcuts

- **Save Project**: File → Save Project (Ctrl+S in future versions)
- **New Project**: File → New Project

## File Format

Projects are saved as JSON files containing all widget information:
```json
[
  {
    "id": "button_1",
    "type": "button",
    "name": "Button",
    "x": 100,
    "y": 100,
    "width": 100,
    "height": 30,
    "text": "Click Me",
    "bg": "SystemButtonFace",
    "fg": "black",
    "font": ["Arial", 10]
  }
]
```

---

## 🗺️ Roadmap

Future enhancements planned for TkForge:

- [ ] **More Widgets** - Scale, Spinbox, Menu, Scrollbar, and more
- [ ] **Layout Managers** - Support for grid and pack layout managers
- [ ] **Advanced Styling** - Font customization, padding, borders
- [ ] **Alignment Tools** - Auto-align, distribute, and snap-to-widget features
- [ ] **Undo/Redo** - Full history management
- [ ] **Copy/Paste/Duplicate** - Quickly replicate widgets
- [ ] **Figma Import** - Import designs from Figma (like Tkinter Designer)
- [ ] **Multi-Framework Export** - Export to PyQt, Kivy, and other frameworks
- [ ] **Themes** - Pre-built themes and color schemes
- [ ] **Code Templates** - Event handlers and business logic templates

Want to contribute? Check out our [Contributing Guide](CONTRIBUTING.md)!

---

## 📊 Comparison with Tkinter Designer

| Feature | TkForge | Tkinter Designer |
|---------|---------|------------------|
| **Visual Editor** | ✅ Drag & Drop | ❌ No visual editor |
| **Figma Import** | 🔄 Planned | ✅ Yes |
| **Code Generation** | ✅ Yes | ✅ Yes |
| **Save/Load Projects** | ✅ JSON format | ❌ N/A |
| **Live Preview** | ✅ Real-time | ❌ N/A |
| **Learning Curve** | ⭐ Easy | ⭐⭐ Medium |
| **Standalone** | ✅ No dependencies | ✅ Minimal |

---

## 💡 Pro Tips

- 📐 **Use grid lines** for precise widget alignment
- 🖼️ **Start with a Frame** as a container for complex layouts
- 👀 **Preview before generating** to catch issues early
- 💾 **Save frequently** - your work is precious!
- 🔄 **Iterate quickly** using the live preview feature
- 📝 **Export often** to have code backups at different stages

---

## 🤝 Contributing

We welcome contributions! Whether it's:
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 📖 Improving documentation
- 🔧 Submitting pull requests

Please read our [Contributing Guidelines](CONTRIBUTING.md) to get started.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Free to use, modify, and distribute! ⚖️

---

## 🌟 Show Your Support

If you find TkForge helpful:
- ⭐ Star this repository
- 🐦 Share it on social media
- 🔗 Link to it in your projects
- 🤝 Contribute to the code

---

## 📞 Contact & Support

- 💬 **Issues**: [GitHub Issues](https://github.com/yourusername/TkForge/issues)
- 📧 **Questions**: Open a discussion on GitHub
- 🌐 **Website**: *Coming soon*

---

**Built with ❤️ for the Python community**

Happy GUI building! 🚀
