#!/usr/bin/env python3
"""
Script to convert the progress report from markdown to PDF
"""

import markdown
from weasyprint import HTML, CSS
import os
from datetime import datetime

def markdown_to_html(markdown_text):
    """Convert markdown text to HTML"""
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code'])
    
    # Add CSS styling for better PDF appearance
    css_styles = """
    <style>
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            margin: 40px;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
        }
        h3 {
            color: #7f8c8d;
        }
        .completed {
            color: #27ae60;
            font-weight: bold;
        }
        .partial {
            color: #f39c12;
            font-weight: bold;
        }
        .not-completed {
            color: #e74c3c;
            font-weight: bold;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        .progress-bar {
            background-color: #ecf0f1;
            border-radius: 10px;
            padding: 3px;
            margin: 10px 0;
        }
        .progress-fill {
            background-color: #3498db;
            border-radius: 8px;
            height: 20px;
            text-align: center;
            color: white;
            line-height: 20px;
            font-size: 12px;
        }
        .status-on-track {
            color: #27ae60;
            font-weight: bold;
        }
        .status-behind {
            color: #e74c3c;
            font-weight: bold;
        }
        ul {
            padding-left: 20px;
        }
        li {
            margin: 5px 0;
        }
        .highlight {
            background-color: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
        }
    </style>
    """
    
    # Wrap in complete HTML document
    html_document = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Fraud Detection Project - Progress Report</title>
        {css_styles}
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    return html_document

def generate_pdf():
    """Generate PDF from the progress report"""
    try:
        # Read the markdown file
        with open('progress_report.md', 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        
        # Convert to HTML
        html_content = markdown_to_html(markdown_content)
        
        # Generate PDF
        HTML(string=html_content).write_pdf('Fraud_Detection_Progress_Report.pdf')
        
        print("✅ PDF report generated successfully: Fraud_Detection_Progress_Report.pdf")
        
    except ImportError:
        print("❌ WeasyPrint not installed. Installing required dependencies...")
        os.system("pip install weasyprint markdown")
        print("Please run the script again after installation.")
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        print("Creating alternative HTML report...")
        
        # Fallback: Create HTML file
        html_content = markdown_to_html(markdown_content)
        with open('Fraud_Detection_Progress_Report.html', 'w', encoding='utf-8') as file:
            file.write(html_content)
        print("✅ HTML report generated: Fraud_Detection_Progress_Report.html")

if __name__ == "__main__":
    generate_pdf() 