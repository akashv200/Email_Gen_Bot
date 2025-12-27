# Email Generator Bot

A template-based, privacy-focused desktop application for Windows that generates professional emails without AI or internet connectivity.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 🌟 Features

### Core Features
- **Template-Based Generation**: Pre-defined professional email templates
- **No AI Required**: Deterministic, reliable output every time
- **Offline Operation**: Works without internet connectivity
- **Privacy-Focused**: All data stays on your local machine
- **Always-on-Top**: Overlay window for easy access
- **Animated Interface**: Smooth, engaging user experience
- **Real-Time Preview**: Review before copying or exporting

### Email Categories
1. **Job Application** - Professional job application emails
2. **Leave Request** - Formal leave/vacation requests
3. **Professional Apology** - Sincere business apologies
4. **Internship Request** - Student internship applications
5. **General Formal Communication** - Customizable formal emails

### Technical Features
- Dynamic form rendering based on email type
- Input validation and placeholder management
- Clipboard integration for easy copying
- Scrollable forms for complex templates
- Modular architecture for easy expansion

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10/11 (32-bit or 64-bit)
- **Python**: 3.7 or higher
- **RAM**: 256 MB minimum
- **Storage**: 50 MB available space

### Python Dependencies
- `tkinter` (included with Python)
- Standard library modules only (no external packages required)

## 🚀 Installation

### Method 1: Run from Source

1. **Install Python** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Download the Application**
   ```bash
   # Option A: Clone repository
   git clone https://github.com/yourusername/email-generator-bot.git
   cd email-generator-bot
   
   # Option B: Download the email_generator_bot.py file directly
   ```

3. **Run the Application**
   ```bash
   python email_generator_bot.py
   ```

### Method 2: Create Windows Executable

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Build Executable**
   ```bash
   pyinstaller --onefile --windowed --name="EmailGeneratorBot" email_generator_bot.py
   ```

3. **Run the Executable**
   - Find the executable in the `dist` folder
   - Double-click `EmailGeneratorBot.exe` to run

### Method 3: Create Desktop Shortcut

1. **Create a batch file** (`run_email_bot.bat`):
   ```batch
   @echo off
   python "C:\path\to\email_generator_bot.py"
   ```

2. **Create shortcut**
   - Right-click the batch file
   - Select "Create shortcut"
   - Move shortcut to desktop

## 📖 Usage Guide

### Step 1: Launch Application
- Run the Python script or executable
- Welcome screen appears with animation

### Step 2: Select Email Category
- Choose from available email categories:
  - 💼 Job Application
  - 📅 Leave Request
  - 🙏 Professional Apology
  - 🎓 Internship Request
  - ✉️ General Formal Communication

### Step 3: Fill in Details
- Complete all required fields in the form
- Fields are dynamically generated based on category
- Use placeholders as guidance
- Scroll for additional fields if needed

### Step 4: Generate Email
- Click "Generate Email" button
- Review the generated email in preview screen

### Step 5: Copy or Export
- Click "📋 Copy to Clipboard" to copy the email
- Paste into your email client
- Or click "✨ Generate New Email" to start over

## 🎨 User Interface

### Welcome Screen
- Animated introduction
- Feature highlights
- Smooth transition to main interface

### Category Selection
- Visual category cards with icons
- Hover effects for better UX
- Clear descriptions for each category

### Form Screen
- Dynamic field generation
- Scrollable for long forms
- Input validation
- Placeholder text management
- Back navigation

### Preview Screen
- Read-only email preview
- Professional formatting
- Copy to clipboard functionality
- Easy navigation

## 🔧 Customization

### Adding New Templates

To add a new email template, edit the `EmailTemplateLibrary.get_templates()` method:

```python
"custom_template": EmailTemplate(
    name="Custom Template Name",
    template="""Subject: {subject}

Dear {recipient},

{content}

Best regards,
{sender}""",
    fields=[
        {"name": "subject", "label": "Subject", "type": "text", "placeholder": "Email subject"},
        {"name": "recipient", "label": "Recipient", "type": "text", "placeholder": "Recipient name"},
        {"name": "content", "label": "Content", "type": "textarea", "placeholder": "Email body"},
        {"name": "sender", "label": "Sender", "type": "text", "placeholder": "Your name"}
    ]
)
```

### Field Types

1. **Text Field** (`type: "text"`)
   - Single-line input
   - For short text entries

2. **Text Area** (`type: "textarea"`)
   - Multi-line input
   - For longer content

3. **Select/Dropdown** (`type: "select"`)
   - Predefined options
   - Requires `options` list

### Customizing Colors

Edit the color codes in the respective screen classes:

```python
# Background colors
bg="#0f1419"  # Dark background
bg="#1a1a2e"  # Input backgrounds
bg="#16213e"  # Button backgrounds

# Text colors
fg="#00d9ff"  # Primary accent (cyan)
fg="#ffffff"  # White text
fg="#a8a8a8"  # Gray text
```

## 🏗️ Architecture

### Module Structure

```
email_generator_bot.py
├── EmailTemplate (Data class)
├── EmailTemplateLibrary (Template storage)
├── AnimatedWelcomeScreen (Welcome UI)
├── CategorySelectionScreen (Category UI)
├── FormScreen (Form UI)
├── PreviewScreen (Preview UI)
└── EmailGeneratorBot (Main controller)
```

### Design Patterns

1. **Template Pattern**: Email templates with placeholders
2. **Screen Navigation**: State-based UI transitions
3. **Event-Driven**: User interactions trigger state changes
4. **Separation of Concerns**: UI, logic, and data separated

### Data Flow

```
User Input → Form Values → Template Processing → Email Generation → Preview → Clipboard
```

## 🔒 Privacy & Security

### Privacy Features
- **No Network Calls**: Application works completely offline
- **No Data Storage**: No persistent storage of user data
- **No Telemetry**: No tracking or analytics
- **Local Processing**: All processing happens on local machine

### Security Considerations
- Input validation to prevent errors
- No execution of user-provided code
- Template-based generation prevents injection
- Read-only preview to prevent accidental modification

## 🐛 Troubleshooting

### Common Issues

**Issue**: Application doesn't start
- **Solution**: Ensure Python 3.7+ is installed and in PATH

**Issue**: Window doesn't stay on top
- **Solution**: Check if "Always on top" is supported by your OS

**Issue**: Clipboard copy doesn't work
- **Solution**: Restart the application or check clipboard access permissions

**Issue**: Form fields not clearing
- **Solution**: Click on the field and manually clear it

### Debug Mode

To enable debug output, add at the start of `main()`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance

### Benchmarks
- **Startup Time**: < 2 seconds
- **Email Generation**: < 100ms
- **Memory Usage**: ~50MB
- **CPU Usage**: < 1% idle, < 5% during generation

### Optimization Tips
- Application is already optimized for minimal resource usage
- Consider using the executable version for faster startup
- Close other applications if running on low-end hardware

## 🔮 Future Enhancements

### Planned Features
1. **Template Import/Export**: Save custom templates
2. **Multiple Languages**: Support for non-English templates
3. **Email History**: Optional local history storage
4. **PDF Export**: Direct export to PDF format
5. **Keyboard Shortcuts**: Quick navigation and actions
6. **Theme Customization**: Light/dark mode toggle
7. **Template Marketplace**: Share templates with community

### Contributing
To contribute new templates or features:
1. Fork the repository
2. Create feature branch
3. Add your template or feature
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Python and Tkinter
- Inspired by the need for privacy-focused, offline tools
- Designed for professionals, students, and anyone needing quick email generation

## 📞 Support

### Getting Help
- Check the troubleshooting section above
- Review the usage guide
- Check existing GitHub issues

### Reporting Bugs
When reporting bugs, include:
1. Python version
2. Operating system
3. Steps to reproduce
4. Expected vs actual behavior
5. Error messages (if any)

## 🎯 Use Cases

### Professionals
- Quick job application emails
- Leave requests
- Formal business communication
- Professional apologies

### Students
- Internship applications
- Academic correspondence
- Formal requests to faculty
- Professional networking emails

### General Users
- Any formal email requirement
- Template-based email needs
- Privacy-conscious communication
- Offline email preparation

## 💡 Tips for Best Results

1. **Fill All Fields**: Complete information generates better emails
2. **Review Before Copying**: Always preview the generated email
3. **Customize After Copy**: Feel free to edit the copied text
4. **Use Placeholders**: Read placeholder text for guidance
5. **Save Templates**: Keep a copy of your favorite customizations

## 🎓 Educational Value

This project demonstrates:
- GUI development with Tkinter
- Event-driven programming
- State management
- Template processing
- User interface design
- Software engineering principles
- Modular architecture
- Documentation best practices

Perfect for:
- Learning Python GUI development
- Understanding design patterns
- Studying user experience design
- Portfolio projects
- Academic coursework

---

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Author**: Email Generator Bot Team  
**Status**: Production Ready
