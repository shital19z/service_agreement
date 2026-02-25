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

def json_to_pdf(data_dict):
    """
    Generate multi-page PDF service agreement matching SA - DC.pdf format
    """
    
    # Extract data
    branch = data_dict.get('branch_code', '').lower()
    care_state = data_dict.get('care_state', '').upper()
    
    # print("="*50)
    # print("PDF GENERATOR MAIN")
    # print(f"Branch: {branch}")
    # print("="*50)
    
    # Generate CSS styles - MATCHING SA - DC.pdf
    styles = get_styles()
    
    # Generate each page HTML
    page1_html = generate_page1(data_dict)
    page1_cont_html = generate_page1_cont(data_dict)
    page2_html = generate_page2(data_dict)
    page3_html = generate_page3(data_dict)
    
    # Page 3.1 is only for specific branches
    page3_1_html = ""
    requires_consumer_notice = branch in ['nspahomecare', 'nspahomecare_staging', 'hbhomecare', 'hbhomecare_staging']
    if requires_consumer_notice:
        page3_1_html = generate_page3_1(data_dict)
    
    # Build HTML with proper page breaks
    full_html = f"""
    <html>
        <head>
            {styles}
        </head>
        <body>
            <!-- Page 1: Service Agreement -->
            <div class="page">
                {page1_html}
                <div class="page-footer">{get_footer_tag(branch, care_state, 1)}</div>
            </div>
            
            <!-- Page 2: Continuation -->
            <div class="page-break"></div>
            <div class="page">
                <div class="page-header">{get_header_tag(branch, care_state, 2)}</div>
                {page1_cont_html}
                <div class="page-footer">{get_footer_tag(branch, care_state, 2)}</div>
            </div>
            
            <!-- Page 3: Rights and Billing -->
            <div class="page-break"></div>
            <div class="page">
                {page2_html}
                <div class="page-footer">{get_footer_tag(branch, care_state, 3)}</div>
            </div>
            
            <!-- Page 4: EFT -->
            <div class="page-break"></div>
            <div class="page">
                {page3_html}
                <div class="page-footer">{get_footer_tag(branch, care_state, 4)}</div>
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

def get_styles():
    """CSS styles matching SA - DC.pdf format"""
    return """
    <style>
        @page { 
            size: letter; 
            margin: 0.75in;
        }
        body { 
            font-family: Helvetica, Arial, sans-serif; 
            font-size: 8pt; 
            line-height: 1.2; 
            color: #000000; 
        }
        
        /* Page breaks */
        .page-break { 
            page-break-before: always; 
        }
        .page {
            page-break-inside: avoid;
        }
        
        /* Header and Footer */
        .page-header {
            font-size: 6pt;
            color: #666;
            margin-bottom: 20px;
        }
        .page-footer {
            font-size: 6pt;
            color: #666;
            margin-top: 20px;
            text-align: right;
        }
        
        /* Office info - like SA - DC.pdf */
        .office-info {
            font-size: 8pt;
            margin-bottom: 15px;
            line-height: 1.3;
        }
        
        /* Responsible Party - like SA - DC.pdf */
        .responsible-party {
            margin-top: 15px;
            font-size: 8pt;
        }
        .responsible-party u {
            font-weight: normal;
        }
        .responsible-party b {
            font-weight: bold;
        }
        

        .date {
            text-align: right;
            font-weight: bold;
            margin: 10px 0 20px 0;
            font-size: 8pt;
        }
        
        /* Service Agreement title - like SA - DC.pdf */
        .service-title {
            text-align: center;
            font-size: 14pt;
            font-weight: bold;
            margin: 20px 0;
        }
        
        /* Care Recipient line - like SA - DC.pdf */
        .care-recipient {
            text-align: center;
            font-size: 8pt;
            margin-bottom: 20px;
        }
        
        /* Admin table - like SA - DC.pdf */
        .admin-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            border: 1px solid #000;
        }
        .admin-table th {
            border: 1px solid #000;
            background-color: #f2f2f2;
            padding: 6px;
            text-align: center;
            font-weight: bold;
            font-size: 7pt;
        }
        .admin-table td {
            border: 1px solid #000;
            padding: 8px;
            text-align: center;
            font-weight: bold;
            font-size: 8pt;
        }
        
        /* Section headers - like SA - DC.pdf (bold, not underlined) */
        .section-title {
            font-weight: bold;
            margin: 12px 0 4px 0;
            font-size: 8pt;
        }
        
        /* Regular text - like SA - DC.pdf */
        .legal-text {
            text-align: justify;
            margin-bottom: 8px;
            font-size: 8pt;
        }
        
        /* Signature table - like SA - DC.pdf */
        .signature-table {
            width: 100%;
            margin-top: 30px;
            border-collapse: collapse;
        }
        .signature-box {
            border-top: 2px solid #000;
            text-align: center;
            font-size: 7pt;
            padding-top: 5px;
            margin-top: 5px;
        }
        
        /* List styles - like SA - DC.pdf */
        ol, ul {
            padding-left: 25px;
            margin-top: 5px;
            margin-bottom: 10px;
        }
        li {
            margin-bottom: 4px;
            text-align: justify;
            font-size: 8pt;
        }
        
        /* Nested lists */
        .nested-list {
            padding-left: 40px;
            list-style-type: lower-alpha;
        }
        .double-nested {
            padding-left: 60px;
            list-style-type: lower-roman;
        }
        
        /* EFT Form - like SA - DC.pdf */
        .eft-title {
            text-align: center;
            font-weight: bold;
            font-size: 12pt;
            margin: 20px 0 5px 0;
        }
        .eft-subtitle {
            text-align: center;
            font-style: italic;
            font-size: 8pt;
            margin-bottom: 30px;
        }
        .form-field {
            border-bottom: 1px solid #000;
            min-height: 20px;
            margin: 5px 0 15px 0;
        }
        .form-label {
            font-weight: bold;
            margin-top: 10px;
        }
        
        /* Void check box */
        .void-box {
            border: 2px double #000;
            padding: 20px;
            text-align: center;
            margin: 30px 0 20px 0;
            font-weight: bold;
        }
        
        /* Account Information section */
        .account-info-title {
            font-weight: bold;
            font-size: 9pt;
            margin: 20px 0 10px 0;
        }
        
        /* Separator line */
        .separator {
            text-align: center;
            margin: 30px 0;
            font-size: 10pt;
        }
    </style>
    """

def get_header_tag(branch, care_state, page_num):
    """Get header tag for page (like BA, DC in the example)"""
    if page_num == 2:
        if branch in ['dchomecare', 'dchomecare_staging']:
            return "DC"
        elif branch in ['bahomecare', 'bahomecare_staging']:
            return "BA"
        elif branch in ['mnhomecare', 'mnhomecare_staging']:
            return "MN"
        elif branch in ['gbhomecare', 'gbhomecare_staging']:
            return "GB"
        else:
            return branch[:2].upper()
    return ""

def get_footer_tag(branch, care_state, page_num):
    """Get footer tag (like MD 2019-09-16 in the example)"""
    # Page 1 footer
    if page_num == 1:
        if branch in ['anhomecare', 'anhomecare_staging', 'bahomecare', 'bahomecare_staging', 
                       'blhomecare', 'blhomecare_staging', 'fkhomecare', 'fkhomecare_staging', 
                       'lphomecare', 'lphomecare_staging', 'testhomecare']:
            return "MD 2019-09-16"
        elif branch in ['athomecare', 'athomecare_staging']:
            return "GA 2019-12-02"
        elif branch in ['scgahomecare', 'scgahomecare_staging']:
            return "SCGA 2019-12-03"
        elif branch in ['clhomecare', 'clhomecare_staging']:
            return "DCOH 2019-09-16"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state == "DC":
            return "DCOH 09-16-2019"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state != "DC":
            return "MD 2019-09-16"
        elif branch in ['nvahomecare', 'nvahomecare_staging', 'rihomecare', 'rihomecare_staging']:
            return "VA 2019-09-16"
        elif branch in ['tahomecare', 'tahomecare_staging']:
            return "FL 2017-06-19"
        elif branch in ['gbhomecare', 'gbhomecare_staging']:
            return "GBNC 2019-09-16"
        elif branch in ['rdhomecare', 'rdhomecare_staging']:
            return "RDNC 2020-04-29"
        elif branch in ['mnhomecare', 'mnhomecare_staging']:
            return "MNVA 2017-06-19"
        elif branch in ['lovahomecare', 'lovahomecare_staging']:
            return "LOVA 2019-11-06"
        elif branch in ['lkinhomecare', 'lkinhomecare_staging']:
            return "IN 2019-09-16"
        elif branch in ['shmihomecare', 'shmihomecare_staging']:
            return "MI 2019-12-06"
        elif branch in ['wenjhomecare', 'wenjhomecare_staging']:
            return "NJ 2019-09-16"
        elif branch in ['hbhomecare', 'hbhomecare_staging']:
            return "PA 2019-12-10"
        elif branch in ['wfvahomecare', 'wfvahomecare_staging']:
            return "WFVA 2020-01-03"
        elif branch in ['cfairfaxhomecare', 'cfairfaxhomecare_staging']:
            return "CFVA 2020-02-22"
        elif branch in ['nspahomecare', 'nspahomecare_staging']:
            return "NSPA 2022-01-02"
    
    # Page 2 footer
    elif page_num == 2:
        if branch in ['anhomecare', 'anhomecare_staging', 'bahomecare', 'bahomecare_staging', 
                       'blhomecare', 'blhomecare_staging', 'fkhomecare', 'fkhomecare_staging', 
                       'lphomecare', 'lphomecare_staging', 'testhomecare']:
            return "MD 2017-06-19"
        elif branch in ['athomecare', 'athomecare_staging']:
            return "GA 2019-12-02"
        elif branch in ['scgahomecare', 'scgahomecare_staging']:
            return "SCGA 2019-12-03"
        elif branch in ['clhomecare', 'clhomecare_staging']:
            return "DCOH 2017-06-19"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state == "DC":
            return "DCOH 06-19-2017"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state != "DC":
            return "MD 2017-06-19"
        elif branch in ['nvahomecare', 'nvahomecare_staging', 'rihomecare', 'rihomecare_staging']:
            return "VA 2017-06-19"
        elif branch in ['tahomecare', 'tahomecare_staging']:
            return "FL 2017-06-19"
        elif branch in ['gbhomecare', 'gbhomecare_staging']:
            return "GBNC 2020-04-27"
        elif branch in ['rdhomecare', 'rdhomecare_staging']:
            return "RDNC 2020-04-27"
        elif branch in ['mnhomecare', 'mnhomecare_staging']:
            return "MNVA 2019-09-16"
        elif branch in ['lovahomecare', 'lovahomecare_staging']:
            return "LOVA 2019-09-16"
        elif branch in ['lkinhomecare', 'lkinhomecare_staging']:
            return "LKIN 2017-06-19"
        elif branch in ['shmihomecare', 'shmihomecare_staging']:
            return "MI 2019-12-06"
        elif branch in ['wenjhomecare', 'wenjhomecare_staging']:
            return "NJ 2019-09-12"
        elif branch in ['hbhomecare', 'hbhomecare_staging']:
            return "PA 2020-04-30"
        elif branch in ['wfvahomecare', 'wfvahomecare_staging']:
            return "WFVA 2020-01-03"
        elif branch in ['cfairfaxhomecare', 'cfairfaxhomecare_staging']:
            return "CFVA 2020-02-22"
    
    # Page 3 footer
    elif page_num == 3:
        if branch in ['anhomecare', 'anhomecare_staging', 'bahomecare', 'bahomecare_staging', 
                       'blhomecare', 'blhomecare_staging', 'fkhomecare', 'fkhomecare_staging', 
                       'lphomecare', 'lphomecare_staging', 'testhomecare']:
            return "MD 2017-04-12"
        elif branch in ['athomecare', 'athomecare_staging']:
            return "GA 2019-12-03"
        elif branch in ['scgahomecare', 'scgahomecare_staging']:
            return "SCGA 2019-12-03"
        elif branch in ['clhomecare', 'clhomecare_staging']:
            return "DCOH - 2016-08-08"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state == "DC":
            return "DCOH - 08-08-2016"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state != "DC":
            return "MD 2017-04-12"
        elif branch in ['nvahomecare', 'nvahomecare_staging']:
            return "NVA - 2017-04-12"
        elif branch in ['rihomecare', 'rihomecare_staging']:
            return "RIVA - 2017-04-12"
        elif branch in ['tahomecare', 'tahomecare_staging']:
            return "FL - 2017-05-18"
        elif branch in ['gbhomecare', 'gbhomecare_staging']:
            return "GBNC - 2020-04-27"
        elif branch in ['rdhomecare', 'rdhomecare_staging']:
            return "RDNC - 2020-04-27"
        elif branch in ['mnhomecare', 'mnhomecare_staging']:
            return "MNVA - 2017-04-12"
        elif branch in ['lovahomecare', 'lovahomecare_staging']:
            return "LOVA 2019-11-06"
        elif branch in ['lkinhomecare', 'lkinhomecare_staging']:
            return "LKIN 2017-04-26"
        elif branch in ['shmihomecare', 'shmihomecare_staging']:
            return "MI 2019-12-06"
        elif branch in ['wenjhomecare', 'wenjhomecare_staging']:
            return "NJ 2020-04-27"
        elif branch in ['hbhomecare', 'hbhomecare_staging']:
            return "PA - 2019-12-10"
        elif branch in ['wfvahomecare', 'wfvahomecare_staging']:
            return "WFVA 2020-01-03"
        elif branch in ['cfairfaxhomecare', 'cfairfaxhomecare_staging']:
            return "CFVA 2020-02-22"
    
    elif page_num == 4:
        if branch in ['anhomecare', 'anhomecare_staging', 'bahomecare', 'bahomecare_staging', 
                       'blhomecare', 'blhomecare_staging', 'fkhomecare', 'fkhomecare_staging', 
                       'lphomecare', 'lphomecare_staging', 'testhomecare']:
            return "MD 2017-04-12"
        elif branch in ['athomecare', 'athomecare_staging']:
            return "GA 2019-12-03"
        elif branch in ['scgahomecare', 'scgahomecare_staging']:
            return "SCGA 2019-12-03"
        elif branch in ['clhomecare', 'clhomecare_staging']:
            return "DCOH - 2016-08-08"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state == "DC":
            return "DCOH - 08-08-2016"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state != "DC":
            return "MD 2017-04-12"
        elif branch in ['nvahomecare', 'nvahomecare_staging']:
            return "NVA - 2017-04-12"
        elif branch in ['rihomecare', 'rihomecare_staging']:
            return "RIVA - 2017-04-12"
        elif branch in ['tahomecare', 'tahomecare_staging']:
            return "FL - 2017-05-18"
        elif branch in ['gbhomecare', 'gbhomecare_staging']:
            return "GBNC - 2020-04-27"
        elif branch in ['rdhomecare', 'rdhomecare_staging']:
            return "RDNC - 2020-04-27"
        elif branch in ['mnhomecare', 'mnhomecare_staging']:
            return "MNVA - 2017-04-12"
        elif branch in ['lovahomecare', 'lovahomecare_staging']:
            return "LOVA 2019-11-06"
        elif branch in ['lkinhomecare', 'lkinhomecare_staging']:
            return "LKIN 2017-04-26"
        elif branch in ['shmihomecare', 'shmihomecare_staging']:
            return "MI 2019-12-06"
        elif branch in ['wenjhomecare', 'wenjhomecare_staging']:
            return "NJ 2020-04-27"
        elif branch in ['hbhomecare', 'hbhomecare_staging']:
            return "PA - 2019-12-10"
        elif branch in ['wfvahomecare', 'wfvahomecare_staging']:
            return "WFVA 2020-01-03"
        elif branch in ['cfairfaxhomecare', 'cfairfaxhomecare_staging']:
            return "CFVA 2020-02-22"
        
    elif page_num == 5:
        if branch in ['anhomecare', 'anhomecare_staging', 'bahomecare', 'bahomecare_staging', 
                       'blhomecare', 'blhomecare_staging', 'fkhomecare', 'fkhomecare_staging', 
                       'lphomecare', 'lphomecare_staging', 'testhomecare']:
            return "MD 2017-04-12"
        elif branch in ['athomecare', 'athomecare_staging']:
            return "GA 2019-12-03"
        elif branch in ['scgahomecare', 'scgahomecare_staging']:
            return "SCGA 2019-12-03"
        elif branch in ['clhomecare', 'clhomecare_staging']:
            return "DCOH - 2016-08-08"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state == "DC":
            return "DCOH - 08-08-2016"
        elif branch in ['dchomecare', 'dchomecare_staging'] and care_state != "DC":
            return "MD 2017-04-12"
        elif branch in ['nvahomecare', 'nvahomecare_staging']:
            return "NVA - 2017-04-12"
        elif branch in ['rihomecare', 'rihomecare_staging']:
            return "RIVA - 2017-04-12"
        elif branch in ['tahomecare', 'tahomecare_staging']:
            return "FL - 2017-05-18"
        elif branch in ['gbhomecare', 'gbhomecare_staging']:
            return "GBNC - 2020-04-27"
        elif branch in ['rdhomecare', 'rdhomecare_staging']:
            return "RDNC - 2020-04-27"
        elif branch in ['mnhomecare', 'mnhomecare_staging']:
            return "MNVA - 2017-04-12"
        elif branch in ['lovahomecare', 'lovahomecare_staging']:
            return "LOVA 2019-11-06"
        elif branch in ['lkinhomecare', 'lkinhomecare_staging']:
            return "LKIN 2017-04-26"
        elif branch in ['shmihomecare', 'shmihomecare_staging']:
            return "MI 2019-12-06"
        elif branch in ['wenjhomecare', 'wenjhomecare_staging']:
            return "NJ 2020-04-27"
        elif branch in ['hbhomecare', 'hbhomecare_staging']:
            return "PA - 2019-12-10"
        elif branch in ['wfvahomecare', 'wfvahomecare_staging']:
            return "WFVA 2020-01-03"
        elif branch in ['cfairfaxhomecare', 'cfairfaxhomecare_staging']:
            return "CFVA 2020-02-22"
    
 
    
 