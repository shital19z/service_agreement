"""Page 3 - EFT Authorization (matches dynamic_sa_page3.php)"""
from datetime import datetime

def generate_page3(data):
    """
    Generate Page 3 HTML - matches dynamic_sa_page3.php logic
    """
    # Get values directly from data, not from a nested 'result'
    care_title = data.get('care_title', '')
    care_first = data.get('care_first_name', '')
    care_last = data.get('care_last_name', '')
    
    clt_title = data.get('clt_title', '')
    clt_first = data.get('clt_first_name', '')
    clt_last = data.get('clt_last_name', '')
    
    html = '<div>'
    
    html += '''
    <p style="text-align: center; font-weight:700; font-size: 18pt; font-family: Calibri; font-style: normal; text-decoration: underline;"><b>Authorization for a Repeating Electronic Funds Transfer</b></p>
    <p style="text-align: center; font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;">(Save time and postage. Avoid interest charges, late payments, and termination notices)</p>
    '''
    
    html += f'''
    <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;padding-top:30px;">I, the undersigned, acknowledge that invoices prepared by Options for Senior America (Options) are due upon receipt, and therefore hereby authorize Options to withdraw any amounts owed by me on the same day as the invoice is prepared and emailed to me.   This funds withdrawal is made by initiating an electronic funds transfer, as a debit through ACH (Automated Clearing House) from my account at the financial institution (hereinafter "Bank") indicated below.  I also agree that, in the event the below mentioned care recipient passes away, I will not close this referenced bank account until I receive notification from Options that the final Options invoice is paid in full using the method of payment herein described.  Furthermore, I authorize Bank to accept and to debit entries indicated by Options from my account.</p>
    
    <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;padding-top:10px;">This authorization is to remain in full force and effect until Options and Bank have received written notice from me of its termination in such time and in such manner as to afford Options and Bank reasonable opportunity to act on it.</p>
    
    <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;padding-top:30px;padding-left:60px;">Care Recipient Name:&nbsp;&nbsp;<b>{care_title} {care_first} {care_last}</b></p>
    
    <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;padding-top:10px;padding-left:60px;">Client Bank Account Signatory Name:&nbsp;&nbsp;<b>{clt_title} {clt_first} {clt_last}</b></p>
    
    <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;padding-top:10px;padding-left:60px;">Client Signature:&nbsp;&nbsp;_______________________________________________</p>
    
    <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;padding-top:10px;padding-left:60px;">Date:&nbsp;&nbsp;<b>{datetime.now().strftime("%m/%d/%Y")}</b></p>
    
    <p style="font-weight:700; font-size: 14pt; font-family: Calibri; font-style: normal;padding-top:10px;padding-left:60px;">&nbsp;&nbsp;***************************************************************************</p>
    
    <p style="font-weight:700; font-size: 14pt; font-family: Calibri; font-style: normal;padding-top:10px;padding-left:60px;text-decoration: underline;"><b>Account Information</b></p>
    
    <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;padding-top:10px;padding-left:60px;">Bank Name, City, and State:&nbsp;&nbsp;______________________________________</p>
    
    <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;padding-top:10px;padding-left:60px;">Routing Transit #:&nbsp;&nbsp;_______________________________________________</p>
    
    <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;padding-top:10px;padding-left:60px;">Account Number:&nbsp;&nbsp;_______________________________________________</p>
    
    <p style="font-weight:400; font-size: 12pt; font-family: Calibri; font-style: normal;padding-top:10px;padding-left:60px;">Account Type:&nbsp;&nbsp;<input type="checkbox">&nbsp;&nbsp; Checking &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="checkbox">&nbsp;&nbsp; Saving</p>
    
    <div style="margin-top:10px; margin-left:60px; margin-right:60px; text-align: center; font-weight:400; font-size: 12pt; padding:100px; border: 4px double #000; border-width:4pt;"><b>----------Please Attach a Voided Check Here----------</b></div>
    '''
    
    html += '</div>'
    return html