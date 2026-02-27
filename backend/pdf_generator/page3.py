"""Page 3 - EFT Authorization (matches dynamic_sa_page3.php)"""
from datetime import datetime

def generate_page3(data):
    """
    Generate Page 3 HTML - matches dynamic_sa_page3.php logic
    """
    # Get values directly from data
    care_title = data.get('care_title', '')
    care_first = data.get('care_first_name', '')
    care_last = data.get('care_last_name', '')
    
    clt_title = data.get('clt_title', '')
    clt_first = data.get('clt_first_name', '')
    clt_last = data.get('clt_last_name', '')
    
    # Debug prints to see what's coming in
    print(f"DEBUG - Page 3 - care_title: '{care_title}'")
    print(f"DEBUG - Page 3 - care_first: '{care_first}'")
    print(f"DEBUG - Page 3 - care_last: '{care_last}'")
    print(f"DEBUG - Page 3 - clt_title: '{clt_title}'")
    print(f"DEBUG - Page 3 - clt_first: '{clt_first}'")
    print(f"DEBUG - Page 3 - clt_last: '{clt_last}'")
    
    # Clean and normalize names for comparison
    care_first_clean = care_first.strip().lower() if care_first else ''
    care_last_clean = care_last.strip().lower() if care_last else ''
    clt_first_clean = clt_first.strip().lower() if clt_first else ''
    clt_last_clean = clt_last.strip().lower() if clt_last else ''
    
    # Check if client and care recipient are the same person
    same_person = (care_first_clean and care_last_clean and 
                   care_first_clean == clt_first_clean and 
                   care_last_clean == clt_last_clean)
    
    # For the same person, use the client's title (Mr.) for both
    if same_person:
        # Use client's title for both care recipient and client
        display_care_title = clt_title
        display_clt_title = clt_title
        print(f"DEBUG - Same person detected, using client title '{clt_title}' for both")
    else:
   
        display_care_title = care_title
        display_clt_title = clt_title
    
    # Format names with proper spacing
    care_name_parts = []
    if display_care_title and display_care_title.strip():
        care_name_parts.append(display_care_title.strip())
    if care_first and care_first.strip():
        care_name_parts.append(care_first.strip())
    if care_last and care_last.strip():
        care_name_parts.append(care_last.strip())
    
    care_name = ' '.join(care_name_parts) if care_name_parts else "Not Provided"
    
    clt_name_parts = []
    if display_clt_title and display_clt_title.strip():
        clt_name_parts.append(display_clt_title.strip())
    if clt_first and clt_first.strip():
        clt_name_parts.append(clt_first.strip())
    if clt_last and clt_last.strip():
        clt_name_parts.append(clt_last.strip())
    
    clt_name = ' '.join(clt_name_parts) if clt_name_parts else "Not Provided"
    
    print(f"DEBUG - Page 3 - Formatted care_name: '{care_name}'")
    print(f"DEBUG - Page 3 - Formatted clt_name: '{clt_name}'")
    
    html = '<div>'
    
    html += '''
    <p style="text-align: center; font-weight:700; font-size: 16pt; font-family: Calibri; font-style: normal; text-decoration: underline; margin:5px 0;"><b>Authorization for a Repeating Electronic Funds Transfer</b></p>
    <p style="text-align: center; font-weight:400; font-size: 10pt; font-family: Calibri; font-style: normal; margin:2px 0;">(Save time and postage. Avoid interest charges, late payments, and termination notices)</p>
    '''
    
    html += f'''
    <p style="font-weight:400; font-size: 10pt; font-family: Calibri; font-style: normal; margin:5px 0; line-height:1.3;">I, the undersigned, acknowledge that invoices prepared by Options for Senior America (Options) are due upon receipt, and therefore hereby authorize Options to withdraw any amounts owed by me on the same day as the invoice is prepared and emailed to me. This funds withdrawal is made by initiating an electronic funds transfer, as a debit through ACH (Automated Clearing House) from my account at the financial institution (hereinafter "Bank") indicated below. I also agree that, in the event the below mentioned care recipient passes away, I will not close this referenced bank account until I receive notification from Options that the final Options invoice is paid in full using the method of payment herein described. Furthermore, I authorize Bank to accept and to debit entries indicated by Options from my account.</p>
    
    <p style="font-weight:400; font-size: 10pt; font-family: Calibri; font-style: normal; margin:3px 0; line-height:1.3;">This authorization is to remain in full force and effect until Options and Bank have received written notice from me of its termination in such time and in such manner as to afford Options and Bank reasonable opportunity to act on it.</p>
    
    <p style="font-weight:400; font-size: 10pt; font-family: Calibri; font-style: normal; margin:8px 0 3px 30px;">Care Recipient Name:&nbsp;&nbsp;<b>{care_name}</b></p>
    
    <p style="font-weight:400; font-size: 10pt; font-family: Calibri; font-style: normal; margin:3px 0 3px 30px;">Client Bank Account Signatory Name:&nbsp;&nbsp;<b>{clt_name}</b></p>
    
    <p style="font-weight:400; font-size: 10pt; font-family: Calibri; font-style: normal; margin:3px 0 3px 30px;">Client Signature:&nbsp;&nbsp;_______________________________________</p>
    
    <p style="font-weight:400; font-size: 10pt; font-family: Calibri; font-style: normal; margin:3px 0 5px 30px;">Date:&nbsp;&nbsp;<b>{datetime.now().strftime("%m/%d/%Y")}</b></p>
    
    <p style="font-weight:700; font-size: 12pt; font-family: Calibri; font-style: normal; margin:5px 0 5px 30px;">&nbsp;&nbsp;****************************************************************</p>
    
    <p style="font-weight:700; font-size: 12pt; font-family: Calibri; font-style: normal; margin:5px 0 3px 30px; text-decoration: underline;"><b>Account Information</b></p>
    
    <p style="font-weight:400; font-size: 10pt; font-family: Calibri; font-style: normal; margin:3px 0 3px 30px;">Bank Name, City, and State:&nbsp;&nbsp;_____________________________</p>
    
    <p style="font-weight:400; font-size: 10pt; font-family: Calibri; font-style: normal; margin:3px 0 3px 30px;">Routing Transit #:&nbsp;&nbsp;_________________________________</p>
    
    <!-- Account Type with square boxes in front - Using the same style as OPTIONS logo -->
    <p style="font-weight:400; font-size: 10pt; font-family: Calibri; font-style: normal; margin:3px 0 3px 30px;">
        <table style="margin:0; padding:0; border-collapse: collapse;">
            <tr>
                <td style="font-weight:400; white-space: nowrap;">Account Type:&nbsp;&nbsp;&nbsp;&nbsp;</td>
                <td style="white-space: nowrap;">
                    <table style="display: inline-table; margin-right: 20px; border-collapse: collapse;">
                        <tr>
                            <td style="border: 1px solid #000000; width: 12px; height: 12px; padding: 0; background-color: white;"></td>
                            <td style="padding-left: 5px ; font-size:24pt;">Checking</td>
                        </tr>
                    </table>
                </td>
                <td style="white-space: nowrap;">
                    <table style="display: inline-table; border-collapse: collapse;">
                        <tr>
                            <td style="border: 1px solid #000000; width: 12px; height: 12px; padding: 0; background-color: white;"></td>
                            <td style="padding-left: 5px; font-size:24pt">Saving</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </p>
    
    <div style="margin:10px 30px; text-align: center; font-weight:400; font-size: 10pt; padding:40px; border: 3px double #000;"><b>----------Please Attach a Voided Check Here----------</b></div>
    '''
    
    html += '</div>'
    return html