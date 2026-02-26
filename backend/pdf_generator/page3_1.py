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
    
    # Logo header - reduced margin
    html += f'''
    <table width="100%" style="font-size:10px; margin-bottom:20px;">
        <tr>
            <td style="padding-left:10px;">
                <img style="width:2in;height:0.9in;" src="{logo_path}" />
            </td>
        </tr>
    </table>
    '''
    
    # Title - reduced font sizes and margins
    html += '''
    <p style="text-align: center; font-weight:700; font-size: 16pt; font-family: Calibri; font-style: normal; text-decoration: underline; margin:5px 0;"><b>Consumer Notice of Direct Care Worker Status</b></p>
    <p style="text-align: center; font-weight:400; font-size: 10pt; font-family: Calibri; font-style: normal; margin:2px 0;">This form is to be completed by every consumer utilizing the <br> services of a Home Care Agency or Home Care Registry</p>
    '''
    
    # First section - Name - reduced spacing
    html += f'''
    <table width="100%" style="font-size:10px; margin-top:15px;">
        <tr>
            <td style="padding-left:10px;" width="5%">
                <p style="font-weight:400; font-size: 11pt; font-family: Calibri; margin:0;">I,</p>
            </td>
            <td width="55%">
                <p style="text-align: center; font-weight:400; font-size: 11pt; font-family: Calibri; margin:0;"><b>{clt_first} {clt_last}</b></p>
                <div style="border-top:1.5px solid black; width:90%; margin:2px auto;"></div>
                <p style="text-align: center; font-weight:400; font-size: 10pt; font-family: Calibri; margin:1px 0;">(Print Name)</p>
            </td>
            <td width="40%">
                <p style="text-align: left; font-weight:400; font-size: 11pt; font-family: Calibri; margin:0; padding-top:5px;"> understand that:</p>
            </td>
        </tr>
    </table>
    '''
    
    # Second section - Insurance information - reduced spacing
    html += '''
    <table width="100%" style="font-size:10px; margin-top:15px;">
        <tr>
            <td style="padding-left:10px;" width="15%">
                <div style="border-top:1.5px solid black; width:80%; margin:0 auto;"></div>
                <p style="text-align: center; font-weight:400; font-size: 10pt; font-family: Calibri; margin:1px 0;">Initials</p>
            </td>
            <td style="padding-left:5px;" width="85%">
                <p style="text-align: left; font-weight:400; font-size: 10pt; font-family: Calibri; margin:0; line-height:1.2;">I have been informed that Options For Senior America maintains general, professional liability, and workers compensation insurance covering the direct care worker who is employed by Options as an independent contractor.</p>                
            </td>
        </tr>
    </table>
    '''
    
    # Signature section - reduced spacing
    html += f'''
    <table width="100%" style="font-size:10px; margin-top:25px;">
        <tr>
            <td align="center" width="70%" style="padding-right:5px;">
                <div style="border-top:1.5px solid black; width:80%; margin:0 auto;"></div>
                <p style="font-weight:400; font-size: 10pt; font-family: Calibri; margin:2px 0;">Signature of Consumer or Consumer\'s Representative</p>
            </td>
            <td align="center" width="30%" style="padding-left:5px;">
                <div style="border-top:1.5px solid black; width:80%; margin:0 auto;"></div>
                <p style="font-weight:400; font-size: 10pt; font-family: Calibri; margin:2px 0;">Date</p>
            </td>
        </tr>
        <tr>
            <td align="center" width="70%" style="padding-top:20px; padding-right:5px;">
                <p style="font-weight:400; font-size: 11pt; font-family: Calibri; margin:0;"><b>{handled_by}</b></p>
                <div style="border-top:1.5px solid black; width:80%; margin:5px auto 0;"></div>
                <p style="font-weight:400; font-size: 10pt; font-family: Calibri; margin:2px 0;">Signature of Representative of Options For Senior America</p>
            </td>
            <td align="center" width="30%" style="padding-top:20px; padding-left:5px;">
                <p style="font-weight:400; font-size: 11pt; font-family: Calibri; margin:0;"><b>{datetime.now().strftime("%m/%d/%Y")}</b></p>
                <div style="border-top:1.5px solid black; width:80%; margin:5px auto 0;"></div>
                <p style="font-weight:400; font-size: 10pt; font-family: Calibri; margin:2px 0;">Date</p>
            </td>
        </tr>
    </table>
    '''
    
    html += '</div>'
    return html