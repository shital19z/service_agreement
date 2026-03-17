"""Page 3.1 - Consumer Notice (matches dynamic_sa_page3_1.php exactly)"""
from datetime import datetime

def generate_page3_1(data):
    """
    Generate Page 3.1 HTML - matches dynamic_sa_page3_1.php exactly
    This page is optional and only for specific branches
    """
    clt_first  = data.get('clt_first_name', '')
    clt_last   = data.get('clt_last_name', '')
    handled_by = data.get('handled_by', '')
    logo_path  = data.get('logo_path', '')

    # ── Consumer notice text: DB override or hardcoded default ─────────────
    consumer_notice_text = data.get('consumer_notice_text', '')
    _default_notice = (
        "I have been informed that Options For Senior America maintains general, professional liability, "
        "and workers compensation insurance covering the direct care worker who is employed by Options "
        "as an independent contractor."
    )
    insurance_text = consumer_notice_text or _default_notice

    current_date = datetime.now().strftime("%m/%d/%Y")

    html = '<div>'

    # ── Logo — left side ────────────────────────────────────────────────────
    html += f'''
    <table width="100%" style="font-size:11.5px; margin-bottom:50px;" cellpadding="0" cellspacing="0">
        <tr>
            <td style="padding-left:18px;">
                <img style="width:2.0833in; height:0.9166in;" src="{logo_path}" />
            </td>
        </tr>
    </table>
    '''

    # ── Title ────────────────────────────────────────────────────────────────
    html += '''
    <p style="text-align:center; font-weight:700; font-size:18pt; font-family:Calibri; text-decoration:underline; margin:0;">
        <b>Consumer Notice of Direct Care Worker Status</b>
    </p>
    <p style="text-align:center; font-weight:400; font-size:12pt; font-family:Calibri; margin:5px 0 15px 0;">
        This form is to be completed by every consumer utilizing the services of a Home Care Agency or Home Care Registry
    </p>
    '''

    # ── Name section — use divs with inline-block to avoid negative width ───
    html += f'''
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:30px;">
        <tr>
            <td width="5%" style="font-size:12pt; font-family:Calibri; padding-left:18px; vertical-align:top;">I,</td>
            <td width="55%" style="vertical-align:top; padding-bottom:5px;">
                <p style="font-size:12pt; font-family:Calibri; font-weight:bold; margin:0 0 5px 0; text-align:center;">{clt_first} {clt_last}</p>
                <div style="border-top:2px solid black; margin:0 5px;"></div>
                <p style="font-size:10pt; font-family:Calibri; text-align:center; margin:2px 0 0 0;">(Print Name)</p>
            </td>
            <td width="40%" style="font-size:12pt; font-family:Calibri; vertical-align:bottom; padding-bottom:5px; padding-left:5px;">
                understand that:
            </td>
        </tr>
    </table>
    '''

    # ── Initials + Insurance ─────────────────────────────────────────────────
    html += f'''
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:30px;">
        <tr>
            <td width="20%" style="padding-left:18px; vertical-align:top;">
                <div style="border-top:2px solid black; width:80%; margin:10px auto 2px auto;"></div>
                <p style="text-align:center; font-size:11pt; font-family:Calibri; margin:0;">Initials</p>
            </td>
            <td width="80%" style="vertical-align:top; padding-left:5px;">
                <p style="font-size:11pt; font-family:Calibri; margin:0; line-height:1.4;">{insurance_text}</p>
            </td>
        </tr>
    </table>
    '''

    # ── Signatures — consumer row ────────────────────────────────────────────
    html += f'''
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:50px;">
        <tr>
            <td width="70%" align="center" style="padding-right:10px; vertical-align:bottom;">
                <p style="font-size:12pt; font-family:Calibri; margin:0 0 15px 0;">&nbsp;</p>
                <div style="border-top:2px solid black; margin:0 10px 2px 10px;"></div>
                <p style="font-size:11pt; font-family:Calibri; margin:2px 0 0 0;">Signature of Consumer or Consumer\'s Representative</p>
            </td>
            <td width="30%" align="center" style="padding-left:10px; vertical-align:bottom;">
                <p style="font-size:12pt; font-family:Calibri; margin:0 0 15px 0;">&nbsp;</p>
                <div style="border-top:2px solid black; margin:0 10px 2px 10px;"></div>
                <p style="font-size:11pt; font-family:Calibri; margin:2px 0 0 0;">Date</p>
            </td>
        </tr>
    </table>
    '''

    # ── Signatures — representative row ─────────────────────────────────────
    html += f'''
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:50px;">
        <tr>
            <td width="70%" align="center" style="padding-right:10px; vertical-align:bottom;">
                <p style="font-size:12pt; font-family:Calibri; font-weight:bold; margin:0 0 5px 0;">{handled_by}</p>
                <div style="border-top:2px solid black; margin:0 10px 2px 10px;"></div>
                <p style="font-size:11pt; font-family:Calibri; margin:2px 0 0 0;">Signature of Representative of Options For Senior America</p>
            </td>
            <td width="30%" align="center" style="padding-left:10px; vertical-align:bottom;">
                <p style="font-size:12pt; font-family:Calibri; font-weight:bold; margin:0 0 5px 0;">{current_date}</p>
                <div style="border-top:2px solid black; margin:0 10px 2px 10px;"></div>
                <p style="font-size:11pt; font-family:Calibri; margin:2px 0 0 0;">Date</p>
            </td>
        </tr>
    </table>
    '''

    html += '</div>'
    return html