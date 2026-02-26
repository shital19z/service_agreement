"""Page 1 - Main Service Agreement"""
from datetime import datetime
from config import Config  

def generate_page1(data):
    """
    Generate Page 1 HTML - Complete with all PHP logic
    """
   
    
    # Get branch for conditional logic
    branch = data.get('branch_code', '').lower()
    
    # Get values
    clt_title = data.get('clt_title', '')
    clt_first = data.get('clt_first_name', '')
    clt_last = data.get('clt_last_name', '')
    clt_address = data.get('clt_address', '')
    clt_city = data.get('clt_city', '')
    clt_state = data.get('clt_state', '')
    clt_zip = data.get('clt_zip', '')
    
    # Fix: Handle empty relationship properly
    clt_relationship = data.get('clt_relationship', '')
    if not clt_relationship or clt_relationship.strip() == '':
        clt_relationship = 'Self'
        print(f"DEBUG - Setting default relationship to: '{clt_relationship}'")
    
    handled_by = data.get('handled_by', '')
    perc_charged = data.get('PercCharged', '100')
    
    # DEBUG: Print relationship value
    print(f"DEBUG - Page 1 - Relationship value after fix: '{clt_relationship}'")
    
    care_title = data.get('care_title', '')
    care_first = data.get('care_first_name', '')
    care_last = data.get('care_last_name', '')
    care_address = data.get('care_recipient_address', '')
    care_city = data.get('care_city', '')
    care_state = data.get('care_state', '')
    care_zip = data.get('care_zip', '')
    
    # Check if client and care recipient are the same person
    care_first_clean = care_first.strip().lower() if care_first else ''
    care_last_clean = care_last.strip().lower() if care_last else ''
    clt_first_clean = clt_first.strip().lower() if clt_first else ''
    clt_last_clean = clt_last.strip().lower() if clt_last else ''
    
    same_person = (care_first_clean and care_last_clean and 
                   care_first_clean == clt_first_clean and 
                   care_last_clean == clt_last_clean)
    
    # For the same person, use the client's title for the care recipient display
    display_care_title = clt_title if same_person else care_title
    if same_person:
        print(f"DEBUG - Same person detected in page1, using client title '{clt_title}' for care recipient")
    
    # Date fields
    initial_inquiry = data.get('initial_inquiry_date', '')
    agreement_date = data.get('agreement_date', '')
    start_date = data.get('start_date', '')
    start_time = data.get('services_start_time', '12:00 pm')
    instructions_by = data.get('instructions_given_by', f"{clt_first} {clt_last}")
    
    # Service fields
    care_type = data.get('care_type', '')
    frequency = data.get('frequency_duration', '')
    hourly_rate = float(data.get('hourly_rate', 0))
    hazards = data.get('hazards', '')
    
    # ===== FIXED: LOGO PATH USING CONFIG =====
    # Get logo path from config instead of data
    logo_path = Config.get_logo_path()
    if not logo_path:
        print("⚠️ Warning: Logo not found, using empty string")
        logo_path = ''  # Empty string if logo not found
    
    # Get current date for signature
    current_date = datetime.now().strftime("%m/%d/%Y")
    
    # ===== OFFICE ADDRESS LOGIC (from PHP) =====
    office_addr = get_office_address(branch, data)
    
    # ===== TOP MARGIN LOGIC (from PHP) =====
    top_margins = get_top_margin(branch)
    
    # Build names
    resp_name = f"{clt_title} {clt_first} {clt_last}".strip()
    if not resp_name or resp_name == '  ':
        resp_name = "Not Provided"
    
    # Use display_care_title for care recipient name
    care_name_parts = []
    if display_care_title and display_care_title.strip():
        care_name_parts.append(display_care_title.strip())
    if care_first and care_first.strip():
        care_name_parts.append(care_first.strip())
    if care_last and care_last.strip():
        care_name_parts.append(care_last.strip())
    
    care_name = ' '.join(care_name_parts) if care_name_parts else "Not Provided"
    
    care_full_address = f"{care_address}, {care_city}, {care_state} {care_zip}".strip(', ')
    if not care_full_address or care_full_address == ', ,  ':
        care_full_address = "Not Provided"
    
    # Build the HTML with REDUCED SPACING
    html = f'''
    <div>    
        <!-- Header table - 2 columns -->
        <table width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse;">
            <tr>
                <td width="25%" align="center" valign="top">
                    <p style="font-size:10px; margin:0; line-height:1.2;">{office_addr}</p>
                </td>
                <td width="70%" align="right" valign="top">
                    <img style="width:2.0833in;height:0.9166in;" src="{logo_path}" />
                </td>
                <td width="5%"></td>
            </tr>
        </table>
        
        <!-- Main info table - 3 columns with reduced padding -->
        <table width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse; margin-top: 5px;">
            <tr>
                <td width="30%" style="padding-top: 5px;">
                    <p style="font-size:14px; margin:0; line-height:1.2;">
                        <u>Name Address of Responsible Party</u><br>
                        <b>
                        {data.get('clt_title', '')} {data.get('clt_first_name', '')} {data.get('clt_last_name', '')}<br>
                        {data.get('clt_address', '')}<br>
                        </b>               
                    </p>
                </td>
                <td width="40%" style="padding-top: 5px;" align="center" valign="bottom"></td>
                <td width="30%" style="padding-top: 5px;" align="left" valign="middle">
                    <p style="font-size:14px; margin:0;">Date: <b>{agreement_date}</b></p>
                </td>
            </tr>
            <tr>
                <td colspan="3" style="text-align: center; padding-top: 5px;" align="center" valign="bottom">
                    <p style="font-size:14px; margin:0; font-weight:bold;">SERVICE AGREEMENT</p>
                </td>
            </tr>
            <tr>
                <td width="65%" style="padding-top: 5px; font-size:14px;" valign="top">
                    <p style="margin:0;">For Care Recipient: <b>{care_name}</b></p>
                </td>
                <td colspan="2" width="35%" style="padding-top: 5px; font-size:14px;" valign="top">
                    <p style="margin:0;">residing at &nbsp; <b>{care_full_address}</b></p>
                </td>
            </tr>
        </table>
    '''
    
    # ===== TABLE STRUCTURE LOGIC (from PHP) =====
    if branch in ['scgahomecare', 'scgahomecare_staging', 'athomecare', 'athomecare_staging']:
        # 6-column table for SC/GA
        initial_contact = data.get('inicontactdate', '')
        html += f'''
        <!-- 6-column table for SC/GA branches -->
        <table width="95%" cellspacing="0" cellpadding="0" border="1" style="margin-top:5px; font-size:14px; border-collapse: collapse;">
            <tr>
                <td width="13%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;">Referral date</p></td>
                <td width="16%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;">Initial Contact with Client</p></td>
                <td width="33%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;">Start Order and/or Instructions Given by</p></td>
                <td width="13%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;">On</p></td>
                <td width="13%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;">Services to Start on</p></td>
                <td width="12%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;">At (time)</p></td>
            </tr>
            <tr>
                <td width="13%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;"><b>{initial_inquiry}</b></p></td>
                <td width="16%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;"><b>{initial_contact}</b></p></td>
                <td width="33%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;"><b>{instructions_by}</b></p></td>
                <td width="13%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;"><b>{agreement_date}</b></p></td>
                <td width="13%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;"><b>{start_date}</b></p></td>
                <td width="12%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;"><b>{start_time}</b></p></td>
            </tr>
        </table>
        '''
    else:
        # 5-column table for others
        html += f'''
        <!-- 5-column table for standard branches -->
        <table width="95%" cellspacing="0" cellpadding="0" border="1" style="margin-top:5px; font-size:14px; border-collapse: collapse;">
            <tr>
                <td width="16%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;">Initial Inquiry date</p></td>
                <td width="36%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;">Start Order and/or Instructions Given by</p></td>
                <td width="16%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;">On</p></td>
                <td width="16%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;">Services to Start on</p></td>
                <td width="16%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;">At (time)</p></td>
            </tr>
            <tr>
                <td width="16%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;"><b>{initial_inquiry}</b></p></td>
                <td width="36%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;"><b>{instructions_by}</b></p></td>
                <td width="16%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;"><b>{agreement_date}</b></p></td>
                <td width="16%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;"><b>{start_date}</b></p></td>
                <td width="16%" align="center" style="border:1px solid black; padding:2px;"><p style="margin:0;"><b>{start_time}</b></p></td>
            </tr>
        </table>
        '''
    
    # Required Services
    blank_div = '<div style="height:5px"> &nbsp; </div>'
    req_services = care_type or blank_div
    
    html += f'''
        <div style="font-size:12px;margin-top:{top_margins};line-height:1.3;">
            <p style="margin:2px 0;"><b><u>REQUIRED SERVICES:</u></b> &nbsp; In addition to the general services that our caregivers provide such as assistance with activities of daily living, meal preparation, light housekeeping, and laundry, the required services as stated by the responsible party/client are:</p>
            <p style="margin:2px 0;">{req_services}</p>
        </div>
        
        <div style="font-size:12px;margin-top:{top_margins};line-height:1.3;">
            <p style="margin:2px 0;"><b><u>FREQUENCY DURATION OF VISITS:</u></b></p>
            <p style="margin:2px 0;">{frequency}</p>
        </div>
        
        <div style="font-size:12px;margin-top:{top_margins};line-height:1.3;">
            <p style="margin:2px 0;"><b><u>FEES:</u></b></p>
            <p style="margin:2px 0;">${hourly_rate:.2f}/hr</p>
        </div>
    '''
    
    # Hazards section (from PHP)
    hazards_branches = [
        'nvahomecare', 'nvahomecare_staging', 'rihomecare', 'rihomecare_staging', 
        'mnhomecare', 'mnhomecare_staging', 'lovahomecare', 'lovahomecare_staging',
        'wfvahomecare', 'wfvahomecare_staging', 'cfairfaxhomecare', 'cfairfaxhomecare_staging'
    ]
    if branch in hazards_branches and hazards:
        html += f'''
        <div style="font-size:12px;margin-top:{top_margins};line-height:1.3;">
            <p style="margin:2px 0;"><b><u>HAZARDS:</u></b></p>
            <p style="margin:2px 0;">{hazards}</p>
        </div>
        '''
    
    # Caregiver competency (from PHP)
    if branch in ['hbhomecare', 'hbhomecare_staging']:
        html += f'''
        <div style="font-size:12px;margin-top:{top_margins};line-height:1.3;">
            <p style="margin:2px 0;"><b><u>CAREGIVER COMPETENCY REQUIREMENTS:</u></b></p>
            <p style="margin:2px 0;">Before assigning a Direct Care Worker to provide services to a consumer, Options shall ensure that the Direct Care Worker has obtained a valid nurse's aide license in Pennsylvania, or has successfully completed a training program as stipulated in Pennsylvania's regulations, section 611.55, item 3.</p>
        </div>
        '''
    
    # Charges section with percentage logic (from PHP)
    html += f'<div style="font-size:12px;margin-top:{top_margins};line-height:1.3;"><p style="margin:2px 0;"><b><u>CHARGES:</u></b> &nbsp;'
    
    perc_branches = [
        'nvahomecare', 'nvahomecare_staging', 'rihomecare', 'rihomecare_staging',
        'mnhomecare', 'mnhomecare_staging', 'lovahomecare', 'lovahomecare_staging'
    ]
    if branch in perc_branches:
        html += f'{perc_charged}% of the fees will be charged to {clt_first} {clt_last}<br>'
    
    if branch in ['test2homecare', 'test2homecare_staging']:
        html += 'OPTIONS will invoice in advance; monthly or bi-monthly. Any prepaid amount at the end of our services will be FULLY REFUNDABLE. RN assessment fee is charged at $100.00 per quarter.</p></div>'
    else:
        html += 'We bill bi-weekly for services rendered during the prior two weeks. If service hours are 80 hours or more per week, and for all 7-day live-in cases, billing will be done weekly. Payments are due upon receipt of OPTIONS invoices.</p></div>'
    
    # Payment obligations
    html += f'''
        <div style="font-size:12px;margin-top:{top_margins};line-height:1.3;">
            <p style="margin:2px 0;"><b><u>PAYMENT OBLIGATIONS:</u></b> &nbsp; The parties responsible for payment include the person who initiates arrangements for our services, as well as the care recipient and the care recipient's power of attorney or guardian. The responsibility for payment cannot be shifted simply by asking us to bill an insurance company or a third party. Your responsibility extends to making timely and prompt payments at all times. In the event the client or care recipient cancels a shift with less than 24-hour notice, then a charge for our minimum 2-hour visit will apply.</p>
        </div>
    '''
    
    # Federal holidays with 12-day logic for mnhomecare (from PHP)
    if branch in ['mnhomecare', 'mnhomecare_staging']:
        html += f'''
        <div style="font-size:12px;margin-top:{top_margins};line-height:1.3;">
            <p style="margin:2px 0;"><b><u>FEDERAL HOLIDAYS:</u></b> &nbsp; When services are required on Federal holidays, you will be charged "time and a half" for those days (50% more than your usual daily charge). We apply those surcharges on the 12 holidays as follows: New Year's Day, Martin Luther King Day, Presidents' Day, Easter Sunday, Memorial Day, Juneteenth Day, Independence Day, Labor Day, Columbus Day, Veterans' Day, Thanksgiving Day, and Christmas Day.</p>
        </div>
        '''
    else:
        html += f'''
        <div style="font-size:12px;margin-top:{top_margins};line-height:1.3;">
            <p style="margin:2px 0;"><b><u>FEDERAL HOLIDAYS:</u></b> &nbsp; When services are required on Federal holidays, you will be charged "time and a half" for those days (50% more than your usual daily charge). We apply those surcharges on the 11 holidays as follows: New Year's Day, Martin Luther King Day, Presidents' Day, Memorial Day, Juneteenth Day, Independence Day, Labor Day, Columbus Day, Veterans' Day, Thanksgiving Day, and Christmas Day.</p>
        </div>
        '''
    
    # Live-in services (from PHP) - with condensed text
    live_in_branches = [
        'anhomecare', 'anhomecare_staging', 'athomecare', 'athomecare_staging', 'bahomecare', 'bahomecare_staging',
        'blhomecare', 'blhomecare_staging', 'dchomecare', 'dchomecare_staging', 'fkhomecare', 'fkhomecare_staging',
        'lphomecare', 'lphomecare_staging', 'testhomecare', 'clhomecare', 'clhomecare_staging', 'ciohhomecare', 'ciohhomecare_staging',
        'nvahomecarearchive', 'nvahomecarearchive_staging', 'rihomecare', 'rihomecare_staging', 'tahomecare', 'tahomecare_staging',
        'gbhomecare', 'gbhomecare_staging', 'rdhomecare', 'rdhomecare_staging', 'mnhomecare', 'mnhomecare_staging',
        'lkinhomecare', 'lkinhomecare_staging', 'shmihomecare', 'shmihomecare_staging', 'wenjhomecare', 'wenjhomecare_staging',
        'lovahomecare', 'lovahomecare_staging', 'scgahomecare', 'scgahomecare_staging', 'hbhomecare', 'hbhomecare_staging',
        'woflhomecare', 'woflhomecare_staging', 'wfvahomecare', 'wfvahomecare_staging', 'cfairfaxhomecare', 'cfairfaxhomecare_staging',
        'sfvahomecare', 'sfvahomecare_staging', 'chazhomecare', 'chazhomecare_staging', 'amfvahomecare', 'amfvahomecare_staging',
        'nspahomecare', 'nspahomecare_staging', 'tomdhomecare', 'tomdhomecare_staging', 'lzflhomecare', 'lzflhomecare_staging',
        'wpbflhomecare', 'wpbflhomecare_staging'
    ]
    if branch in live_in_branches:
        html += f'''
        <div style="font-size:12px;margin-top:{top_margins};line-height:1.3;">
            <p style="margin:2px 0;"><b><u>LIVE-IN SERVICES AND CARE PROVIDER SCHEDULE:</u></b> &nbsp; OPTIONS care providers who provide live-in services have a standard work schedule of twelve (12) hours per each twenty-four hour day. This accounts for eight (8) hours of sleep (five (5) of which must be uninterrupted), and four (4) hours for meals and breaks. During this twelve (12) hour period, the care provider is considered off-duty, and must be provided with adequate, private, and sanitary accommodations. In the event the care recipient requests our live-in care provider to provide services during an off-duty period, then you will be responsible for additional charges, beyond the daily live-in rate, at our standard hourly rate times the number of hours worked during the interruption period. If, as a result of such request, our care provider is unable to rest for an uninterrupted five (5) hours, then you will be billed at our standard hourly rate for the entire eight (8) hour sleep time period.</p>
        </div>
        '''
    
    # Signature section - with reduced spacing
    html += '<div style="page-break-inside: avoid; margin-top: 10px;">'
    
    if branch in ['athomecare', 'athomecare_staging', 'scgahomecare', 'scgahomecare_staging']:
        html += get_signature_3col(clt_first, clt_last, clt_relationship, handled_by, current_date)
    else:
        html += get_signature_2col(clt_first, clt_last, clt_relationship, current_date)
    
    html += '</div>'  # Close the page-break-inside div
    html += '</div>'  # Close the main div from the beginning
    
    return html


# Keep all your existing helper functions (get_office_address, get_top_margin, 
# get_signature_3col, get_signature_2col) exactly as they are


def get_office_address(branch, data):
    """Get office address based on branch (from PHP)"""
    branch_lower = branch.lower()
    
    if branch_lower in ['scgahomecare', 'scgahomecare_staging']:
        return '2110 Powers Ferry Rd <br>Suite 306 <br>Atlanta, GA 30339<br>_______________________________<br>Tel: 404.634.1111 <br>Fax: 404.634.1199'
    elif branch_lower in ['gbhomecare', 'gbhomecare_staging']:
        return 'Options For Senior America<br>215 Alamance Road <br>Burlington, NC 27215<br>_______________________________<br>Tel: 336.270.6647 <br>Mobile: 336.270.6198'
    elif branch_lower in ['rdhomecare', 'rdhomecare_staging']:
        return 'Options For Senior America<br>315 East Chatham Street, Suite 201<br>Cary, NC 27511<br>_______________________________<br>Tel: 919.380.6812 <br>Mobile: 919.306.2406'
    elif branch_lower in ['mnhomecare', 'mnhomecare_staging']:
        return 'Options For Senior America<br>10432 Balls Ford Road <br>Suite 300<br>Manassas, VA 20109<br>_______________________________<br>Tel: 571.449.6781 <br>Fax: 571.921.4622'
    elif branch_lower in ['lovahomecare', 'lovahomecare_staging']:
        return 'Options For Senior America<br>13800 Coppermine Road<br>Suite 125-A<br>Herndon, VA 20171<br>_______________________________<br>Tel: 571.999.5464 <br>Fax: 571.207.7600'
    elif branch_lower in ['lkinhomecare', 'lkinhomecare_staging']:
        return 'Options for Senior America<br>8488 Georgia Street, Suite D<br>Merrillville, IN 46410<br>_______________________________<br>Tel: 219.321.9130 <br>Fax: 219.321.9133'
    elif branch_lower in ['shmihomecare', 'shmihomecare_staging']:
        return '13854 Lakeside Circle<br>Suite 250<br>Sterling Heights, MI 48313<br>_______________________________<br>Tel: 586.344.8436 <br>Fax: 586.532.5415'
    elif branch_lower in ['wenjhomecare', 'wenjhomecare_staging']:
        return '70 S. Orange Avenue<br>Suite 105<br>Livingston, NJ 07039<br>_______________________________<br>Tel: 973.803.0901 <br>Fax: 973.808.1991'
    elif branch_lower in ['wfvahomecare', 'wfvahomecare_staging']:
        return 'Options for Senior America <br>13800 Coppermine Road <br>Suite 125-B <br>Herndon, VA 20171<br>_______________________________<br>Tel: 571.999.5464 <br>Fax: 571.207.7600'
    elif branch_lower in ['cfairfaxhomecare', 'cfairfaxhomecare_staging']:
        return 'Options for Senior America <br>13800 Coppermine Road <br>Suite 125-C <br>Herndon, VA 20171<br>_______________________________<br>Tel: 571.999.5464 <br>Fax: 571.207.7600'
    elif branch_lower in ['amfvahomecare', 'amfvahomecare_staging']:
        return 'Options for Senior America <br>11350 Random Hills Road<br>Suite 800 <br>Fairfax, VA 22030<br>_______________________________<br>Tel: 571.449.6781 <br>Fax: 571.921.4622'
    elif branch_lower in ['woflhomecare', 'woflhomecare_staging']:
        return 'Options for Senior America <br>7061 Grand National Drive<br>Suite 105C <br>Orlando, FL 32819<br>_______________________________<br>Tel: 407.729.7551'
    elif branch_lower in ['chazhomecare', 'chazhomecare_staging']:
        return 'Options for Senior America <br>920 W. Chandler Blvd<br>Suite 3<br>Chandler, AZ 85225<br>_______________________________<br>Tel:  480.673.3888 <br>Fax: 888.511.8962'
    elif branch_lower in ['nspahomecare', 'nspahomecare_staging']:
        return 'Options for Senior America <br>175 Strafford Avenue<br>Suite One<br>Wayne, PA 19087<br>_______________________________<br>Tel: 610.975.4422 <br>Fax: 610.514.5560'
    elif branch_lower in ['ciohhomecare', 'ciohhomecare_staging']:
        return 'Options For Senior America <br>10925 Reed Hartman Hwy<br>Suite 310-E<br>Cincinnati, OH 45242<br>_______________________________<br>Tel: 513.928.0042 <br>Fax: 513.880.0044'
    elif branch_lower in ['sfvahomecare', 'sfvahomecare_staging']:
        return 'Options For Senior America <br>7830 Backlick Rd, Suite 200-A<br>Springfield, VA 22150<br>_______________________________<br>Tel: 571.416.8260 <br>Fax: 571.415.5460'
    elif branch_lower in ['blmdhomecare', 'blmdhomecare_staging']:
        return 'Options For Senior America<br>4690 Millennium Drive<br>Belcamp, MD 21017<br>_______________________________<br>Tel:667.450.2289<br>Fax: 667.444.4042'
    elif branch_lower in ['wpbflhomecare', 'wpbflhomecare_staging']:
        return 'Options For Senior America <br>2300 Palm Beach Lakes Blvd<br> Suite 300-A<br>West Palm Beach, FL 33409<br>_______________________________<br>Tel:  <br>Fax: '
    
    # Default corporate address
    return 'Corporate Office <br>6 Montgomery Village Avenue<br>Suite 330<br>Gaithersburg, MD 20879<br>_______________________________<br>Tel: 301.562.1100 <br>Fax: 301.562.1133'

def get_top_margin(branch):
    """Get top margin based on branch (from PHP)"""
    branch_lower = branch.lower()
    branches_with_6px = [
        'cfairfaxhomecare', 'cfairfaxhomecare_staging', 
        'wfvahomecare', 'wfvahomecare_staging',
        'scgahomecare', 'scgahomecare_staging', 
        'amfvahomecare', 'amfvahomecare_staging',
        'woflhomecare', 'woflhomecare_staging',
        'chazhomecare', 'chazhomecare_staging'
    ]
    return "6px" if branch_lower in branches_with_6px else "8px"

def get_signature_3col(clt_first, clt_last, clt_relationship, handled_by, current_date):
    """3-column signature for GA/SC branches"""
    return f'''
    <!-- 3-column signature table -->
    <table width="100%" style="font-size:11.5px; margin-top:20px; border-collapse: collapse;" cellpadding="0" cellspacing="0">
        <tr>
            <td style="padding-left:15px; padding-right:5px;" width="33%">
                <p style="margin:0;"><b>{clt_first} {clt_last}</b></p>
                <div style="border-top:2px solid black; width:100%; margin:5px auto;"></div>
                <p style="margin:2px 0 0 0; text-align:center;">Name of Responsible Party</p>
            </td>
            <td style="padding-left:5px; padding-right:5px;" width="34%">
                <p style="margin:0;"><b>{clt_relationship}</b></p>
                <div style="border-top:2px solid black; width:100%; margin:5px auto;"></div>
                <p style="margin:2px 0 0 0; text-align:center;">Relationship to Care Recipient</p>
            </td>
            <td style="padding-left:5px; padding-right:15px;" width="33%">
                <p style="margin:0;"><b>{handled_by}</b></p>
                <div style="border-top:2px solid black; width:100%; margin:5px auto;"></div>
                <p style="margin:2px 0 0 0; text-align:center;">Options Representative</p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding-top:15px;">
                <p style="margin:0;">(SEAL)</p>
                <div style="border-top:2px solid black; width:80%; margin:5px auto 0;"></div>
                <p style="margin:2px 0 0 0;">Signature</p>
            </td>
            <td align="center" style="padding-top:15px;">
                <p style="margin:0;">&nbsp;</p>
            </td>
            <td align="center" style="padding-top:15px;">
                <div style="border-top:2px solid black; width:80%; margin:5px auto 0;"></div>
                <p style="margin:2px 0 0 0;">Signature</p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding-top:15px;">
                <div style="border-top:2px solid black; width:80%; margin:0 auto;"></div>
                <p style="margin:2px 0 0 0;">Date: {current_date}</p>
            </td>
            <td align="center" style="padding-top:15px;">
                <p style="margin:0;">&nbsp;</p>
            </td>
            <td align="center" style="padding-top:15px;">
                <div style="border-top:2px solid black; width:80%; margin:0 auto;"></div>
                <p style="margin:2px 0 0 0;">Date: {current_date}</p>
            </td>
        </tr>
    </table>
    '''

def get_signature_2col(clt_first, clt_last, clt_relationship, current_date):
    """2-column signature for most branches"""
    return f'''
    <!-- 2-column signature table -->
    <table width="100%" style="font-size:12px; margin-top:20px; border-collapse: collapse;" cellpadding="0" cellspacing="0">
        <tr>
            <td align="center" width="50%" style="padding-right:10px;">
                <p style="margin:0;"><b>{clt_first} {clt_last}</b></p>
                <div style="border-top:2px solid black; width:90%; margin:5px auto;"></div>
                <p style="margin:2px 0 0 0;">Name of Responsible Party</p>
            </td>
            <td align="center" width="50%" style="padding-left:10px;">
                <p style="margin:0;"><b>{clt_relationship}</b></p>
                <div style="border-top:2px solid black; width:90%; margin:5px auto;"></div>
                <p style="margin:2px 0 0 0;">Relationship to Care Recipient</p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding-top:15px;">
                <p style="margin:0;">(SEAL)</p>
                <div style="border-top:2px solid black; width:70%; margin:5px auto 0;"></div>
                <p style="margin:2px 0 0 0;">Signature</p>
            </td>
            <td align="center" style="padding-top:15px;">
                <div style="border-top:2px solid black; width:70%; margin:5px auto 0;"></div>
                <p style="margin:2px 0 0 0;">Date: {current_date}</p>
            </td>
        </tr>
    </table>
    '''