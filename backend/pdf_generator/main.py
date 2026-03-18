
"""
Main PDF Generator - Orchestrates all pages
Produces PDF matching SA - DC.pdf format
"""
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime

from .page1 import generate_page1
from .page1_cont import generate_page1_cont
from .page2 import generate_page2
from .page3 import generate_page3
from .page3_1 import generate_page3_1
from .styles import get_styles
from .footer_utils import get_header_tag, get_footer_tag

def json_to_pdf(data_dict):
    """
    Generate multi-page PDF service agreement matching SA - DC.pdf format
    """
    
    # Extract data - ✅ FIX: use (... or '') to handle None values safely
    branch = (data_dict.get('branch_code') or '').lower()
    care_state = (data_dict.get('care_state') or '').upper()

    def get_branch_specific_footer(branch_code : str) -> str:
        print('branch_code[:2] --->' , branch_code[:2])
        return branch_code[:2].upper()
    
    # Generate CSS styles - MATCHING SA - DC.pdf
    margins = {
        'top': 0.75,
        'bottom': 0.75,
        'left': 0.75,
        'right': 0.75
    }
    styles = get_styles(margins)
    
    # Generate each page HTML
    page1_html = generate_page1(data_dict)
    page1_cont_html = generate_page1_cont(data_dict)
    page2_html = generate_page2(data_dict)
    page3_html = generate_page3(data_dict)
    
    # Page 3.1 is only for specific branches
    page3_1_html = ""
    requires_consumer_notice = (
    data_dict.get('requires_consumer_notice', False)
    or branch in ['nspahomecare', 'nspahomecare_staging', 'hbhomecare', 'hbhomecare_staging']
    )
    if requires_consumer_notice:
        page3_1_html = generate_page3_1(data_dict)
    
    # Build HTML with proper page breaks and footer at bottom right
    full_html = f"""
    <html>
        <head>
            {styles}
            <style>
                /* Page container */
                .page {{
                    position: relative;
                    page-break-inside: avoid;
                    min-height: 95vh;
                }}
                
                /* Footer positioned at bottom right */
                .page-footer {{
                    position: absolute;
                    bottom: 0;
                    right: 0;
                    font-size: 6pt;
                    color: #666666;
                    text-align: right;
                }}
                
                /* Header */
                .page-header {{
                    font-size: 6pt;
                    color: #666;
                    margin-bottom: 10px;
                }}
                
                /* Page break */
                .page-break {{
                    page-break-before: always;
                }}
            </style>
        </head>
        <body>
            <!-- Page 1: Service Agreement -->
            <div class="page">
                {page1_html}
                <div id="footer_content" style="font-size:10px; color:#a29d96;">
                <table width="100%">
                    <tr>
                        <td align="left">{get_branch_specific_footer(branch)}</td>
                        <td align="right">{get_footer_tag(branch, care_state, 1)}</td>
                    </tr>
                </table>
            </div>
            </div>
            
            <!-- Page 2: Continuation -->
            <div class="page-break"></div>
            <div class="page">
                {page1_cont_html}
                <div id="footer_content" style="font-size:10px; color:#a29d96;">
                <table width="100%">
                    <tr>
                        <td align="left">{get_branch_specific_footer(branch)}</td>
                        <td align="right">{get_footer_tag(branch, care_state, 2)}</td>
                    </tr>
                </table>
            </div>
            </div>
            
            <!-- Page 3: Rights and Billing -->
            <div class="page-break"></div>
            <div class="page">
                {page2_html}
                <div id="footer_content" style="font-size:10px; color:#a29d96;">
                <table width="100%">
                    <tr>
                        <td align="left">{get_branch_specific_footer(branch)}</td>
                        <td align="right">{get_footer_tag(branch, care_state, 3)}</td>
                    </tr>
                </table>
            </div>
            </div>
            
            <!-- Page 4: EFT -->
            <div class="page-break"></div>
            <div class="page">
                {page3_html}
                <div id="footer_content" style="font-size:10px; color:#a29d96;">
                <table width="100%">
                    <tr>
                        <td align="left">{get_branch_specific_footer(branch)}</td>
                        <td align="right">{get_footer_tag(branch, care_state, 4)}</td>
                    </tr>
                </table>
            </div>
            </div>
    """
    
    # Add Page 3.1 if needed (as page 5)
    if requires_consumer_notice:
        full_html += f"""
            <!-- Page 5: Consumer Notice -->
            <div class="page-break"></div>
            <div class="page">
                {page3_1_html}
                <div class="page-footer">{get_footer_tag(branch, care_state, 5)}</div>
            </div>
        """
    
    full_html += """
        </body>
    </html>
    """
    
    # Generate PDF
    pdf_buffer = BytesIO()
    try:
        result = pisa.CreatePDF(full_html, dest=pdf_buffer)
        if result.err:
            print(f"PDF generation errors: {result.err}")
        pdf_buffer.seek(0)
        return pdf_buffer
    except Exception as e:
        pdf_buffer.close()
        raise Exception(f"Failed to generate PDF: {str(e)}")
