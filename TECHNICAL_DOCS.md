# Email Generator Bot - Technical Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Class Hierarchy](#class-hierarchy)
3. [Core Components](#core-components)
4. [Data Flow](#data-flow)
5. [UI Components](#ui-components)
6. [Template System](#template-system)
7. [Extending the Application](#extending-the-application)
8. [Code Standards](#code-standards)
9. [Testing Guide](#testing-guide)

---

## Architecture Overview

### Design Philosophy
The Email Generator Bot follows these architectural principles:

1. **Separation of Concerns**: Clear boundaries between UI, logic, and data
2. **Modularity**: Each component is self-contained and reusable
3. **Simplicity**: No external dependencies beyond standard library
4. **Privacy-First**: No data persistence or network communication
5. **Deterministic**: Same input always produces same output

### Technology Stack
- **Language**: Python 3.7+
- **GUI Framework**: Tkinter (built-in)
- **Architecture**: Model-View-Controller (MVC)
- **Design Patterns**: Template Method, Factory, Observer

### System Requirements
```python
Python >= 3.7
tkinter (bundled with Python)
Standard Library:
  - typing (type hints)
  - datetime (timestamp generation)
  - json (potential future use)
  - os (file system operations)
```

---

## Class Hierarchy

### Class Diagram Overview

```
EmailGeneratorBot (Main Controller)
├── AnimatedWelcomeScreen
├── CategorySelectionScreen
├── FormScreen
├── PreviewScreen
└── Uses: EmailTemplateLibrary
    └── Returns: Dict[str, EmailTemplate]
        └── EmailTemplate (Data Class)
```

### Class Dependencies

```
EmailTemplate
  └── No dependencies

EmailTemplateLibrary
  └── Creates: EmailTemplate instances

AnimatedWelcomeScreen
  └── Depends on: tk.Frame, callback function

CategorySelectionScreen
  └── Depends on: tk.Frame, EmailTemplate dict, callback function

FormScreen
  └── Depends on: tk.Frame, EmailTemplate, callback functions
  └── Uses: scrolledtext, ttk widgets

PreviewScreen
  └── Depends on: tk.Frame, callback functions
  └── Uses: scrolledtext

EmailGeneratorBot
  └── Orchestrates all components
  └── Manages state and navigation
```

---

## Core Components

### 1. EmailTemplate Class

**Purpose**: Represents a single email template with its metadata

**Attributes**:
```python
name: str           # Display name of template
template: str       # Email text with {placeholders}
fields: List[Dict]  # Field definitions for form
```

**Methods**:
```python
def generate(self, values: Dict[str, str]) -> str:
    """
    Generates email by replacing placeholders with user values.
    
    Args:
        values: Dictionary mapping field names to user inputs
        
    Returns:
        Complete email text with substitutions made
        
    Example:
        template = "Dear {name}, ..."
        values = {"name": "John"}
        result = "Dear John, ..."
    """
```

**Field Definition Structure**:
```python
{
    "name": str,          # Internal field identifier
    "label": str,         # Display label for user
    "type": str,          # "text", "textarea", or "select"
    "placeholder": str,   # Helper text for user
    "options": List[str]  # Only for "select" type
}
```

---

### 2. EmailTemplateLibrary Class

**Purpose**: Central repository for all email templates

**Methods**:
```python
@staticmethod
def get_templates() -> Dict[str, EmailTemplate]:
    """
    Returns all available email templates.
    
    Returns:
        Dictionary mapping template IDs to EmailTemplate objects
        
    Template IDs:
        - job_application
        - leave_request
        - apology
        - internship_request
        - formal_communication
    """
```

**Adding New Templates**:
```python
def get_templates() -> Dict[str, EmailTemplate]:
    return {
        "template_id": EmailTemplate(
            name="Display Name",
            template="Email text with {placeholders}",
            fields=[
                {
                    "name": "placeholder",
                    "label": "User Label",
                    "type": "text",
                    "placeholder": "Helper text"
                }
            ]
        )
    }
```

---

### 3. AnimatedWelcomeScreen Class

**Purpose**: Initial welcome screen with animation

**Constructor**:
```python
def __init__(self, parent, on_complete):
    """
    Args:
        parent: Parent tkinter widget
        on_complete: Callback function when animation completes
    """
```

**Key Methods**:
```python
def show(self):
    """Display the welcome screen and start animation"""
    
def hide(self):
    """Remove welcome screen from view"""
    
def animate_fade_in(self):
    """Trigger animation sequence (2 second delay)"""
```

**UI Elements**:
- Title label (36pt bold)
- Subtitle label
- Feature list (4 items)
- Loading indicator

---

### 4. CategorySelectionScreen Class

**Purpose**: Display and handle email category selection

**Constructor**:
```python
def __init__(self, parent, templates: Dict[str, EmailTemplate], on_select):
    """
    Args:
        parent: Parent tkinter widget
        templates: Dictionary of available templates
        on_select: Callback function when category is selected
    """
```

**Key Methods**:
```python
def show(self):
    """Display the category selection screen"""
    
def hide(self):
    """Remove category screen from view"""
```

**UI Layout**:
```
+---------------------------------------------+
|           Select Email Category             |
|    Choose the type of email you want...     |
|                                             |
|  [Card 1]    [Card 2]    [Card 3]          |
|                                             |
|  [Card 4]    [Card 5]                       |
+---------------------------------------------+
```

**Category Card Structure**:
- Icon (48pt emoji)
- Template name (14pt bold)
- Description (10pt)
- Hover effect
- Click handler

---

### 5. FormScreen Class

**Purpose**: Dynamic form generation and input collection

**Constructor**:
```python
def __init__(self, parent, template: EmailTemplate, on_generate, on_back):
    """
    Args:
        parent: Parent tkinter widget
        template: EmailTemplate to generate form for
        on_generate: Callback when form is submitted
        on_back: Callback for back button
    """
```

**Key Methods**:
```python
def show(self):
    """Display the form screen"""
    
def hide(self):
    """Remove form screen from view"""
    
def collect_values(self) -> Dict[str, str]:
    """
    Collect all form field values.
    
    Returns:
        Dictionary mapping field names to user inputs
    """
    
def clear_placeholder(self, widget, placeholder):
    """
    Clear placeholder text when user focuses field.
    
    Args:
        widget: The input widget
        placeholder: The placeholder text to check against
    """
    
def handle_generate(self):
    """
    Validate and submit form.
    Shows warning if required fields are empty.
    Calls on_generate callback with collected values.
    """
```

**Field Widget Creation**:
```python
# Text field
tk.Entry(
    font=("Segoe UI", 10),
    bg="#1a1a2e",
    fg="#ffffff",
    insertbackground="#00d9ff",
    relief="flat"
)

# Textarea
scrolledtext.ScrolledText(
    height=4,
    font=("Segoe UI", 10),
    bg="#1a1a2e",
    fg="#ffffff",
    insertbackground="#00d9ff"
)

# Select dropdown
ttk.Combobox(
    values=options,
    font=("Segoe UI", 10),
    state="readonly"
)
```

**Scrolling Implementation**:
- Canvas widget for scrollable area
- Scrollbar for navigation
- Dynamic height calculation
- Mouse wheel support

---

### 6. PreviewScreen Class

**Purpose**: Display generated email and provide export options

**Constructor**:
```python
def __init__(self, parent, on_back, on_new):
    """
    Args:
        parent: Parent tkinter widget
        on_back: Callback for back button
        on_new: Callback for new email button
    """
```

**Key Methods**:
```python
def show(self):
    """Display the preview screen"""
    
def hide(self):
    """Remove preview screen from view"""
    
def set_content(self, content: str):
    """
    Set the email content to display.
    
    Args:
        content: Generated email text
    """
    
def copy_to_clipboard(self):
    """
    Copy email content to system clipboard.
    Shows success message box.
    """
```

**UI Elements**:
- Header with back button
- ScrolledText widget (read-only)
- Copy to clipboard button
- Generate new email button

---

### 7. EmailGeneratorBot Class (Main Controller)

**Purpose**: Orchestrate application flow and state management

**Constructor**:
```python
def __init__(self):
    """
    Initialize main application:
    - Create root window
    - Load templates
    - Initialize all screens
    - Show welcome screen
    """
```

**Key Methods**:
```python
def show_category_selection(self):
    """Navigate to category selection screen"""
    
def show_form(self, template_id: str):
    """
    Navigate to form screen for given template.
    
    Args:
        template_id: ID of template to show form for
    """
    
def generate_email(self, values: Dict[str, str]):
    """
    Generate email from template and values.
    Navigate to preview screen.
    
    Args:
        values: User input values from form
    """
    
def show_preview(self, content: str):
    """
    Navigate to preview screen with content.
    
    Args:
        content: Generated email content
    """
    
def back_to_form(self):
    """Navigate back to form from preview"""
    
def on_closing(self):
    """Handle window close event"""
    
def run(self):
    """Start the application main loop"""
```

**State Management**:
```python
self.templates: Dict[str, EmailTemplate]  # All available templates
self.current_template: Optional[EmailTemplate]  # Currently selected
self.current_template_id: Optional[str]  # ID of current template
self.form_screen: Optional[FormScreen]  # Current form instance
```

---

## Data Flow

### Email Generation Flow

```
User Input → Form Collection → Template Processing → Email Output
```

**Detailed Steps**:

1. **User Selection**:
   ```python
   User clicks category → on_select(template_id) called
   ```

2. **Form Display**:
   ```python
   template = templates[template_id]
   form_screen = FormScreen(template)
   form_screen.show()
   ```

3. **Input Collection**:
   ```python
   user clicks "Generate" → handle_generate() called
   values = collect_values()  # Returns Dict[str, str]
   ```

4. **Validation**:
   ```python
   empty_fields = [name for name, value in values.items() if not value]
   if empty_fields:
       show_warning()
       return
   ```

5. **Generation**:
   ```python
   email_content = template.generate(values)
   # Replaces {placeholder} with values[placeholder]
   ```

6. **Display**:
   ```python
   preview_screen.set_content(email_content)
   preview_screen.show()
   ```

7. **Export**:
   ```python
   clipboard.append(email_content)
   show_success_message()
   ```

### Navigation Flow

```
Welcome (2s) → Category → Form → Preview
                  ↑         ↑       ↓
                  └─────────┴───────┘
```

**State Transitions**:

| Current Screen | Action | Next Screen |
|----------------|--------|-------------|
| Welcome | Auto (2s) | Category |
| Category | Select Template | Form |
| Form | Generate | Preview |
| Form | Back | Category |
| Preview | Back | Form |
| Preview | New Email | Category |

---

## UI Components

### Color Scheme

```python
# Dark theme colors
BACKGROUND_PRIMARY = "#0f1419"    # Main background
BACKGROUND_SECONDARY = "#1a1a2e"  # Input backgrounds
BACKGROUND_TERTIARY = "#16213e"   # Button backgrounds

# Text colors
TEXT_PRIMARY = "#ffffff"          # Main text
TEXT_SECONDARY = "#a8a8a8"        # Subtitle text
TEXT_ACCENT = "#00d9ff"           # Accent color (cyan)
TEXT_BLACK = "#000000"            # Button text

# Interactive states
HOVER_COLOR = "#1e2a47"           # Hover state
ACTIVE_COLOR = "#00b8d4"          # Active state
```

### Font System

```python
# Font specifications
TITLE_FONT = ("Segoe UI", 36, "bold")
SUBTITLE_FONT = ("Segoe UI", 14)
HEADER_FONT = ("Segoe UI", 28, "bold")
SUBHEADER_FONT = ("Segoe UI", 24, "bold")
LABEL_FONT = ("Segoe UI", 11, "bold")
INPUT_FONT = ("Segoe UI", 10)
BUTTON_FONT = ("Segoe UI", 12, "bold")
BUTTON_LARGE_FONT = ("Segoe UI", 13, "bold")
MONOSPACE_FONT = ("Consolas", 10)
```

### Widget Styling

**Standard Button**:
```python
tk.Button(
    text="Button Text",
    font=("Segoe UI", 12, "bold"),
    bg="#16213e",           # Background
    fg="#00d9ff",           # Text color
    activebackground="#1e2a47",  # Hover background
    activeforeground="#00d9ff",  # Hover text
    relief="flat",          # No 3D effect
    padx=20,                # Horizontal padding
    pady=8,                 # Vertical padding
    cursor="hand2"          # Cursor style
)
```

**Primary Button**:
```python
tk.Button(
    text="Primary Action",
    font=("Segoe UI", 13, "bold"),
    bg="#00d9ff",           # Accent background
    fg="#000000",           # Dark text
    activebackground="#00b8d4",
    activeforeground="#000000",
    relief="flat",
    padx=40,
    pady=12,
    cursor="hand2"
)
```

**Input Field**:
```python
tk.Entry(
    font=("Segoe UI", 10),
    bg="#1a1a2e",
    fg="#ffffff",
    insertbackground="#00d9ff",  # Cursor color
    relief="flat",
    highlightthickness=1,
    highlightbackground="#16213e"
)
```

---

## Template System

### Template Structure

```python
template = """Subject: {subject}

Dear {recipient},

{body}

Best regards,
{sender}"""
```

### Placeholder Syntax

- **Simple**: `{field_name}`
- **Case-sensitive**: Must match field name exactly
- **No nesting**: Cannot have `{{nested}}`
- **No formatting**: Plain text replacement only

### Field Types Reference

#### 1. Text Field
```python
{
    "name": "field_name",
    "label": "Display Label",
    "type": "text",
    "placeholder": "Example: John Smith"
}
```
**Rendered as**: Single-line `tk.Entry` widget

#### 2. Textarea Field
```python
{
    "name": "field_name",
    "label": "Display Label",
    "type": "textarea",
    "placeholder": "Enter detailed information..."
}
```
**Rendered as**: Multi-line `scrolledtext.ScrolledText` widget (4 rows)

#### 3. Select Field
```python
{
    "name": "field_name",
    "label": "Display Label",
    "type": "select",
    "options": ["Option 1", "Option 2", "Option 3"]
}
```
**Rendered as**: Dropdown `ttk.Combobox` widget (readonly)

### Template Best Practices

1. **Clear Placeholders**: Use descriptive names like `{company_name}` not `{cn}`
2. **Consistent Format**: Follow email conventions (Subject, Dear, Body, Signature)
3. **Optional Fields**: Include but make them clearly optional in label
4. **Field Order**: Order fields logically (recipient info first, sender info last)
5. **Placeholder Text**: Provide helpful examples in placeholder attribute

### Example Template Definition

```python
"custom_template": EmailTemplate(
    name="Meeting Request",
    template="""Subject: Meeting Request - {meeting_topic}

Dear {recipient_name},

I hope this email finds you well. I am writing to request a meeting to discuss {meeting_topic}.

Proposed details:
- Date: {proposed_date}
- Time: {proposed_time}
- Duration: {duration}
- Location: {location}

Agenda:
{agenda_items}

Please let me know if this works for you or suggest an alternative time.

Thank you for your consideration.

Best regards,
{sender_name}
{sender_title}
{sender_email}""",
    fields=[
        {"name": "recipient_name", "label": "Recipient Name", 
         "type": "text", "placeholder": "e.g., Dr. Smith"},
        {"name": "meeting_topic", "label": "Meeting Topic", 
         "type": "text", "placeholder": "e.g., Q4 Strategy Review"},
        {"name": "proposed_date", "label": "Proposed Date", 
         "type": "text", "placeholder": "e.g., January 15, 2025"},
        {"name": "proposed_time", "label": "Proposed Time", 
         "type": "text", "placeholder": "e.g., 2:00 PM"},
        {"name": "duration", "label": "Duration", 
         "type": "select", "options": ["30 minutes", "1 hour", "2 hours"]},
        {"name": "location", "label": "Location", 
         "type": "text", "placeholder": "e.g., Conference Room A / Zoom"},
        {"name": "agenda_items", "label": "Agenda Items", 
         "type": "textarea", "placeholder": "List the topics to discuss"},
        {"name": "sender_name", "label": "Your Name", 
         "type": "text", "placeholder": "e.g., John Smith"},
        {"name": "sender_title", "label": "Your Title", 
         "type": "text", "placeholder": "e.g., Project Manager"},
        {"name": "sender_email", "label": "Your Email", 
         "type": "text", "placeholder": "e.g., john.smith@company.com"}
    ]
)
```

---

## Extending the Application

### Adding a New Email Template

**Step 1**: Define your template in `EmailTemplateLibrary.get_templates()`:

```python
@staticmethod
def get_templates() -> Dict[str, EmailTemplate]:
    return {
        # ... existing templates ...
        
        "new_template": EmailTemplate(
            name="Your Template Name",
            template="""Your email template with {placeholders}""",
            fields=[
                # Your field definitions
            ]
        )
    }
```

**Step 2**: Add category information in `CategorySelectionScreen.__init__()`:

```python
category_info = {
    # ... existing categories ...
    
    "new_template": {
        "icon": "📧",  # Choose an emoji
        "description": "Brief description"
    }
}
```

**Step 3**: Test your template:
1. Run the application
2. Select your new category
3. Fill in the form
4. Verify generated email

### Adding Custom Field Validation

**Location**: `FormScreen.handle_generate()` method

**Example**: Email validation

```python
def validate_email(email: str) -> bool:
    """Simple email validation"""
    return "@" in email and "." in email.split("@")[1]

def handle_generate(self):
    values = self.collect_values()
    
    # Custom validation
    if "sender_email" in values:
        if not validate_email(values["sender_email"]):
            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid email address"
            )
            return
    
    # ... rest of method ...
```

### Adding New Field Types

**Step 1**: Define field type in template:

```python
{
    "name": "field_name",
    "label": "Field Label",
    "type": "custom_type",
    "options": {}  # Custom options
}
```

**Step 2**: Add handler in `FormScreen.__init__()`:

```python
# In field creation loop
if field["type"] == "custom_type":
    widget = YourCustomWidget(
        field_frame,
        # ... widget configuration ...
    )
    widget.pack(fill="x")
```

**Step 3**: Update `collect_values()` method:

```python
def collect_values(self) -> Dict[str, str]:
    values = {}
    for field_name, field_info in self.field_widgets.items():
        widget = field_info["widget"]
        field_type = field_info["type"]
        
        if field_type == "custom_type":
            value = widget.get_custom_value()  # Your custom method
        # ... existing handlers ...
        
        values[field_name] = value
    return values
```

### Customizing UI Theme

**Create a theme configuration**:

```python
class Theme:
    """Application theme configuration"""
    
    # Colors
    BG_PRIMARY = "#0f1419"
    BG_SECONDARY = "#1a1a2e"
    TEXT_PRIMARY = "#ffffff"
    ACCENT = "#00d9ff"
    
    # Fonts
    TITLE = ("Segoe UI", 36, "bold")
    BODY = ("Segoe UI", 10)
    
    @classmethod
    def apply_to_widget(cls, widget, style="default"):
        """Apply theme to widget"""
        if style == "button":
            widget.config(
                bg=cls.ACCENT,
                fg="#000000",
                font=cls.BODY
            )
        # ... more styles ...
```

**Use in code**:

```python
button = tk.Button(parent, text="Click Me")
Theme.apply_to_widget(button, "button")
```

---

## Code Standards

### Style Guide

Follow PEP 8 with these specifics:

**Imports**:
```python
# Standard library imports
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Optional
import json
from datetime import datetime
import os

# No relative imports needed (single-file application)
```

**Naming Conventions**:
```python
# Classes: PascalCase
class EmailTemplate:
    pass

# Functions/methods: snake_case
def generate_email():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_FIELD_LENGTH = 200

# Private methods: _leading_underscore
def _internal_helper():
    pass
```

**Type Hints**:
```python
def generate_email(
    template: EmailTemplate,
    values: Dict[str, str]
) -> str:
    """Always use type hints for clarity"""
    pass
```

**Docstrings**:
```python
def method_name(arg1: str, arg2: int) -> bool:
    """
    Brief description of what the method does.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When input is invalid
        
    Example:
        >>> method_name("test", 42)
        True
    """
    pass
```

### Error Handling

**User Input Errors**:
```python
try:
    # Process user input
    values = self.collect_values()
    if not validate(values):
        raise ValueError("Invalid input")
except ValueError as e:
    messagebox.showwarning("Invalid Input", str(e))
    return
```

**System Errors**:
```python
try:
    # System operation
    clipboard.append(content)
except Exception as e:
    messagebox.showerror(
        "Error",
        f"An error occurred: {str(e)}"
    )
```

### Best Practices

1. **Single Responsibility**: Each class has one clear purpose
2. **DRY Principle**: Don't repeat code, create helper methods
3. **Type Safety**: Use type hints for all function signatures
4. **Documentation**: Document complex logic with comments
5. **Error Messages**: Make them helpful and actionable
6. **User Feedback**: Always acknowledge user actions
7. **Performance**: Avoid unnecessary computations
8. **Memory**: Clean up resources when done

---

## Testing Guide

### Manual Testing Checklist

**Welcome Screen**:
- [ ] Appears on startup
- [ ] Animation displays correctly
- [ ] Transitions after ~2 seconds
- [ ] All text is readable

**Category Selection**:
- [ ] All 5 categories display
- [ ] Cards are properly aligned
- [ ] Hover effects work
- [ ] Click navigates to form
- [ ] Icons display correctly

**Form Screen**:
- [ ] Back button works
- [ ] All fields render correctly
- [ ] Placeholders appear
- [ ] Placeholders clear on focus
- [ ] Scrolling works if needed
- [ ] Validation shows warnings
- [ ] Generate button works

**Preview Screen**:
- [ ] Email displays correctly
- [ ] Copy button works
- [ ] Clipboard contains full email
- [ ] Success message appears
- [ ] New email button works
- [ ] Back button works

**Each Template**:
- [ ] All placeholders replaced
- [ ] Formatting is correct
- [ ] No missing values
- [ ] Output is professional

### Unit Testing Example

```python
import unittest

class TestEmailTemplate(unittest.TestCase):
    def setUp(self):
        self.template = EmailTemplate(
            name="Test",
            template="Dear {name}, {message}",
            fields=[
                {"name": "name", "label": "Name", "type": "text"},
                {"name": "message", "label": "Message", "type": "text"}
            ]
        )
    
    def test_generate_simple(self):
        values = {"name": "John", "message": "Hello"}
        result = self.template.generate(values)
        self.assertEqual(result, "Dear John, Hello")
    
    def test_generate_missing_placeholder(self):
        values = {"name": "John"}
        result = self.template.generate(values)
        self.assertIn("{message}", result)  # Placeholder not replaced

if __name__ == "__main__":
    unittest.main()
```

### Integration Testing

**Test Scenario**: Complete email generation flow

```python
def test_full_workflow():
    """Test complete user journey"""
    # 1. Start application
    app = EmailGeneratorBot()
    
    # 2. Skip welcome screen (simulated)
    app.show_category_selection()
    
    # 3. Select template
    app.show_form("job_application")
    
    # 4. Fill form (simulated)
    test_values = {
        "recipient_name": "Test Manager",
        "company_name": "Test Corp",
        # ... all required fields ...
    }
    
    # 5. Generate email
    email = app.current_template.generate(test_values)
    
    # 6. Verify output
    assert "Test Manager" in email
    assert "Test Corp" in email
    assert "{" not in email  # No unreplaced placeholders
    
    print("Integration test passed!")
```

---

## Performance Considerations

### Optimization Opportunities

1. **Template Loading**: Templates are loaded once at startup
2. **UI Rendering**: Screens are created once and hidden/shown
3. **Memory**: No persistent data means low memory footprint
4. **CPU**: Minimal processing (string replacement only)

### Benchmarks

Typical performance metrics:
- Startup: < 2 seconds
- Screen transition: < 100ms
- Email generation: < 10ms
- Clipboard copy: < 50ms

### Scalability

Current limitations and solutions:

| Aspect | Current | Scalable Solution |
|--------|---------|-------------------|
| Templates | Hardcoded | JSON/YAML file loading |
| Fields | 10-15 max | Dynamic scrolling (implemented) |
| Email size | Unlimited | No change needed |
| Users | Single | No multi-user support needed |

---

## Future Development

### Planned Features (Roadmap)

**Version 1.1**:
- Template import/export
- Configuration file
- User preferences storage

**Version 1.2**:
- Multi-language support
- Custom themes
- Keyboard shortcuts

**Version 2.0**:
- Template marketplace
- PDF export
- Email history (optional)

### Architecture for Extensions

**Plugin System** (Future):
```python
class TemplatePlugin:
    """Base class for template plugins"""
    
    def get_templates(self) -> Dict[str, EmailTemplate]:
        """Return plugin templates"""
        raise NotImplementedError
    
    def get_metadata(self) -> Dict:
        """Return plugin metadata"""
        return {
            "name": "Plugin Name",
            "version": "1.0.0",
            "author": "Author Name"
        }
```

---

**Document Version**: 1.0.0  
**Last Updated**: December 2025  
**Maintainer**: Development Team
