"""Page 1 Continuation - Additional Terms (matches dynamic_sa_page1_cont.php)"""
from datetime import datetime

def generate_page1_cont(data):
    """
    Generate Page 1 Continuation HTML - matches dynamic_sa_page1_cont.php logic
    """
    # Create a copy of data to avoid modifying the original
    clean_data = data.copy() if data else {}
    
    # Filter out any "BA" from string values in the data
    for key, value in clean_data.items():
     if key == 'branch_code':  # Skip this one!
        continue
    if isinstance(value, str):
        clean_data[key] = value.replace('BA', '').replace('ba', '')
    # Get values directly from cleaned data
    branch = clean_data.get('branch_code', '').lower()
    branch_data = clean_data.get('branch_data', {})
    care_state = clean_data.get('care_state', '').upper()
    
    # Get client information directly from cleaned data
    clt_first = clean_data.get('clt_first_name', '')
    clt_last = clean_data.get('clt_last_name', '')
    
    # Fix: Handle empty relationship properly
    clt_relationship = clean_data.get('clt_relationship', '')
    if not clt_relationship or clt_relationship.strip() == '':
        clt_relationship = 'Self'
        print(f"DEBUG - page1_cont - Setting default relationship to: '{clt_relationship}'")
    
    handled_by = clean_data.get('handled_by', '')
    
    # Get current date for signature
    current_date = datetime.now().strftime("%m/%d/%Y")
    
    # Get mileage rate
    mileage_rate = 0.67
    if branch_data and 'Mileage' in branch_data:
        try:
            mileage_rate = float(branch_data['Mileage'])
            print(f"Using branch_data.Mileage: {mileage_rate}")
        except (ValueError, TypeError):
            pass
    else:
        mileage_rate_raw = clean_data.get('mileage_rate', 0.67)
        try:
            mileage_rate = float(mileage_rate_raw)
        except (ValueError, TypeError):
            mileage_rate = 0.67

    html = '<div style="font-family: Arial, sans-serif;">'  # Added font family for better readability
    
    # Test branch live-in services
    if branch in ['testhomecare', 'testhomecare_staging']:
        html += '''
        <div style="font-size:12px;margin-top:8px;line-height:1.4;">
            <p style="margin:5px 0;"><b><u>LIVE-IN SERVICES AND CARE PROVIDER SCHEDULE:</u></b> &nbsp; OPTIONS care providers who provide live-in services have a standard work schedule of twelve (12) hours per each twenty-four hour day. This accounts for eight (8) hours of sleep (five (5) of which must be uninterrupted), and four (4) hours for meals and breaks. During this twelve (12) hour period, the care provider is considered off-duty, and must be provided with adequate, private, and sanitary accommodations. In the event the care recipient requests our live-in care provider to provide services during an off-duty period, then you will be responsible for additional charges, beyond the daily live-in rate, at our standard hourly rate times the number of hours worked during the interruption period. If, as a result of such request, our care provider is unable to rest for an uninterrupted five (5) hours, then you will be billed at our standard hourly rate for the entire eight (8) hour sleep time period.</p>
        </div>
        '''
    
    # Get top margin based on branch
    top_margin = get_top_margin_cont(branch)
    
    # Needs Assessment & Valuables for specific branches
    needs_assessment_branches = [
        'athomecare', 'athomecare_staging', 'scgahomecare', 'scgahomecare_staging', 
        'tahomecare', 'tahomecare_staging', 'woflhomecare', 'woflhomecare_staging', 
        'dchomecare', 'dchomecare_staging', 'bahomecare', 'bahomecare_staging', 
        'lphomecare', 'lphomecare_staging', 'amfvahomecare', 'amfvahomecare_staging', 
        'nvahomecarearchive', 'rihomecare', 'rihomecare_staging', 'cfairfaxhomecare', 
        'cfairfaxhomecare_staging', 'sfvahomecare', 'sfvahomecare_staging', 
        'chazhomecare', 'chazhomecare_staging', 'hbhomecare', 'hbhomecare_staging', 
        'nspahomecare', 'nspahomecare_staging', 'lzflhomecare', 'lzflhomecare_staging', 
        'blmdhomecare', 'blmdhomecare_staging', 'wpbflhomecare', 'wpbflhomecare_staging'
    ]
    
    if branch in needs_assessment_branches:
        html += f'''
        <div style="font-size:12px;margin-top:{top_margin};line-height:1.4;">
            <p style="margin:5px 0;"><b><u>NEEDS ASSESSMENT & PLAN OF CARE:</u></b> &nbsp; When a Needs Assessment and a Plan of Care is conducted by Options staff, the associated $95 fee is waived for any ongoing case that requires more than thirty (30) service hours per week. Otherwise, this fee is included on the Options invoice.</p>
        </div>
        <div style="font-size:12px;margin-top:{top_margin};line-height:1.4;">
            <p style="margin:5px 0;"><b><u>YOUR VALUABLES:</u></b> &nbsp; Our care providers are not authorized to accept payments directly, nor to have use or custody of any valuables belonging to you (credit cards, checkbooks, cash, and the like). Common sense dictates that you be careful with such valuables, and alert OPTIONS and the police should you notice a loss.</p>
        </div>
        '''
    
    # Notice Period
    if branch in ['hbhomecare', 'hbhomecare_staging', 'nspahomecare', 'nspahomecare_staging']:
        html += f'''
        <div style="font-size:12px;margin-top:{top_margin};line-height:1.4;">
            <p style="margin:5px 0;"><b><u>NOTICE PERIOD:</u></b> &nbsp; The care recipient or his/her designees are not obligated to give a written notice of termination. OPTIONS may end services under this agreement by giving at least 10 calendar days advance written notice of the intent to terminate services. Less than 10 days advance written notice may be provided by OPTIONS in the event the client has failed to pay for services, despite notice, and the client is more than 14 days in arrears, or if the health and welfare of the OPTIONS caregiver is at risk.</p>
        </div>
        '''
    else:
        html += f'''
        <div style="font-size:12px;margin-top:{top_margin};line-height:1.4;">
            <p style="margin:5px 0;"><b><u>NOTICE PERIOD:</u></b> &nbsp; The care recipient or his/her designees are not obligated to give a written notice of termination. OPTIONS may end services under this agreement by giving 3 calendar days notice in writing.</p>
        </div>
        '''
    
    # Medication Administration
    med_branches = [
        'athomecare', 'athomecare_staging', 'scgahomecare', 'scgahomecare_staging', 
        'clhomecare', 'clhomecare_staging', 'ciohhomecare', 'ciohhomecare_staging',
        'nvahomecare', 'nvahomecare_staging', 'rihomecare', 'rihomecare_staging', 
        'tahomecare', 'tahomecare_staging', 'mnhomecare', 'mnhomecare_staging',
        'lovahomecare', 'lovahomecare_staging', 'sfvahomecare', 'sfvahomecare_staging', 
        'lkinhomecare', 'lkinhomecare_staging', 'shmihomecare', 'shmihomecare_staging', 
        'wfvahomecare', 'wfvahomecare_staging', 'cfairfaxhomecare', 'cfairfaxhomecare_staging', 
        'amfvahomecare', 'amfvahomecare_staging', 'woflhomecare', 'woflhomecare_staging', 
        'nspahomecare', 'nspahomecare_staging', 'lzflhomecare', 'lzflhomecare_staging'
    ]
    
    if branch in med_branches:
        html += f'''
        <div style="font-size:12px;margin-top:{top_margin};line-height:1.4;">
            <p style="margin:5px 0;"><b><u>ADMINISTERING MEDICATION:</u></b> &nbsp; For those care recipients who require administration of medication, if the care recipient is not cognitively competent, and a family member is unavailable to administer the medication on a weekly basis, we will assign an RN or CMT to make weekly visits to administer and dispense the medication at the rate of $75/visit.</p>
        </div>
        '''
    
    # DC branch special case
    if branch in ['dchomecare', 'dchomecare_staging'] and care_state == "DC":
        html += f'''
        <div style="font-size:12px;margin-top:{top_margin};line-height:1.4;">
            <p style="margin:5px 0;"><b><u>ADMINISTERING MEDICATION:</u></b> &nbsp; For those care recipients who require administration of medication, if the care recipient is not cognitively competent, and a family member is unavailable to administer the medication on a weekly basis, we will assign an RN or CMT to make weekly visits to administer and dispense the medication at the rate of $75/visit.</p>
        </div>
        '''
    
    # Common sections for all branches
    html += f'''
        <div style="font-size:12px;margin-top:{top_margin};line-height:1.4;">
            <p style="margin:5px 0;"><b><u>OUR CARE PROVIDERS CANNOT BE HIRED BY YOU:</u></b> &nbsp; You understand that OPTIONS is not a staffing agency and acknowledge the substantial effort and expense incurred by OPTIONS in screening, interviewing, and recruiting care providers. The care providers we introduce to you are not, under any circumstance, to become employed by you, whether per your request or theirs, and whether during or after using our services. If you wish to employ our care provider after a one year period of care provider's termination of employment with you, you agree to pay OPTIONS the larger of a lump-sum placement fee of nine thousand dollars ($9,000) or the value of eight (8) weeks of service charges based on the frequency of visits and the fees as stipulated in this agreement. This amount will be due in 10 calendar days from the date our care provider begins employment with you.</p>
        </div>
        
        <div style="font-size:12px;margin-top:{top_margin};line-height:1.4;">
            <p style="margin:5px 0;"><b><u>RECORD KEEPING:</u></b> &nbsp; It is standard policy and practice at OPTIONS that each care provider keeps track of their time worked and the tasks provided on a Daily Progress Notes form. You and the care recipient must allow OPTIONS care providers reasonable time to complete this form which must be signed by you or the care recipient each week. If you and the care recipient do not wish to sign this form, you must tell OPTIONS in writing. In this instance, the form will continue to be filled out by the care provider, and the lack of your or the care recipient's signature does not constitute a reason to dispute the hours worked or the completed tasks by the care provider.</p>
        </div>
        
        <div style="font-size:12px;margin-top:{top_margin};line-height:1.4;">
            <p style="margin:5px 0;"><b><u>MILEAGE REIMBURSEMENT:</u></b> &nbsp; Mileage will be charged at the rate of ${mileage_rate:.2f} per mile when the Care Provider is required to use their personal vehicle in order to perform required duties such as errands, shopping, appointments, etc. for the Care Recipient. When the Care Provider utilizes the Care Recipient's vehicle to perform the above mentioned duties, there will be no mileage reimbursement charge.</p>
        </div>
    '''
    
    # Vehicle authorization - different for GA/SC branches
    if branch in ['scgahomecare', 'scgahomecare_staging', 'athomecare', 'athomecare_staging']:
        html += f'''
        <div style="font-size:12px;margin-top:{top_margin};line-height:1.4;">
            <p style="margin:5px 0;"><b><u>USE OF FAMILY VEHICLE:</u></b> &nbsp; If you wish to authorize our care providers to drive your/the care recipient’s vehicle and hold Options and its care providers harmless and release them from any associated liability, please check the “Yes” box and place your initials next to it, or otherwise check the “No” box and place your initials next to it.&nbsp;&nbsp;<input type="checkbox" style="width:12px;height:12px;"> Yes _______&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="checkbox" style="width:12px;height:12px;"> No _______</p>
        </div>
        '''
    else:
        html += f'''
        <div style="font-size:12px;margin-top:{top_margin};line-height:1.4;">
            <p style="margin:5px 0;"><b><u>USE OF FAMILY VEHICLE:</u></b> &nbsp; If you wish to authorize our care providers to drive your/the care recipient's vehicle and hold Options and its care providers harmless and release them from any associated liability, please write "Authorized" here and initial: _______________________</p>
        </div>
        '''
    
    # General Provisions - Governing State
    gen_prov_state = get_governing_state(branch)
    html += f'''
    <div style="font-size:12px;margin-top:{top_margin};line-height:1.4;">
        <p style="margin:5px 0;"><b><u>GENERAL PROVISIONS:</u></b></p>
        <ol type="a" style="padding-left: 25px; margin:5px 0;">
            <li style="margin-bottom:3px;">The waiver by Options of a breach of any provision of this Agreement shall not be construed as a waiver of any other provision of this Agreement or of any future breach of the provision so waived.</li>
            <li style="margin-bottom:3px;">No change, modification, termination, or attempted waiver of any of the provisions of this Agreement shall be binding upon Options or the undersigned unless put in writing and signed by Options and the undersigned.</li>
            <li style="margin-bottom:3px;">This Agreement shall be governed by the laws of the state of {gen_prov_state}.</li>
            <li style="margin-bottom:3px;">This Agreement supersedes all prior agreements and understandings, oral or written, between Options and the undersigned with respect to the subject matter hereof.</li>
        </ol>
    </div>
    '''
    
    # Signature section based on branch - with page break avoidance
    html += '<div style="page-break-inside: avoid; margin-top: 15px;">'
    
    if branch in ['athomecare', 'athomecare_staging', 'scgahomecare', 'scgahomecare_staging']:
        html += get_signature_3col_cont(clt_first, clt_last, clt_relationship, handled_by, current_date)
    else:
        html += get_signature_2col_cont(clt_first, clt_last, clt_relationship, current_date)
    
    html += '</div>'
    html += '</div>'
    return html

def get_top_margin_cont(branch):
    """Get top margin for continuation page"""
    margin_7px_branches = [
        'mnhomecare', 'mnhomecare_staging', 'lovahomecare', 'lovahomecare_staging',
        'amfvahomecare', 'amfvahomecare_staging', 'woflhomecare', 'woflhomecare_staging',
        'lzflhomecare', 'lzflhomecare_staging'
    ]
    return "8px" if branch in margin_7px_branches else "12px"

def get_governing_state(branch):
    """Get governing state based on branch"""
    branch_lower = branch.lower()
    
    if branch_lower in ['gbhomecare', 'gbhomecare_staging', 'rdhomecare', 'rdhomecare_staging']:
        return "North Carolina"
    elif branch_lower in ['scgahomecare', 'scgahomecare_staging']:
        return "Georgia"
    elif branch_lower in ['mnhomecare', 'mnhomecare_staging', 'cfairfaxhomecare', 'cfairfaxhomecare_staging', 
                          'lovahomecare', 'lovahomecare_staging', 'wfvahomecare', 'wfvahomecare_staging',
                          'amfvahomecare', 'amfvahomecare_staging', 'sfvahomecare', 'sfvahomecare_staging']:
        return "Commonwealth of Virginia"
    elif branch_lower in ['ciohhomecare', 'ciohhomecare_staging']:
        return "Ohio"
    elif branch_lower in ['nspahomecare', 'nspahomecare_staging']:
        return "Pennsylvania"
    elif branch_lower in ['lkinhomecare', 'lkinhomecare_staging']:
        return "Indiana"
    elif branch_lower in ['wenjhomecare', 'wenjhomecare_staging']:
        return "New Jersey"
    elif branch_lower in ['chazhomecare', 'chazhomecare_staging']:
        return "Arizona"
    elif branch_lower in ['wpbflhomecare', 'wpbflhomecare_staging', 'lzflhomecare', 'lzflhomecare_staging']:
        return "Florida"
    else:
        return "Maryland"

def get_signature_3col_cont(clt_first, clt_last, clt_relationship, handled_by, current_date):
    """3-column signature for GA/SC branches on continuation page"""
    return f'''
    <p style="font-size:12px;margin:10px 0 5px;line-height:1.4;text-align:center;"><b><i>I have read and agree to the above listed terms, and understand that this agreement is a contract under seal.</i></b></p>
    <table width="100%" style="font-size:12px;margin-top:5px; border-collapse: collapse;">
        <tr>
            <td style="padding-left:10px;" width="33.33%">
                <p style="margin:0;"><b>{clt_first} {clt_last}</b></p>
                <div style="border-top:1.5px solid black; width:90%; margin:5px auto;"></div>
                <p style="margin:2px 0 0 0; text-align:center;">Name of Responsible Party</p>
            </td>
            <td style="padding-left:5px;" width="33.33%">
                <p style="margin:0;"><b>{clt_relationship}</b></p>
                <div style="border-top:1.5px solid black; width:90%; margin:5px auto;"></div>
                <p style="margin:2px 0 0 0; text-align:center;">Relationship to Care Recipient</p>
            </td>
            <td style="padding-left:5px;" width="33.33%">
                <p style="margin:0;"><b>{handled_by}</b></p>
                <div style="border-top:1.5px solid black; width:90%; margin:5px auto;"></div>
                <p style="margin:2px 0 0 0; text-align:center;">Options Representative</p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding-top:10px;">
                <div style="border-top:1.5px solid black; width:70%; margin:5px auto 0;"></div>
                <p style="margin:2px 0 0 0;">Signature &nbsp; &nbsp; (SEAL)</p>
            </td>
            <td align="center" style="padding-top:10px;">&nbsp;</td>
            <td align="center" style="padding-top:10px;">
                <div style="border-top:1.5px solid black; width:70%; margin:5px auto 0;"></div>
                <p style="margin:2px 0 0 0;">Signature</p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding-top:10px;">
                <div style="border-top:1.5px solid black; width:70%; margin:0 auto;"></div>
                <p style="margin:2px 0 0 0;">Date: {current_date}</p>
            </td>
            <td align="center" style="padding-top:10px;">&nbsp;</td>
            <td align="center" style="padding-top:10px;">
                <div style="border-top:1.5px solid black; width:70%; margin:0 auto;"></div>
                <p style="margin:2px 0 0 0;">Date: {current_date}</p>
            </td>
        </tr>
    </table>
    '''

def get_signature_2col_cont(clt_first, clt_last, clt_relationship, current_date):
    """2-column signature for most branches on continuation page"""
    return f'''
    <p style="font-size:12px;margin:10px 0 5px;line-height:1.4;text-align:center;"><b><i>I have read and agree to the above listed terms, and understand that this agreement is a contract under seal.</i></b></p>
    <table width="100%" style="font-size:12px;margin-top:5px; border-collapse: collapse;">
        <tr>
            <td align="center" width="50%" style="padding-right:5px;">
                <p style="margin:0;"><b>{clt_first} {clt_last}</b></p>
                <div style="border-top:1.5px solid black; width:80%; margin:5px auto;"></div>
                <p style="margin:2px 0 0 0;">Name of Responsible Party</p>
            </td>
            <td align="center" width="50%" style="padding-left:5px;">
                <p style="margin:0;"><b>{clt_relationship}</b></p>
                <div style="border-top:1.5px solid black; width:80%; margin:5px auto;"></div>
                <p style="margin:2px 0 0 0;">Relationship to Care Recipient</p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding-top:10px;">
                <p style="margin:0;">(SEAL)</p>
                <div style="border-top:1.5px solid black; width:60%; margin:5px auto 0;"></div>
                <p style="margin:2px 0 0 0;">Signature</p>
            </td>
            <td align="center" style="padding-top:10px;">
                <div style="border-top:1.5px solid black; width:60%; margin:5px auto 0;"></div>
                <p style="margin:2px 0 0 0;">Date: {current_date}</p>
            </td>
        </tr>
    </table>
    '''