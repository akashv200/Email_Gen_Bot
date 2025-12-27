"""
Email Generator Bot - Template-Based Email Generator for Windows
A lightweight, privacy-focused desktop application for generating professional emails
without AI or internet connectivity.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime
from typing import Dict, List, Optional
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64


class GmailConfig:
    """Manages Gmail SMTP configuration and credentials"""
    
    CONFIG_FILE = "gmail_config.dat"
    
    @staticmethod
    def save_credentials(email: str, app_password: str):
        """Save Gmail credentials (encoded for basic obfuscation)"""
        data = {
            "email": base64.b64encode(email.encode()).decode(),
            "password": base64.b64encode(app_password.encode()).decode()
        }
        try:
            with open(GmailConfig.CONFIG_FILE, 'w') as f:
                json.dump(data, f)
            return True
        except Exception as e:
            print(f"Error saving credentials: {e}")
            return False
    
    @staticmethod
    def load_credentials() -> Optional[Dict[str, str]]:
        """Load saved Gmail credentials"""
        try:
            if os.path.exists(GmailConfig.CONFIG_FILE):
                with open(GmailConfig.CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                return {
                    "email": base64.b64decode(data["email"]).decode(),
                    "password": base64.b64decode(data["password"]).decode()
                }
        except Exception as e:
            print(f"Error loading credentials: {e}")
        return None
    
    @staticmethod
    def delete_credentials():
        """Delete saved credentials"""
        try:
            if os.path.exists(GmailConfig.CONFIG_FILE):
                os.remove(GmailConfig.CONFIG_FILE)
            return True
        except Exception as e:
            print(f"Error deleting credentials: {e}")
            return False


class EmailSender:
    """Handles email sending via Gmail SMTP"""
    
    @staticmethod
    def send_email(from_email: str, app_password: str, to_email: str, 
                   subject: str, body: str) -> tuple[bool, str]:
        """
        Send email using Gmail SMTP
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to Gmail SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            
            # Login
            server.login(from_email, app_password)
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            return True, "Email sent successfully!"
            
        except smtplib.SMTPAuthenticationError:
            return False, "Authentication failed. Please check your email and app password."
        except smtplib.SMTPException as e:
            return False, f"SMTP error: {str(e)}"
        except Exception as e:
            return False, f"Error sending email: {str(e)}"


class EmailTemplate:
    """Represents an email template with placeholders"""
    
    def __init__(self, name: str, template: str, fields: List[Dict]):
        self.name = name
        self.template = template
        self.fields = fields
    
    def generate(self, values: Dict[str, str]) -> str:
        """Generate email by replacing placeholders with values"""
        email = self.template
        for key, value in values.items():
            placeholder = f"{{{key}}}"
            email = email.replace(placeholder, value)
        return email


class EmailTemplateLibrary:
    """Manages all email templates"""
    
    @staticmethod
    def get_templates() -> Dict[str, EmailTemplate]:
        """Returns all available email templates"""
        return {
            "job_application": EmailTemplate(
                name="Job Application",
                template="""To: {recipient_email}
Subject: Application for {job_role} Position

Dear {recipient_name},

I am writing to express my strong interest in the {job_role} position at {company_name}. With my background in {field_of_expertise} and {years_experience} years of relevant experience, I believe I would be a valuable addition to your team.

{additional_message}

I have attached my resume for your review, which provides detailed information about my qualifications and achievements. I am particularly drawn to {company_name} because of {reason_for_interest}.

I am available for an interview at your convenience and would welcome the opportunity to discuss how my skills and experience align with your needs. Thank you for considering my application.

I look forward to hearing from you.

Best regards,
{sender_name}""",
                fields=[
                    {"name": "recipient_email", "label": "To: (Recipient Email)", "type": "text", "placeholder": "e.g., hr@techcorp.com"},
                    {"name": "recipient_name", "label": "Recipient Name", "type": "text", "placeholder": "e.g., Hiring Manager"},
                    {"name": "company_name", "label": "Company Name", "type": "text", "placeholder": "e.g., Tech Corp"},
                    {"name": "job_role", "label": "Job Role", "type": "text", "placeholder": "e.g., Software Engineer"},
                    {"name": "field_of_expertise", "label": "Field of Expertise", "type": "text", "placeholder": "e.g., software development"},
                    {"name": "years_experience", "label": "Years of Experience", "type": "text", "placeholder": "e.g., 3"},
                    {"name": "reason_for_interest", "label": "Reason for Interest", "type": "text", "placeholder": "e.g., your innovative approach to AI"},
                    {"name": "additional_message", "label": "Additional Message (Optional)", "type": "textarea", "placeholder": "Any additional information you'd like to include"},
                    {"name": "sender_name", "label": "Your Name", "type": "text", "placeholder": "e.g., John Smith"}
                ]
            ),
            
            "leave_request": EmailTemplate(
                name="Leave Request",
                template="""To: {recipient_email}
Subject: Leave Request - {leave_type}

Dear {recipient_name},

I am writing to formally request {leave_type} leave from {start_date} to {end_date} ({total_days} days).

Reason for leave:
{reason}

I have ensured that all my current responsibilities are up to date, and I have made arrangements for {coverage_person} to handle any urgent matters during my absence. {handover_notes}

I will be available via {contact_method} in case of any emergencies.

Thank you for considering my request. I look forward to your approval.

Best regards,
{sender_name}
{sender_position}""",
                fields=[
                    {"name": "recipient_email", "label": "To: (Recipient Email)", "type": "text", "placeholder": "e.g., manager@company.com"},
                    {"name": "recipient_name", "label": "Recipient Name", "type": "text", "placeholder": "e.g., Manager Name"},
                    {"name": "leave_type", "label": "Leave Type", "type": "select", "options": ["Annual", "Sick", "Personal", "Unpaid", "Emergency"]},
                    {"name": "start_date", "label": "Start Date", "type": "text", "placeholder": "e.g., January 15, 2025"},
                    {"name": "end_date", "label": "End Date", "type": "text", "placeholder": "e.g., January 20, 2025"},
                    {"name": "total_days", "label": "Total Days", "type": "text", "placeholder": "e.g., 5"},
                    {"name": "reason", "label": "Reason for Leave", "type": "textarea", "placeholder": "Briefly explain your reason"},
                    {"name": "coverage_person", "label": "Coverage Person", "type": "text", "placeholder": "e.g., Jane Doe"},
                    {"name": "handover_notes", "label": "Handover Notes (Optional)", "type": "textarea", "placeholder": "Any additional handover information"},
                    {"name": "contact_method", "label": "Emergency Contact Method", "type": "text", "placeholder": "e.g., phone or email"},
                    {"name": "sender_name", "label": "Your Name", "type": "text", "placeholder": "e.g., John Smith"},
                    {"name": "sender_position", "label": "Your Position", "type": "text", "placeholder": "e.g., Software Engineer"}
                ]
            ),
            
            "apology": EmailTemplate(
                name="Professional Apology",
                template="""To: {recipient_email}
Subject: Sincere Apology - {apology_subject}

Dear {recipient_name},

I am writing to sincerely apologize for {incident_description}. I understand that this has caused {impact_description}, and I take full responsibility for my actions.

{explanation}

To prevent this from happening again, I have taken the following steps:
{corrective_actions}

I value our {relationship_type} relationship and am committed to ensuring this does not affect our future {relationship_context}. If there is anything more I can do to rectify this situation, please let me know.

Once again, I apologize for any inconvenience or disappointment this may have caused.

Sincerely,
{sender_name}
{sender_title}""",
                fields=[
                    {"name": "recipient_email", "label": "To: (Recipient Email)", "type": "text", "placeholder": "e.g., client@company.com"},
                    {"name": "recipient_name", "label": "Recipient Name", "type": "text", "placeholder": "e.g., Mr. Johnson"},
                    {"name": "apology_subject", "label": "Subject of Apology", "type": "text", "placeholder": "e.g., Missed Deadline"},
                    {"name": "incident_description", "label": "What Happened", "type": "textarea", "placeholder": "Describe the incident briefly"},
                    {"name": "impact_description", "label": "Impact/Consequence", "type": "text", "placeholder": "e.g., delays in the project timeline"},
                    {"name": "explanation", "label": "Brief Explanation (Optional)", "type": "textarea", "placeholder": "Context if appropriate (not an excuse)"},
                    {"name": "corrective_actions", "label": "Corrective Actions", "type": "textarea", "placeholder": "Steps you've taken to prevent recurrence"},
                    {"name": "relationship_type", "label": "Relationship Type", "type": "text", "placeholder": "e.g., professional, business"},
                    {"name": "relationship_context", "label": "Relationship Context", "type": "text", "placeholder": "e.g., collaboration, partnership"},
                    {"name": "sender_name", "label": "Your Name", "type": "text", "placeholder": "e.g., John Smith"},
                    {"name": "sender_title", "label": "Your Title/Position", "type": "text", "placeholder": "e.g., Project Manager"}
                ]
            ),
            
            "internship_request": EmailTemplate(
                name="Internship Request",
                template="""To: {recipient_email}
Subject: Internship Application - {internship_position}

Dear {recipient_name},

I am {sender_name}, currently pursuing {degree_program} at {university_name}, and I am writing to express my strong interest in securing an internship opportunity at {company_name} in the {department_name} department.

I am particularly interested in the {internship_position} role because {reason_for_interest}. My academic background in {academic_focus} and coursework in {relevant_courses} has equipped me with foundational knowledge that I am eager to apply in a professional setting.

{skills_and_experience}

I am available to intern for {duration} starting from {start_date}. I am confident that this internship would provide valuable learning opportunities while allowing me to contribute meaningfully to your team.

I have attached my resume and {additional_documents} for your consideration. I would greatly appreciate the opportunity to discuss how I can contribute to {company_name}.

Thank you for your time and consideration.

Best regards,
{sender_name}
{university_name}""",
                fields=[
                    {"name": "recipient_email", "label": "To: (Recipient Email)", "type": "text", "placeholder": "e.g., internships@company.com"},
                    {"name": "recipient_name", "label": "Recipient Name", "type": "text", "placeholder": "e.g., Internship Coordinator"},
                    {"name": "company_name", "label": "Company Name", "type": "text", "placeholder": "e.g., Tech Innovations Inc."},
                    {"name": "department_name", "label": "Department", "type": "text", "placeholder": "e.g., Software Development"},
                    {"name": "internship_position", "label": "Internship Position", "type": "text", "placeholder": "e.g., Software Engineering Intern"},
                    {"name": "reason_for_interest", "label": "Reason for Interest", "type": "textarea", "placeholder": "Why this company/position interests you"},
                    {"name": "sender_name", "label": "Your Name", "type": "text", "placeholder": "e.g., Jane Smith"},
                    {"name": "degree_program", "label": "Degree Program", "type": "text", "placeholder": "e.g., Bachelor of Science in Computer Science"},
                    {"name": "university_name", "label": "University Name", "type": "text", "placeholder": "e.g., State University"},
                    {"name": "academic_focus", "label": "Academic Focus", "type": "text", "placeholder": "e.g., software engineering and data structures"},
                    {"name": "relevant_courses", "label": "Relevant Courses", "type": "text", "placeholder": "e.g., algorithms, databases, web development"},
                    {"name": "skills_and_experience", "label": "Skills and Experience", "type": "textarea", "placeholder": "Highlight your relevant skills and any projects"},
                    {"name": "duration", "label": "Internship Duration", "type": "text", "placeholder": "e.g., 3 months"},
                    {"name": "start_date", "label": "Preferred Start Date", "type": "text", "placeholder": "e.g., June 1, 2025"},
                    {"name": "additional_documents", "label": "Additional Documents", "type": "text", "placeholder": "e.g., academic transcript"}
                ]
            ),
            
            "formal_communication": EmailTemplate(
                name="General Formal Communication",
                template="""To: {recipient_email}
Subject: {email_subject}

Dear {recipient_name},

{opening_paragraph}

{main_content}

{closing_paragraph}

{call_to_action}

Thank you for your time and attention to this matter.

Best regards,
{sender_name}
{sender_title}
{sender_organization}""",
                fields=[
                    {"name": "recipient_email", "label": "To: (Recipient Email)", "type": "text", "placeholder": "e.g., contact@company.com"},
                    {"name": "recipient_name", "label": "Recipient Name", "type": "text", "placeholder": "e.g., Dr. Johnson"},
                    {"name": "email_subject", "label": "Email Subject", "type": "text", "placeholder": "Brief subject line"},
                    {"name": "opening_paragraph", "label": "Opening Paragraph", "type": "textarea", "placeholder": "Introduce the purpose of your email"},
                    {"name": "main_content", "label": "Main Content", "type": "textarea", "placeholder": "Detailed information or message body"},
                    {"name": "closing_paragraph", "label": "Closing Paragraph", "type": "textarea", "placeholder": "Summarize or conclude your message"},
                    {"name": "call_to_action", "label": "Call to Action (Optional)", "type": "textarea", "placeholder": "e.g., I look forward to your response by..."},
                    {"name": "sender_name", "label": "Your Name", "type": "text", "placeholder": "e.g., John Smith"},
                    {"name": "sender_title", "label": "Your Title", "type": "text", "placeholder": "e.g., Senior Consultant"},
                    {"name": "sender_organization", "label": "Your Organization", "type": "text", "placeholder": "e.g., ABC Consulting"}
                ]
            )
        }


class AnimatedWelcomeScreen:
    """Animated welcome screen with fade-in effect"""
    
    def __init__(self, parent, on_complete):
        self.parent = parent
        self.on_complete = on_complete
        self.frame = tk.Frame(parent, bg="#1a1a2e")
        self.alpha = 0.0
        
        # Title
        self.title = tk.Label(
            self.frame,
            text="Email Generator Bot",
            font=("Segoe UI", 36, "bold"),
            fg="#00d9ff",
            bg="#1a1a2e"
        )
        self.title.pack(pady=(150, 20))
        
        # Subtitle
        self.subtitle = tk.Label(
            self.frame,
            text="Template-Based Professional Email Generator",
            font=("Segoe UI", 14),
            fg="#a8a8a8",
            bg="#1a1a2e"
        )
        self.subtitle.pack(pady=(0, 40))
        
        # Feature highlights
        features = [
            "✓ No AI Required",
            "✓ Works Offline",
            "✓ Privacy Focused",
            "✓ Instant Generation"
        ]
        
        for feature in features:
            label = tk.Label(
                self.frame,
                text=feature,
                font=("Segoe UI", 12),
                fg="#ffffff",
                bg="#1a1a2e"
            )
            label.pack(pady=5)
        
        # Loading message
        self.loading = tk.Label(
            self.frame,
            text="Loading...",
            font=("Segoe UI", 11, "italic"),
            fg="#00d9ff",
            bg="#1a1a2e"
        )
        self.loading.pack(pady=(60, 0))
        
    def show(self):
        """Display the welcome screen with animation"""
        self.frame.pack(fill="both", expand=True)
        self.animate_fade_in()
        
    def animate_fade_in(self):
        """Animate fade-in effect and transition to main screen"""
        self.parent.after(2000, self.on_complete)
        
    def hide(self):
        """Hide the welcome screen"""
        self.frame.pack_forget()


class CategorySelectionScreen:
    """Screen for selecting email category"""
    
    def __init__(self, parent, templates: Dict[str, EmailTemplate], on_select):
        self.parent = parent
        self.templates = templates
        self.on_select = on_select
        self.frame = tk.Frame(parent, bg="#0f1419")
        
        # Header
        header = tk.Label(
            self.frame,
            text="Select Email Category",
            font=("Segoe UI", 28, "bold"),
            fg="#00d9ff",
            bg="#0f1419"
        )
        header.pack(pady=(40, 10))
        
        # Subtitle
        subtitle = tk.Label(
            self.frame,
            text="Choose the type of email you want to generate",
            font=("Segoe UI", 12),
            fg="#a8a8a8",
            bg="#0f1419"
        )
        subtitle.pack(pady=(0, 40))
        
        # Category buttons container
        button_container = tk.Frame(self.frame, bg="#0f1419")
        button_container.pack(expand=True)
        
        # Category information
        category_info = {
            "job_application": {
                "icon": "💼",
                "description": "Apply for job positions"
            },
            "leave_request": {
                "icon": "📅",
                "description": "Request time off from work"
            },
            "apology": {
                "icon": "🙏",
                "description": "Send professional apologies"
            },
            "internship_request": {
                "icon": "🎓",
                "description": "Request internship opportunities"
            },
            "formal_communication": {
                "icon": "✉️",
                "description": "General formal emails"
            }
        }
        
        # Create category buttons
        row = 0
        col = 0
        for template_id, template in templates.items():
            info = category_info.get(template_id, {"icon": "📧", "description": ""})
            
            btn_frame = tk.Frame(button_container, bg="#16213e", relief="flat", bd=0)
            btn_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            # Make button clickable
            btn_frame.bind("<Button-1>", lambda e, tid=template_id: self.on_select(tid))
            btn_frame.bind("<Enter>", lambda e, f=btn_frame: f.config(bg="#1e2a47"))
            btn_frame.bind("<Leave>", lambda e, f=btn_frame: f.config(bg="#16213e"))
            
            # Icon
            icon_label = tk.Label(
                btn_frame,
                text=info["icon"],
                font=("Segoe UI", 48),
                bg="#16213e",
                cursor="hand2"
            )
            icon_label.pack(pady=(20, 10))
            icon_label.bind("<Button-1>", lambda e, tid=template_id: self.on_select(tid))
            
            # Template name
            name_label = tk.Label(
                btn_frame,
                text=template.name,
                font=("Segoe UI", 14, "bold"),
                fg="#00d9ff",
                bg="#16213e",
                cursor="hand2"
            )
            name_label.pack(pady=(0, 5))
            name_label.bind("<Button-1>", lambda e, tid=template_id: self.on_select(tid))
            
            # Description
            desc_label = tk.Label(
                btn_frame,
                text=info["description"],
                font=("Segoe UI", 10),
                fg="#a8a8a8",
                bg="#16213e",
                cursor="hand2",
                wraplength=200
            )
            desc_label.pack(pady=(0, 20))
            desc_label.bind("<Button-1>", lambda e, tid=template_id: self.on_select(tid))
            
            col += 1
            if col > 2:
                col = 0
                row += 1
        
    def show(self):
        """Display the category selection screen"""
        self.frame.pack(fill="both", expand=True)
        
    def hide(self):
        """Hide the category selection screen"""
        self.frame.pack_forget()


class FormScreen:
    """Dynamic form screen for collecting user input"""
    
    def __init__(self, parent, template: EmailTemplate, on_generate, on_back):
        self.parent = parent
        self.template = template
        self.on_generate = on_generate
        self.on_back = on_back
        self.frame = tk.Frame(parent, bg="#0f1419")
        self.field_widgets = {}
        
        # Header with back button
        header_frame = tk.Frame(self.frame, bg="#0f1419")
        header_frame.pack(fill="x", pady=(20, 10))
        
        back_btn = tk.Button(
            header_frame,
            text="← Back",
            font=("Segoe UI", 11),
            bg="#16213e",
            fg="#00d9ff",
            activebackground="#1e2a47",
            activeforeground="#00d9ff",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.on_back
        )
        back_btn.pack(side="left", padx=20)
        
        # Title
        title = tk.Label(
            self.frame,
            text=f"{template.name} - Fill Details",
            font=("Segoe UI", 24, "bold"),
            fg="#00d9ff",
            bg="#0f1419"
        )
        title.pack(pady=(0, 30))
        
        # Scrollable form container
        canvas_frame = tk.Frame(self.frame, bg="#0f1419")
        canvas_frame.pack(fill="both", expand=True, padx=20)
        
        canvas = tk.Canvas(canvas_frame, bg="#0f1419", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0f1419")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create form fields
        for field in template.fields:
            field_frame = tk.Frame(scrollable_frame, bg="#0f1419")
            field_frame.pack(fill="x", pady=10, padx=40)
            
            # Label
            label = tk.Label(
                field_frame,
                text=field["label"],
                font=("Segoe UI", 11, "bold"),
                fg="#ffffff",
                bg="#0f1419",
                anchor="w"
            )
            label.pack(anchor="w", pady=(0, 5))
            
            # Input widget based on type
            if field["type"] == "select":
                widget = ttk.Combobox(
                    field_frame,
                    values=field["options"],
                    font=("Segoe UI", 10),
                    state="readonly"
                )
                widget.set(field["options"][0])
                widget.pack(fill="x")
            elif field["type"] == "textarea":
                widget = scrolledtext.ScrolledText(
                    field_frame,
                    height=4,
                    font=("Segoe UI", 10),
                    bg="#1a1a2e",
                    fg="#ffffff",
                    insertbackground="#00d9ff",
                    relief="flat",
                    padx=10,
                    pady=10
                )
                widget.insert("1.0", field.get("placeholder", ""))
                widget.bind("<FocusIn>", lambda e, w=widget, p=field.get("placeholder", ""): 
                           self.clear_placeholder(w, p))
                widget.pack(fill="x")
            else:  # text
                widget = tk.Entry(
                    field_frame,
                    font=("Segoe UI", 10),
                    bg="#1a1a2e",
                    fg="#ffffff",
                    insertbackground="#00d9ff",
                    relief="flat"
                )
                widget.insert(0, field.get("placeholder", ""))
                widget.bind("<FocusIn>", lambda e, w=widget, p=field.get("placeholder", ""): 
                           self.clear_placeholder(w, p))
                widget.config({"highlightthickness": 1, "highlightbackground": "#16213e"})
                widget.pack(fill="x", ipady=8, padx=2)
            
            self.field_widgets[field["name"]] = {
                "widget": widget,
                "type": field["type"],
                "placeholder": field.get("placeholder", "")
            }
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Generate button
        btn_frame = tk.Frame(self.frame, bg="#0f1419")
        btn_frame.pack(pady=20)
        
        generate_btn = tk.Button(
            btn_frame,
            text="Generate Email",
            font=("Segoe UI", 13, "bold"),
            bg="#00d9ff",
            fg="#000000",
            activebackground="#00b8d4",
            activeforeground="#000000",
            relief="flat",
            padx=40,
            pady=12,
            cursor="hand2",
            command=self.handle_generate
        )
        generate_btn.pack()
        
    def clear_placeholder(self, widget, placeholder):
        """Clear placeholder text on focus"""
        if isinstance(widget, scrolledtext.ScrolledText):
            if widget.get("1.0", "end-1c") == placeholder:
                widget.delete("1.0", "end")
                widget.config(fg="#ffffff")
        else:
            if widget.get() == placeholder:
                widget.delete(0, "end")
                widget.config(fg="#ffffff")
    
    def collect_values(self) -> Dict[str, str]:
        """Collect all form values"""
        values = {}
        for field_name, field_info in self.field_widgets.items():
            widget = field_info["widget"]
            field_type = field_info["type"]
            placeholder = field_info["placeholder"]
            
            if field_type == "textarea":
                value = widget.get("1.0", "end-1c").strip()
                if value == placeholder:
                    value = ""
            elif field_type == "select":
                value = widget.get()
            else:
                value = widget.get().strip()
                if value == placeholder:
                    value = ""
            
            values[field_name] = value
        
        return values
    
    def handle_generate(self):
        """Handle generate button click"""
        values = self.collect_values()
        
        # Validate required fields (simple check)
        empty_fields = [name for name, value in values.items() if not value]
        if empty_fields:
            messagebox.showwarning(
                "Missing Information",
                f"Please fill in all required fields to generate the email."
            )
            return
        
        self.on_generate(values)
    
    def show(self):
        """Display the form screen"""
        self.frame.pack(fill="both", expand=True)
        
    def hide(self):
        """Hide the form screen"""
        self.frame.pack_forget()


class PreviewScreen:
    """Email preview and export screen"""
    
    def __init__(self, parent, on_back, on_new, on_settings):
        self.parent = parent
        self.on_back = on_back
        self.on_new = on_new
        self.on_settings = on_settings
        self.frame = tk.Frame(parent, bg="#0f1419")
        self.email_content = ""
        self.recipient_email = ""
        
        # Header
        header_frame = tk.Frame(self.frame, bg="#0f1419")
        header_frame.pack(fill="x", pady=(20, 10))
        
        back_btn = tk.Button(
            header_frame,
            text="← Back",
            font=("Segoe UI", 11),
            bg="#16213e",
            fg="#00d9ff",
            activebackground="#1e2a47",
            activeforeground="#00d9ff",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.on_back
        )
        back_btn.pack(side="left", padx=20)
        
        title = tk.Label(
            header_frame,
            text="Email Preview",
            font=("Segoe UI", 24, "bold"),
            fg="#00d9ff",
            bg="#0f1419"
        )
        title.pack(side="left", padx=20)
        
        # Settings button
        settings_btn = tk.Button(
            header_frame,
            text="⚙️ Gmail Setup",
            font=("Segoe UI", 10),
            bg="#16213e",
            fg="#a8a8a8",
            activebackground="#1e2a47",
            activeforeground="#00d9ff",
            relief="flat",
            padx=15,
            pady=6,
            cursor="hand2",
            command=self.on_settings
        )
        settings_btn.pack(side="right", padx=20)
        
        # Preview area
        preview_frame = tk.Frame(self.frame, bg="#0f1419")
        preview_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            font=("Consolas", 10),
            bg="#1a1a2e",
            fg="#ffffff",
            relief="flat",
            padx=20,
            pady=20,
            wrap="word",
            state="disabled"
        )
        self.preview_text.pack(fill="both", expand=True)
        
        # Action buttons
        btn_frame = tk.Frame(self.frame, bg="#0f1419")
        btn_frame.pack(pady=20)
        
        # Send Email button
        self.send_btn = tk.Button(
            btn_frame,
            text="📧 Send Email",
            font=("Segoe UI", 12, "bold"),
            bg="#00d9ff",
            fg="#000000",
            activebackground="#00b8d4",
            activeforeground="#000000",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.send_email
        )
        self.send_btn.pack(side="left", padx=10)
        
        copy_btn = tk.Button(
            btn_frame,
            text="📋 Copy to Clipboard",
            font=("Segoe UI", 12),
            bg="#16213e",
            fg="#00d9ff",
            activebackground="#1e2a47",
            activeforeground="#00d9ff",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.copy_to_clipboard
        )
        copy_btn.pack(side="left", padx=10)
        
        new_btn = tk.Button(
            btn_frame,
            text="✨ Generate New Email",
            font=("Segoe UI", 12),
            bg="#16213e",
            fg="#00d9ff",
            activebackground="#1e2a47",
            activeforeground="#00d9ff",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.on_new
        )
        new_btn.pack(side="left", padx=10)
        
    def set_content(self, content: str, recipient_email: str = ""):
        """Set the email content to display"""
        self.email_content = content
        self.recipient_email = recipient_email
        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", content)
        self.preview_text.config(state="disabled")
    
    def send_email(self):
        """Send email via Gmail SMTP"""
        # Check if credentials are saved
        credentials = GmailConfig.load_credentials()
        if not credentials:
            response = messagebox.askyesno(
                "Gmail Setup Required",
                "Gmail credentials not configured.\n\nWould you like to set up Gmail now?"
            )
            if response:
                self.on_settings()
            return
        
        # Extract subject and body from email content
        lines = self.email_content.split('\n')
        subject = ""
        body_lines = []
        to_email = self.recipient_email
        
        for i, line in enumerate(lines):
            if line.startswith("To: "):
                to_email = line.replace("To: ", "").strip()
            elif line.startswith("Subject: "):
                subject = line.replace("Subject: ", "").strip()
            elif i > 1 and line.strip():  # Skip To and Subject lines
                body_lines.append(line)
        
        body = '\n'.join(body_lines).strip()
        
        if not to_email:
            messagebox.showerror(
                "Missing Recipient",
                "No recipient email address found in the email."
            )
            return
        
        if not subject:
            subject = "Email from Email Generator Bot"
        
        # Show sending indicator
        self.send_btn.config(text="📧 Sending...", state="disabled")
        self.parent.update()
        
        # Send email
        success, message = EmailSender.send_email(
            credentials["email"],
            credentials["password"],
            to_email,
            subject,
            body
        )
        
        # Re-enable button
        self.send_btn.config(text="📧 Send Email", state="normal")
        
        # Show result
        if success:
            messagebox.showinfo("Success", f"Email sent successfully to {to_email}!")
        else:
            messagebox.showerror("Error", f"Failed to send email:\n\n{message}")
    
    def copy_to_clipboard(self):
        """Copy email content to clipboard"""
        self.parent.clipboard_clear()
        self.parent.clipboard_append(self.email_content)
        messagebox.showinfo(
            "Success",
            "Email copied to clipboard!\nYou can now paste it into your email client."
        )
    
    def show(self):
        """Display the preview screen"""
        self.frame.pack(fill="both", expand=True)
        
    def hide(self):
        """Hide the preview screen"""
        self.frame.pack_forget()


class GmailSettingsScreen:
    """Gmail SMTP configuration screen"""
    
    def __init__(self, parent, on_back):
        self.parent = parent
        self.on_back = on_back
        self.frame = tk.Frame(parent, bg="#0f1419")
        
        # Header
        header_frame = tk.Frame(self.frame, bg="#0f1419")
        header_frame.pack(fill="x", pady=(20, 10))
        
        back_btn = tk.Button(
            header_frame,
            text="← Back",
            font=("Segoe UI", 11),
            bg="#16213e",
            fg="#00d9ff",
            activebackground="#1e2a47",
            activeforeground="#00d9ff",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.on_back
        )
        back_btn.pack(side="left", padx=20)
        
        title = tk.Label(
            header_frame,
            text="Gmail Setup",
            font=("Segoe UI", 24, "bold"),
            fg="#00d9ff",
            bg="#0f1419"
        )
        title.pack(side="left", padx=20)
        
        # Main content
        content_frame = tk.Frame(self.frame, bg="#0f1419")
        content_frame.pack(fill="both", expand=True, padx=60, pady=20)
        
        # Instructions
        instructions = tk.Label(
            content_frame,
            text="Configure Gmail SMTP to send emails directly from the bot",
            font=("Segoe UI", 12),
            fg="#a8a8a8",
            bg="#0f1419",
            wraplength=700
        )
        instructions.pack(pady=(0, 30))
        
        # Info box
        info_frame = tk.Frame(content_frame, bg="#1a1a2e", relief="flat")
        info_frame.pack(fill="x", pady=(0, 30), padx=20)
        
        info_title = tk.Label(
            info_frame,
            text="📌 Important: Use Gmail App Password",
            font=("Segoe UI", 11, "bold"),
            fg="#00d9ff",
            bg="#1a1a2e",
            anchor="w"
        )
        info_title.pack(fill="x", padx=15, pady=(15, 5))
        
        info_text = tk.Label(
            info_frame,
            text="1. Enable 2-Step Verification in your Google Account\n"
                 "2. Go to: myaccount.google.com/apppasswords\n"
                 "3. Generate an App Password for 'Mail'\n"
                 "4. Use that 16-character password below (not your regular password)",
            font=("Segoe UI", 10),
            fg="#ffffff",
            bg="#1a1a2e",
            justify="left",
            anchor="w"
        )
        info_text.pack(fill="x", padx=15, pady=(5, 15))
        
        # Form fields
        form_frame = tk.Frame(content_frame, bg="#0f1419")
        form_frame.pack(fill="x", pady=20)
        
        # Gmail Address
        email_label = tk.Label(
            form_frame,
            text="Gmail Address",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg="#0f1419",
            anchor="w"
        )
        email_label.pack(fill="x", pady=(10, 5))
        
        self.email_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            bg="#1a1a2e",
            fg="#ffffff",
            insertbackground="#00d9ff",
            relief="flat"
        )
        self.email_entry.pack(fill="x", ipady=10, pady=(0, 20))
        
        # Load existing credentials if available
        credentials = GmailConfig.load_credentials()
        if credentials:
            self.email_entry.insert(0, credentials["email"])
        
        # App Password
        password_label = tk.Label(
            form_frame,
            text="Gmail App Password (16 characters)",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg="#0f1419",
            anchor="w"
        )
        password_label.pack(fill="x", pady=(10, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            bg="#1a1a2e",
            fg="#ffffff",
            insertbackground="#00d9ff",
            relief="flat",
            show="*"
        )
        self.password_entry.pack(fill="x", ipady=10, pady=(0, 10))
        
        if credentials:
            self.password_entry.insert(0, credentials["password"])
        
        # Show/Hide password
        self.show_password_var = tk.BooleanVar()
        show_password_check = tk.Checkbutton(
            form_frame,
            text="Show password",
            variable=self.show_password_var,
            font=("Segoe UI", 9),
            fg="#a8a8a8",
            bg="#0f1419",
            selectcolor="#0f1419",
            activebackground="#0f1419",
            activeforeground="#00d9ff",
            command=self.toggle_password
        )
        show_password_check.pack(anchor="w", pady=(0, 20))
        
        # Action buttons
        btn_frame = tk.Frame(content_frame, bg="#0f1419")
        btn_frame.pack(pady=20)
        
        save_btn = tk.Button(
            btn_frame,
            text="💾 Save Credentials",
            font=("Segoe UI", 12, "bold"),
            bg="#00d9ff",
            fg="#000000",
            activebackground="#00b8d4",
            activeforeground="#000000",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.save_credentials
        )
        save_btn.pack(side="left", padx=10)
        
        test_btn = tk.Button(
            btn_frame,
            text="🧪 Test Connection",
            font=("Segoe UI", 12),
            bg="#16213e",
            fg="#00d9ff",
            activebackground="#1e2a47",
            activeforeground="#00d9ff",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.test_connection
        )
        test_btn.pack(side="left", padx=10)
        
        delete_btn = tk.Button(
            btn_frame,
            text="🗑️ Delete Credentials",
            font=("Segoe UI", 12),
            bg="#16213e",
            fg="#ff6b6b",
            activebackground="#1e2a47",
            activeforeground="#ff6b6b",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.delete_credentials
        )
        delete_btn.pack(side="left", padx=10)
    
    def toggle_password(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def save_credentials(self):
        """Save Gmail credentials"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter both email and app password."
            )
            return
        
        if "@gmail.com" not in email.lower():
            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid Gmail address (e.g., yourname@gmail.com)"
            )
            return
        
        if GmailConfig.save_credentials(email, password):
            messagebox.showinfo(
                "Success",
                "Gmail credentials saved successfully!\n\nYou can now send emails directly from the bot."
            )
        else:
            messagebox.showerror(
                "Error",
                "Failed to save credentials. Please try again."
            )
    
    def test_connection(self):
        """Test Gmail SMTP connection"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter both email and app password."
            )
            return
        
        # Try to send a test (will fail at send but will validate auth)
        try:
            import smtplib
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            server.quit()
            
            messagebox.showinfo(
                "Success",
                "Connection successful! ✅\n\nYour Gmail credentials are working correctly."
            )
        except smtplib.SMTPAuthenticationError:
            messagebox.showerror(
                "Authentication Failed",
                "Invalid email or app password.\n\nPlease check:\n"
                "• Email is correct\n"
                "• Using App Password (not regular password)\n"
                "• 2-Step Verification is enabled"
            )
        except Exception as e:
            messagebox.showerror(
                "Connection Error",
                f"Failed to connect to Gmail:\n\n{str(e)}"
            )
    
    def delete_credentials(self):
        """Delete saved credentials"""
        response = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete saved Gmail credentials?"
        )
        
        if response:
            if GmailConfig.delete_credentials():
                self.email_entry.delete(0, "end")
                self.password_entry.delete(0, "end")
                messagebox.showinfo(
                    "Success",
                    "Gmail credentials deleted successfully."
                )
            else:
                messagebox.showerror(
                    "Error",
                    "Failed to delete credentials."
                )
    
    def show(self):
        """Display the settings screen"""
        self.frame.pack(fill="both", expand=True)
        
    def hide(self):
        """Hide the settings screen"""
        self.frame.pack_forget()


class EmailGeneratorBot:
    """Main application class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Email Generator Bot")
        self.root.geometry("900x700")
        self.root.configure(bg="#0f1419")
        
        # Always on top
        self.root.attributes("-topmost", True)
        
        # Load templates
        self.templates = EmailTemplateLibrary.get_templates()
        self.current_template = None
        self.current_template_id = None
        
        # Initialize screens
        self.welcome_screen = AnimatedWelcomeScreen(
            self.root,
            self.show_category_selection
        )
        
        self.category_screen = CategorySelectionScreen(
            self.root,
            self.templates,
            self.show_form
        )
        
        self.form_screen = None
        self.preview_screen = PreviewScreen(
            self.root,
            self.back_to_form,
            self.show_category_selection,
            self.show_settings
        )
        
        self.settings_screen = GmailSettingsScreen(
            self.root,
            self.back_to_preview
        )
        
        # Show welcome screen
        self.welcome_screen.show()
        
        # Window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def show_category_selection(self):
        """Show category selection screen"""
        if hasattr(self, 'welcome_screen'):
            self.welcome_screen.hide()
        if self.form_screen:
            self.form_screen.hide()
        self.preview_screen.hide()
        self.category_screen.show()
    
    def show_form(self, template_id: str):
        """Show form for selected template"""
        self.current_template_id = template_id
        self.current_template = self.templates[template_id]
        
        self.category_screen.hide()
        
        # Create new form screen
        if self.form_screen:
            self.form_screen.hide()
        
        self.form_screen = FormScreen(
            self.root,
            self.current_template,
            self.generate_email,
            self.show_category_selection
        )
        self.form_screen.show()
    
    def generate_email(self, values: Dict[str, str]):
        """Generate email from template and values"""
        email_content = self.current_template.generate(values)
        recipient_email = values.get("recipient_email", "")
        self.show_preview(email_content, recipient_email)
    
    def show_preview(self, content: str, recipient_email: str = ""):
        """Show preview screen with generated email"""
        if self.form_screen:
            self.form_screen.hide()
        self.settings_screen.hide()
        self.preview_screen.set_content(content, recipient_email)
        self.preview_screen.show()
    
    def show_settings(self):
        """Show settings screen from preview"""
        self.preview_screen.hide()
        self.settings_screen.show()
    
    def back_to_preview(self):
        """Return to preview screen from settings"""
        self.settings_screen.hide()
        self.preview_screen.show()
    
    def back_to_form(self):
        """Return to form screen from preview"""
        self.preview_screen.hide()
        self.settings_screen.hide()
        if self.form_screen:
            self.form_screen.show()
    
    def on_closing(self):
        """Handle window close event"""
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Application entry point"""
    app = EmailGeneratorBot()
    app.run()


if __name__ == "__main__":
    main()
