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
    
    # Logo header
    html += f'''
    <table width="100%" style="font-size:11.5px;margin-bottom:50px;">
        <tr>
            <td style="padding-left:18px;">
                <img style="width:2.0833in;height:0.9166in;" src="{logo_path}" />
            </td>
        </tr>
    </table>
    '''
    
    # Title
    html += '''
    <p style="text-align: center; font-weight:700; font-size: 18pt; font-family: Calibri; font-style: normal; text-decoration: underline;"><b>Consumer Notice of Direct Care Worker Status</b></p>
    <p style="text-align: center; font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;">This form is to be completed by every consumer utilizing the <br> services of a Home Care Agency or Home Care Registry</p>
    '''
    
    # First section - Name
    html += f'''
    <table width="100%" style="font-size:11.5px;margin-top:30px;">
        <tr>
            <td style="padding-left:18px;" width="1%">
                <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;">I,</p>
                <p>&nbsp;&nbsp;</p>
            </td>
            <td width="59%">
                <p style="text-align: center; font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;"><b>&nbsp; &nbsp; {clt_first} {clt_last}</b></p>
                <p style="border-top:2px solid black; text-align: center; font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (Print Name) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</p>
            </td>
            <td width="40%">
                <p style="text-align: left; font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;padding-top:50px;"> understand that:</p>
                <p>&nbsp;&nbsp;</p>
            </td>
        </tr>
    </table>
    '''
    
    # Second section - Insurance information
    html += '''
    <table width="100%" style="font-size:11.5px;margin-top:30px;">
        <tr>
            <td style="padding-left:18px;" width="20%">
                <p style="font-size:2px;">&nbsp;</p>
                <p style="text-align: center; font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal; border-top:2px solid black;"> &nbsp;&nbsp;&nbsp;&nbsp; Initials &nbsp;&nbsp;&nbsp;&nbsp;</p>
            </td>
            <td style="padding-left:-17px;" width="80%">
                <p style="text-align: center; font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;">I have been informed that Options For Senior America maintains general, professional liability, and workers compensation insurance covering the direct care worker who is employed by Options as an independent contractor.</p>                
            </td>
        <tr>
    </table>
    '''
    
    # Signature section
    html += f'''
    <table width="100%" style="font-size:11.5px;margin-top:50px;">
        <tr>
            <td align="center" width="70%">
                <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;"><b>&nbsp;</b></p><p style="font-size:2px;">&nbsp;</p>
                <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;border-top:2px solid black;">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Signature of Consumer or Consumer\'s Representative &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</p>
            </td>
            <td align="center" width="30%">
                <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;"><b>&nbsp;</b></p><p style="font-size:2px;">&nbsp;</p>
                <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;border-top:2px solid black;">&nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  Date &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;</p>
            </td>
        </tr>
        <tr>
            <td align="center" width="70%" style="padding-top:50px;">
                <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;"><b>{handled_by}</b></p><p style="font-size:2px;">&nbsp;</p>
                <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;border-top:2px solid black;">&nbsp; &nbsp; &nbsp; &nbsp; Signature of Representative of Options For Senior America  &nbsp; &nbsp; &nbsp; &nbsp;</p>
            </td>
            <td align="center" width="30%" style="padding-top:50px;">
                <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;"><b> {datetime.now().strftime("%m/%d/%Y")} </b></p><p style="font-size:2px;">&nbsp;</p>
                <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;border-top:2px solid black;">&nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  Date &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;</p>
            </td>
        </tr>
    </table>
    '''
    
    html += '</div>'
    return html