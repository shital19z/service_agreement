"""Page 3.1 - Consumer Notice (matches dynamic_sa_page3_1.php)"""
from datetime import datetime

def generate_page3_1(data):
    """
    Generate Page 3.1 HTML - matches dynamic_sa_page3_1.php logic
    This page is optional and only for specific branches
    """
    # Get values directly from data, not from a nested 'result'
    clt_first = data.get('clt_first_name', '')
    clt_last = data.get('clt_last_name', '')
    handled_by = data.get('handled_by', '')
    logo_path = data.get('logo_path', '')
    
    html = '<div>'
    
    # Logo header - LEFT SIDE to match dynamic_sa_page3_1.php
    html += f'''
    <table width="100%" style="font-size:11.5px; margin-bottom:50px;" cellpadding="0" cellspacing="0">
        <tr>
            <td style="padding-left:18px;">
                <img style="width:2.0833in;height:0.9166in;" src="{logo_path}" />
            </td>
        </tr>
    </table>
    '''
    
    # Title
    html += '''
    <p style="text-align: center; font-weight:700; font-size: 18pt; font-family: Calibri; font-style: normal; text-decoration: underline; margin:0 0 10px 0;"><b>Consumer Notice of Direct Care Worker Status</b></p>
    <p style="text-align: center; font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal; margin:0 0 20px 0;">This form is to be completed by every consumer utilizing the <br> services of a Home Care Agency or Home Care Registry</p>
    '''
    
    # First section - Name
    html += f'''
    <table width="100%" style="font-size:12pt; margin-top:20px;" cellpadding="0" cellspacing="0">
        <tr>
            <td style="padding-left:18px;" width="5%" valign="top">
                <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal; margin:0;">I,</p>
            </td>
            <td width="55%" valign="top">
                <p style="text-align: center; font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal; margin:0;"><b>{clt_first} {clt_last}</b></p>
                <div style="border-top:2px solid black; width:95%; margin:5px auto 2px auto;"></div>
                <p style="text-align: center; font-weight:400; font-size: 10pt; font-family: Calibri; font-style: normal; margin:0;">(Print Name)</p>
            </td>
            <td width="40%" valign="top">
                <p style="text-align: left; font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal; margin:0;"> understand that:</p>
            </td>
        </tr>
    </table>
    '''
    
    # Second section - Initials and Insurance information
    # Dynamic: read consumer_notice_text from DB if saved via Edit Content.
    # Fallback: hardcoded default insurance notice text.
    consumer_notice_text = data.get('consumer_notice_text', '')
    _default_consumer_notice = (
        "I have been informed that Options For Senior America maintains general, professional liability, "
        "and workers compensation insurance covering the direct care worker who is employed by Options "
        "as an independent contractor."
    )
    insurance_text = consumer_notice_text or _default_consumer_notice

    html += f'''
    <table width="100%" style="font-size:12pt; margin-top:25px;" cellpadding="0" cellspacing="0">
        <tr>
            <td style="padding-left:18px;" width="20%" valign="top">
                <div style="border-top:2px solid black; width:80%; margin:0 auto 2px auto;"></div>
                <p style="text-align: center; font-weight:400; font-size: 11pt; font-family: Calibri; font-style: normal; margin:0;">Initials</p>
            </td>
            <td width="80%" valign="top">
                <p style="text-align: left; font-weight:400; font-size: 11pt; font-family: Calibri; font-style: normal; margin:0; line-height:1.3;">{insurance_text}</p>
            </td>
        </tr>
    </table>
    '''
    
    # Signature section - SIMPLIFIED to avoid table rendering issues
    current_date = datetime.now().strftime("%m/%d/%Y")
    
    # First signature row (consumer)
    html += f'''
    <table width="100%" style="font-size:12pt; margin-top:40px;" cellpadding="0" cellspacing="0">
        <tr>
            <td width="70%" align="center" style="padding-right:10px;">
                <div style="border-top:2px solid black; width:90%; margin:0 auto 2px auto;"></div>
                <p style="font-weight:400; font-size: 11pt; font-family: Calibri; font-style: normal; margin:0;">Signature of Consumer or Consumer\'s Representative</p>
            </td>
            <td width="30%" align="center" style="padding-left:10px;">
                <div style="border-top:2px solid black; width:80%; margin:0 auto 2px auto;"></div>
                <p style="font-weight:400; font-size: 11pt; font-family: Calibri; font-style: normal; margin:0;">Date</p>
            </td>
        </tr>
    </table>
    '''
    
    # Second signature row (representative) - completely separate table
    html += f'''
    <table width="100%" style="font-size:12pt; margin-top:30px;" cellpadding="0" cellspacing="0">
        <tr>
            <td width="70%" align="center" style="padding-right:10px;">
                <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal; margin:0 0 5px 0;"><b>{handled_by}</b></p>
                <div style="border-top:2px solid black; width:90%; margin:0 auto 2px auto;"></div>
                <p style="font-weight:400; font-size: 11pt; font-family: Calibri; font-style: normal; margin:0;">Signature of Representative of Options For Senior America</p>
            </td>
            <td width="30%" align="center" style="padding-left:10px;">
                <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal; margin:0 0 5px 0;"><b>{current_date}</b></p>
                <div style="border-top:2px solid black; width:80%; margin:0 auto 2px auto;"></div>
                <p style="font-weight:400; font-size: 11pt; font-family: Calibri; font-style: normal; margin:0;">Date</p>
            </td>
        </tr>
    </table>
    '''
    
    html += '</div>'
    return html