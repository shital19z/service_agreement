"""
Enhanced PDF Generator for Multi-page Service Agreements
Supports Page 1, Page 1 Continuation, Page 2, Page 3, and Page 3.1 (Consumer Notice)
"""
from xhtml2pdf import pisa
from io import BytesIO
try:
    from branch_config import get_branch_config, format_holidays_list
except ImportError:
  
    def get_branch_config(branch_code, state_code):
        return {
            "state_authority": "State Health Department",
            "manager_phone": "1-800-2-OPTIONS",
            "notice_period_days": 3,
            "holiday_count": 11,
            "holidays": ["New Year's Day", "Martin Luther King Day", "Presidents' Day", "Memorial Day", "Juneteenth Day", "Independence Day", "Labor Day", "Columbus Day", "Veterans' Day", "Thanksgiving Day", "Christmas Day"],
            "requires_consumer_notice": False,
            "governing_law": "This agreement is governed by the laws of the state of Maryland.",
            "notice_period_text": "OPTIONS, however, may end services with 3 calendar days' written notice.",
           'pdf_margins': {'top': 0.2, 'bottom': 0.3, 'left': 0.4, 'right': 0.4}
            
           
        }
        
    
    def format_holidays_list(holidays):
        if len(holidays) == 11:
            return ", ".join(holidays[:-1]) + ", and " + holidays[-1] + "."
        elif len(holidays) == 12:
            return ", ".join(holidays[:-1]) + ", and " + holidays[-1] + "."
        else:
            return ", ".join(holidays) + "."


def json_to_pdf(data_dict: dict):
    """
    Generate multi-page PDF service agreement with branch-specific content
    
    Args:
        data_dict: Dictionary containing agreement data and branch configuration
    
    Returns:
        BytesIO buffer containing the PDF
    """
    
    def safe_get(key, default=""):
        val = data_dict.get(key)
        if val is None or str(val).strip().lower() in ['none', 'null', '']:
            return default
        return str(val).strip()

    # Extract branch and state information
    branch_code = safe_get('branch_code', 'mnhomecare').lower()
    state_code = safe_get('state_code')
    
    # Get branch-specific configuration
    branch_config = get_branch_config(branch_code, state_code)

    requires_live_in = branch_config.get('requires_live_in_text', False)
    requires_consumer_notice = branch_config.get('requires_consumer_notice', False)
    margins = branch_config.get('pdf_margins', {'top': 0.2, 'bottom': 0.4, 'left': 0.4, 'right': 0.4})
    
    # Extract data
    office_name = safe_get('office_name', 'Options For Senior America')
    office_address = safe_get('address_line_1', '6 Montgomery Village Avenue')
    office_suite = safe_get('address_line_2', 'Suite 330')
    office_city = safe_get('city', 'Gaithersburg')
    office_state = safe_get('state_code', 'MD')
    office_zip = safe_get('zip_code', '20879')
    office_tel = safe_get('tel', '301.562.1100')
    office_fax = safe_get('fax', '301.562.1133')
    
    resp_name = f"{safe_get('clt_title')} {safe_get('clt_first_name')} {safe_get('clt_last_name')}".strip()
    clt_relationship = safe_get('clt_relationship', 'Self')
    agreement_date = safe_get('agreement_date', '')
    care_name = f"{safe_get('care_title')} {safe_get('care_first_name')} {safe_get('care_last_name')}".strip()
    care_addr = f"{safe_get('care_recipient_address')}, {safe_get('care_city')}, {safe_get('care_state')} {safe_get('care_zip')}"
    
    # Logo path - use provided URL or fallback to user-provided path
    logo_path = safe_get('logo_path', r'C:\Users\User\service-agreement-app\Image111.bmp')

    
    # Branch-specific values
    manager_phone = branch_config.get('manager_phone', safe_get('manager_phone', '1-800-2-OPTIONS'))
    state_authority = branch_config.get('state_authority', 'State Health Department')
    notice_period_text = branch_config.get('notice_period_text', 'OPTIONS, however, may end services with 3 calendar days\' written notice.')
    holidays_text = format_holidays_list(branch_config.get('holidays', []))
    governing_law = branch_config.get('governing_law', 'This agreement is governed by the laws of the state of Maryland.')
    footer_version = branch_config.get('footer_version', f'{state_code}')
    requires_consumer_notice = branch_config.get('requires_consumer_notice', False)
    
    # PDF margins from branch config
    margins = branch_config.get('pdf_margins', {'top': 0.2, 'bottom': 0.4, 'left': 0.4, 'right': 0.4})
    
    # Additional fields
    frequency_duration = safe_get('frequency_duration', '')
    hourly_rate = float(safe_get('hourly_rate', 36.0))
    mileage_rate = float(safe_get('mileage_rate', 0.67))
    vehicle_authorized = safe_get('vehicle_authorized', 'false').lower() == 'true'
    vehicle_initials = safe_get('vehicle_authorization_initials', '')
    requires_live_in = safe_get('is_live_in', 'false').lower() == 'true'
    
    # Bank information
    bank_name = safe_get('bank_name', '')
    bank_city = safe_get('bank_city', '')
    bank_state = safe_get('bank_state', '')
    routing_number = safe_get('routing_number', '')
    account_number = safe_get('account_number', '')
    account_type = safe_get('account_type', '')
    hazards_html = "" # Default to empty to prevent overlap
    hazards_branches = [
        'nvahomecare', 'nvahomecare_staging', 'rihomecare', 'rihomecare_staging', 
        'mnhomecare', 'mnhomecare_staging', 'lovahomecare', 'lovahomecare_staging',
        'wfvahomecare', 'wfvahomecare_staging', 'cfairfaxhomecare', 'cfairfaxhomecare_staging'
    ]

    if branch_code in hazards_branches:
        # Get hazards data and replace newlines with HTML breaks
        hazards_val = safe_get('hazards', 'None Reported').replace('\n', '<br/>')
        hazards_html = f"""
        <div style="font-size:10px; margin-top:8px; line-height:16px;">
            <p><b><u>HAZARDS:</u></b></p>
            <p style="margin-top:4px;">{hazards_val}</p>
        </div>
        """
        
    # --- CAREGIVER COMPETENCY Logic (Integrated from PHP) ---
    competency_html = "" # Initialize as empty to prevent overlap
    competency_branches = ['hbhomecare', 'hbhomecare_staging']

    if branch_code in competency_branches:
        competency_html = """
        <div style="font-size:10px; margin-top:8px; line-height:16px;">
            <p><b><u>CAREGIVER COMPETENCY REQUIREMENTS:</u></b></p>
            <p style="margin-top:4px;">Before assigning a Direct Care Worker to provide services to a consumer, 
            Options shall ensure that the Direct Care Worker has obtained a valid nurse's aide license in 
            Pennsylvania, or has successfully completed a training program as stipulated in 
            Pennsylvania's regulations, section 611.55, item 3.</p>
        </div>
        """
    
    # --- CHARGES Logic (Integrated from PHP) ---
    perc_charged = safe_get('PercCharged', '100')
    charges_header = f"<b><u>CHARGES:</u></b> &nbsp;"
    
    # Check for branches that show percentage charged
    perc_branches = [
        'nvahomecare', 'nvahomecare_staging', 'rihomecare', 'rihomecare_staging',
        'mnhomecare', 'mnhomecare_staging', 'lovahomecare', 'lovahomecare_staging'
    ]
    
    perc_text = ""
    if branch_code in perc_branches:
        perc_text = f"{perc_charged}% of the fees will be charged to {resp_name}<br/>"

    # Determine the main body of the Charges section
    if branch_code in ['test2homecare', 'test2homecare_staging']:
        charges_body = "OPTIONS will invoice in advance; monthly or bi-monthly. Any prepaid amount at the end of our services will be FULLY REFUNDABLE. RN assessment fee is charged at $100.00 per quarter."
    else:
        charges_body = "We bill bi-weekly for services rendered during the prior two weeks. If service hours are 80 hours or more per week, and for all 7-day live-in cases, billing will be done weekly. Payments are due upon receipt of OPTIONS invoices."

    # Combine into one variable
    final_charges_html = f"""
    <div style="font-size:10px; margin-top:8px; line-height:16px;">
        <p>{charges_header}{perc_text}{charges_body}</p>
    </div>
    """
    
    # --- FEDERAL HOLIDAYS Logic (Integrated from PHP) ---
    # Default list (11 holidays)
    holidays_list = [
        "New Year's Day", "Martin Luther King Day", "Presidents' Day", 
        "Memorial Day", "Juneteenth Day", "Independence Day", 
        "Labor Day", "Columbus Day", "Veterans' Day", 
        "Thanksgiving Day", "Christmas Day"
    ]
    
    # Check if branch is mnhomecare to add Easter Sunday (12 holidays)
    if branch_code in ['mnhomecare', 'mnhomecare_staging']:
        # Insert Easter Sunday after Presidents' Day
        holidays_list.insert(3, "Easter Sunday")
    
    holiday_count = len(holidays_list)
    # Format the list into a string: "A, B, and C"
    formatted_holidays = ", ".join(holidays_list[:-1]) + ", and " + holidays_list[-1]

    # Build the dynamic HTML block
    federal_holidays_html = f"""
    <div style="font-size:10px; margin-top:8px; line-height:16px;">
        <p><b><u>FEDERAL HOLIDAYS:</u></b> &nbsp; When services are required on Federal holidays, 
        you will be charged "time and a half" for those days (50% more than your usual daily charge). 
        We apply those surcharges on the {holiday_count} holidays as follows: {formatted_holidays}.
        </p>
    </div>
    """
    
    # --- LIVE-IN SERVICES Logic (Integrated from PHP) ---
    live_in_services_html = "" # Initialize as empty to prevent overlap
    
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

    if branch_code in live_in_branches:
        live_in_services_html = """
        <div style="font-size:10px; margin-top:8px; line-height:16px;">
            <p><b><u>LIVE-IN SERVICES AND CARE PROVIDER SCHEDULE:</u></b> &nbsp; 
            OPTIONS care providers who provide live-in services have a standard work schedule of 
            twelve (12) hours per each twenty-four hour day. This accounts for eight (8) hours of 
            sleep (five (5) of which must be uninterrupted), and four (4) hours for meals and breaks. 
            During this twelve (12) hour period, the care provider is considered off-duty, and must 
            be provided with adequate, private, and sanitary accommodations. In the event the care 
            recipient requests our live-in care provider to provide services during an off-duty period, 
            then you will be responsible for additional charges, beyond the daily live-in rate, at 
            our standard hourly rate times the number of hours worked during the interruption period. 
            If, as a result of such request, our care provider is unable to rest for an uninterrupted 
            five (5) hours, then you will be billed at our standard hourly rate for the entire eight 
            (8) hour sleep time period.
            </p>
        </div>
        """
    # --- UPDATED NEEDS ASSESSMENT & VALUABLES Logic ---
    # Default values for standard branches
    needs_assessment_body = "A fee of $95.00 for a Needs Assessment and Plan of Care is waived if the ongoing case requires more than 30 service hours per week. Otherwise, the fee is included on the invoice."
    valuables_body = "Our care providers are not authorized to accept direct payments from you or to handle your valuables (credit cards, checkbooks, cash, etc.). Please exercise caution with your valuables. If you believe any valuables are missing, please report the loss to OPTIONS and to the police."

    # Expanded branch list from PHP snippet
    expanded_needs_branches = [
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

    if branch_code in expanded_needs_branches:
        needs_assessment_body = "When a Needs Assessment and a Plan of Care is conducted by Options staff, the associated $95 fee is waived for any ongoing case that requires more than thirty (30) service hours per week. Otherwise, this fee is included on the Options invoice."
        valuables_body = "Our care providers are not authorized to accept payments directly, nor to have use or custody of any valuables belonging to you (credit cards, checkbooks, cash, and the like). Common sense dictates that you be careful with such valuables, and alert OPTIONS and the police should you notice a loss."

    # Build the HTML block using 13px font and 14px line-height as per PHP snippet
    needs_and_valuables_html = f"""
    <div style="font-size:10px; margin-top:8px; line-height:14px;">
        <p><b><u>NEEDS ASSESSMENT & PLAN OF CARE:</u></b> &nbsp; {needs_assessment_body}</p>
    </div>
    <div style="font-size:10px; margin-top:8px; line-height:14px;">
        <p><b><u>YOUR VALUABLES:</u></b> &nbsp; {valuables_body}</p>
    </div>
    """
    
    # --- NOTICE PERIOD Logic (Integrated from PHP) ---
    ten_day_notice_branches = ['hbhomecare', 'hbhomecare_staging', 'nspahomecare', 'nspahomecare_staging']

    if branch_code in ten_day_notice_branches:
        notice_body = ("The care recipient or his/her designees are not obligated to give a written notice of termination. "
                       "OPTIONS may end services under this agreement by giving at least 10 calendar days advance written "
                       "notice of the intent to terminate services. Less than 10 days advance written notice may be provided "
                       "by OPTIONS in the event the client has failed to pay for services, despite notice, and the client is "
                       "more than 14 days in arrears, or if the health and welfare of the OPTIONS caregiver is at risk.")
    else:
        notice_body = ("The care recipient or his/her designees are not obligated to give a written notice of termination. "
                       "OPTIONS may end services under this agreement by giving 3 calendar days notice in writing.")

    notice_period_html = f"""
    <div style="font-size:10px; margin-top:8px; line-height:14px;">
        <p><b><u>NOTICE PERIOD:</u></b> &nbsp; {notice_body}</p>
    </div>
    """
    
    # --- ADMINISTERING MEDICATION Logic (Integrated from PHP) ---
    medication_html = ""
    
    # List of branches that always include this clause
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

    # Get the care recipient's state (ensure it's uppercase for comparison)
    care_state = safe_get('CareState', '').upper()

    # Check if branch is in the main list OR if it's DC branch specifically in DC state
    if branch_code in med_branches or (branch_code in ['dchomecare', 'dchomecare_staging'] and care_state == "DC"):
        medication_html = """
        <div style="font-size:10px; margin-top:8px; line-height:14px;">
            <p><b><u>ADMINISTERING MEDICATION:</u></b> &nbsp; For those care recipients who require 
            administration of medication, if the care recipient is not cognitively competent, and a 
            family member is unavailable to administer the medication on a weekly basis, we will 
            assign an RN or CMT to make weekly visits to administer and dispense the medication 
            at the rate of $75/visit.</p>
        </div>
        """
        
    # --- USE OF FAMILY VEHICLE Logic (Integrated from PHP) ---
    vehicle_branches = ['scgahomecare', 'scgahomecare_staging', 'athomecare', 'athomecare_staging']
    
    if branch_code in vehicle_branches:
        # Checkbox version for GA/SC branches
        vehicle_body = (
            "If you wish to authorize our care providers to drive your/the care recipient's vehicle "
            "and hold Options and its care providers harmless and release them from any associated "
            "liability, please check the “Yes” box and place your initials next to it, or otherwise "
            "check the “No” box and place your initials next to it.&nbsp;&nbsp;"
            "☐ Yes _______&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;☐ No _______"
        )
    else:
        # Standard initial line version
        vehicle_body = (
            "If you wish to authorize our care providers to drive your/the care recipient's vehicle "
            "and hold Options and its care providers harmless and release them from any associated "
            "liability, please write \"Authorized\" here and initial: _______________________"
        )

    vehicle_html = f"""
    <div style="font-size:10px; margin-top:8px; line-height:14px;">
        <p><b><u>USE OF FAMILY VEHICLE:</u></b> &nbsp; {vehicle_body}</p>
    </div>
    """
    
    # --- GENERAL PROVISIONS Logic (Governing State) ---
    # Default to Maryland
    gen_prov_state = "Maryland"
    
    # Define mapping of branches to states
    state_mapping = {
        "North Carolina": ['gbhomecare', 'gbhomecare_staging', 'rdhomecare', 'rdhomecare_staging'],
        "Georgia": ['scgahomecare', 'scgahomecare_staging'],
        "Commonwealth of Virginia": [
            'mnhomecare', 'mnhomecare_staging', 'cfairfaxhomecare', 'cfairfaxhomecare_staging', 
            'lovahomecare', 'lovahomecare_staging', 'wfvahomecare', 'wfvahomecare_staging', 
            'amfvahomecare', 'amfvahomecare_staging', 'sfvahomecare', 'sfvahomecare_staging'
        ],
        "Ohio": ['ciohhomecare', 'ciohhomecare_staging'],
        "Pennsylvania": ['nspahomecare', 'nspahomecare_staging'],
        "Indiana": ['lkinhomecare', 'lkinhomecare_staging'],
        "New Jersey": ['wenjhomecare', 'wenjhomecare_staging'],
        "Arizona": ['chazhomecare', 'chazhomecare_staging'],
        "Florida": ['wpbflhomecare', 'wpbflhomecare_staging', 'lzflhomecare', 'lzflhomecare_staging']
    }

    # Find the correct state based on branch_code (lowercased for safety)
    current_branch_lower = branch_code.lower()
    for state, branches in state_mapping.items():
        if any(current_branch_lower == b.lower() for b in branches):
            gen_prov_state = state
            break

    general_provisions_html = f"""
    <div style="font-size:10px; margin-top:8px; line-height:14px;">
        <p><b><u>GENERAL PROVISIONS:</u></b></p>
        <ol type="a" style="padding-left: 20px;">
            <li style="margin-bottom: 3px;">The waiver by Options of a breach of any provision of this Agreement shall not be construed as a waiver of any other provision of this Agreement or of any future breach of the provision so waived.</li>
            <li style="margin-bottom: 3px;">No change, modification, termination, or attempted waiver of any of the provisions of this Agreement shall be binding upon Options or the undersigned unless put in writing and signed by Options and the undersigned.</li>
            <li style="margin-bottom: 3px;">This Agreement shall be governed by the laws of the state of {gen_prov_state}.</li>
            <li style="margin-bottom: 3px;">This Agreement supersedes all prior agreements and understandings, oral or written, between Options and the undersigned with respect to the subject matter hereof.</li>
        </ol>
    </div>
    """
    
    # --- PATIENTS' RIGHTS & COMPLAINT PROCEDURES Logic (Integrated from PHP) ---
    rights_html = ""
    
    # Get branch lowercase for consistent comparison
    branch_lower = branch_code.lower()
    
    # 1. MARYLAND & NEW JERSEY BRANCHES
    md_nj_branches = [
        'anhomecare', 'anhomecare_staging', 'bahomecare', 'bahomecare_staging', 
        'blhomecare', 'blhomecare_staging', 'fkhomecare', 'fkhomecare_staging', 
        'lphomecare', 'lphomecare_staging', 'testhomecare', 'dchomecare', 'dchomecare_staging'
    ]

    if branch_lower in md_nj_branches:
        # Determine Top Margin
        top_margin = "5px"
        if branch_lower in ['bahomecare', 'bahomecare_staging', 'lphomecare', 'lphomecare_staging']:
            top_margin = "0px"
            
        # NJ vs MD checks
        is_nj = branch_lower in ['wenjhomecare', 'wenjhomecare_staging']
        
        # Barbara Fagan / Maryland Hotline clause
        md_hotline_li = ""
        if not is_nj:
            md_hotline_li = (
                "<li>You may write to Barbara Fagan, Survey Coordinator, Office of Health Care Quality, "
                "Bland Bryant Building, Spring Grove Hospital Center, 55 Wade Avenue, Catonsville, MD 21228, "
                "or you may call the State of Maryland's Residential Service Agency Hotline at 1-877-4MD-DHMH.</li>"
            )

        # Phone numbers for Complaint Intake
        if is_nj:
            office_num = "973.803.0901"
        else:
            office_num = ("410.224.2700 for Annapolis, 410.448.1100 for Baltimore, 410.893.9914 for Bel Air, "
                          "301.562.3100 for Bethesda, 301.624.5630 for Frederick, and 301.392.1387 for La Plata")

        # Appeal Text
        if is_nj:
            appeal_text = (
                "If you are not satisfied with the proposed resolution, you may appeal to an agency Director "
                "at 973.803.0901, or in writing to OPTIONS Director, 70 South Orange Avenue, Suite 105, "
                "Livingston, NJ 07039 in which case they would review the case and get back to you in writing "
                "within 21 days of receipt of the appeal. You may also write to the New Jersey Office of the "
                "Attorney General, Division of Consumer Affairs, Certified Homemaker-Home Health Aide Unit, "
                "124 Halsey Street, 6th Floor, P.O. Box 47030, Newark, NJ 07101 - 973.504.6430."
            )
        else:
            appeal_text = (
                "If you are not satisfied with the proposed resolution, you may appeal to an agency Director "
                "at 1-800-2-OPTIONS, or in writing to OPTIONS Director, 555 Quince Orchard Road, Suite 240, "
                "Gaithersburg, MD 20878, in which case they would review the case and get back to you in writing "
                "within 21 days of receipt of the appeal. You may also write to Barbara Fagan, Survey Coordinator, "
                "Office of Health Care Quality, Bland Bryant Building, Spring Grove Hospital Center, 55 Wade Avenue, "
                "Catonsville, MD 21228, or you may call the State of Maryland's Residential Service Agency Hotline "
                "at 1-877-4MD-DHMH."
            )

        rights_html = f"""
        <div style="font-size:11px; margin-top:{top_margin};">
            <p style="text-align:center; margin-bottom:5px;"><b><u>Notice of Patients' Rights and Responsibilities</u></b></p>
            <ol type="1" style="padding-left: 26px; margin:0;">
                <li>A client, or the client representative with legal authority to make health care decisions, has the right to:
                    <ol type="a" style="padding-left: 24px; margin:0;">
                        <li>Be treated with consideration, respect, and full recognition of the client's human dignity and individuality</li>
                        <li>Receive treatment, care, and services that are adequate, appropriate, and in compliance with relevant State, local, and federal laws and regulations</li>
                        <li>Participate in the development of the client's care plan and medical treatment</li>
                        <li>Refuse treatment after the possible consequences of refusing treatment have been fully explained</li>
                        <li>Privacy</li>
                        <li>Be free from mental, verbal, sexual, and physical abuse, neglect, involuntary seclusion, and exploitation</li>
                        <li>Confidentiality</li>
                    </ol>
                </li>
                <li>A client or client representative has the right to:
                    <ol type="a" style="padding-left: 24px; margin:0;">
                        <li>Make suggestions or complaints, or present grievances on behalf of the client to the agency, government agencies, or other persons without the threat or fear of retaliation</li>
                        <li>Receive a prompt response, through an established complaint or grievance procedure, to any complaints, suggestions, or grievances the participant may have</li>
                        <li>Have access to the procedures for making a complaint to the Office of Health Care Quality - see (3) below, and to:
                            <ol type="i" style="padding-left: 24px;">
                                <li>The Adult Protective Services Program of the local department of social services, if the client is an adult; or</li>
                                <li>The Child Protective Services Program of the local department of social services, if the client is a minor</li>
                            </ol>
                        </li>
                    </ol>
                </li>
                {md_hotline_li}
                <li>A client or client representative has the responsibility to:
                    <ol type="a" style="padding-left: 24px; margin:0;">
                        <li>Advise the Options office of any changes in the care recipient's condition, or of any events that affect the care recipient's service needs.</li>
                        <li>Treat the Options caregivers with respect.</li>
                        <li>Pay Options invoices in a timely manner as indicated below under the "Notice of Billing Procedures" section.</li>
                    </ol>
                </li>
            </ol>

            <p style="font-size:11px;text-align:center;margin:3px 0;margin-top:{top_margin};"><b><u>Notice of Complaint Procedures</u></b></p>
            <ol type="1" style="padding-left: 26px; margin:0;">
                <li>Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their office number is {office_num}.</li>
                <li>OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
                <li>The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager or the Care Manager.</li>
                <li>OPTIONS will produce a written record of the findings of each complaint investigated.</li>
                <li>The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Manager.</li>
                <li>The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient's property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
                <li>The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
                <li>{appeal_text}</li>
            </ol>
        </div>
        """

    # 2. GEORGIA BRANCHES
    elif branch_lower in ['athomecare', 'athomecare_staging', 'scgahomecare', 'scgahomecare_staging']:
        rights_html = """
        <div style="font-size:11px; margin-top:8px;">
            <p style="text-align:center; margin-bottom:5px;"><b><u>NOTICE OF RIGHTS AND RESPONSIBILITIES</u></b></p>
            <p style="text-align:center; margin-bottom:5px;"><b>You are a valued customer, and you have the following rights and responsibilities</b></p>
            <ol type="1" style="padding-left: 26px; margin:0;">
                <li>Right to be promptly and fully informed of any changes in the plan of service.</li>
                <li>Right to accept or refuse services.</li>
                <li>Right to be fully informed of the charges of services.</li>
                <li>Right to be informed of the name, business telephone number and business address of the person supervising the services and how to contact that person.</li>
                <li>Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time. The complaint procedure provided shall include the business address and telephone number of the person designated by the provider to handle complaints and questions.</li>
                <li>Right of confidentiality of client records.</li>
                <li>Right to have property and residence treated with respect.</li>
                <li>Right to receive a written notice of the address and telephone number of the state licensing authority, namely the department of Human Resources which is charged the responsibility of licensing the provider and investigating client complaints that appear to violate licensing regulation.</li>
                <li>Right to obtain a copy of the provider's most recent completed report of licensure inspection from the provider upon written request. The provider is not required to release the report of licensure inspection until the provider has had an opportunity to file a written plan of correction for the violations, if any, identified.</li>
                <li>The facility may charge the client reasonable photocopying charges.</li>
                <li>Responsibility to advise the provider of any changes in the care recipient's condition of any events that affect the care recipient's service needs</li>
                <li>For further assistance or other issues, you may call the OPTIONS Manager, at 404-634-1111, or you may
                call the State Licensing authority for private home care providers at: Georgia Department of Community 
                Health, Healthcare Facility Regulation Division, 2 Peachtree Street, NW, Suite 31-447, Atlanta, GA 
                30303-3142, (404) 657-5850. For complaints (404) 657-5728. It is your right to report abuse, neglect or exploitation. Please call toll free 1-800-962-2873.</li>
            </ol>
        </div>
        """

    # 3. CLEVELAND/DC/OTHER BRANCHES with similar format
    elif branch_lower in ['clhomecare', 'clhomecare_staging', 'blmdhomecare', 'blmdhomecare_staging', 
                          'ciohhomecare', 'ciohhomecare_staging', 'chazhomecare', 'chazhomecare_staging',
                          'shmihomecare', 'shmihomecare_staging']:
        
        # Set specific manager phone based on branch
        if branch_lower in ['clhomecare', 'clhomecare_staging']:
            manager_phone_display = "301.562.1100 or 800.267.8466"
            complaint_phone = "301.562.3100 for the District of Columbia, 216.861.3700 for the Cleveland area"
            director_info = "at 1-800-2-OPTIONS, or in writing to OPTIONS Director, 555 Quince Orchard Road, Suite 240, Gaithersburg, MD 20878"
        elif branch_lower in ['blmdhomecare', 'blmdhomecare_staging']:
            manager_phone_display = "667.415.8317"
            complaint_phone = "667.415.8317"
            director_info = "at 1-800-2-OPTIONS, or in writing to OPTIONS Director, 4690 Millennium Drive, Belcamp MD 21017"
        elif branch_lower in ['ciohhomecare', 'ciohhomecare_staging']:
            manager_phone_display = "513.928.0042"
            complaint_phone = "513.928.0042"
            director_info = "at 1-800-2-OPTIONS, or in writing to OPTIONS Director, 555 Quince Orchard Road, Suite 240, Gaithersburg, MD 20878"
        elif branch_lower in ['chazhomecare', 'chazhomecare_staging']:
            manager_phone_display = "480.673.3888"
            complaint_phone = "480.673.3888"
            director_info = "at 480.673.3888, or in writing to OPTIONS Director, 920 W. Chandler Blvd, Suite 3, Chandler, AZ 85225"
        elif branch_lower in ['shmihomecare', 'shmihomecare_staging']:
            manager_phone_display = "586.344.8436"
            complaint_phone = "586.344.8436"
            director_info = "in writing to 13854 Lakeside Circle, Suite 250, Sterling Heights, MI 48313"
        else:
            manager_phone_display = "301.562.1100 or 800.267.8466"
            complaint_phone = "301.562.3100"
            director_info = "at 1-800-2-OPTIONS"

        rights_html = f"""
        <div style="font-size:11px;">
            <p style="font-size:14px;text-align:center;margin-bottom:5px;margin-top:18px;"><b><u>Notice of Patients' Rights and Responsibilities</u></b></p>
            <p style="font-size:11px;margin-bottom:5px;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE FOLLOWING RIGHTS AND RESPONSIBILITIES:</p>
            <ol type="1" style="padding-left: 26px;margin:0;">
                <li>Right to accept or refuse services.</li>
                <li>Right to be fully informed of the charges of the services.</li>
                <li>Right to be fully informed of the name, business telephone number and business address of the person supervising the service and how to contact that person.</li>
                <li>Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time.</li>
                <li>Right of confidentiality of patient records.</li>
                <li>Right to have your property and residence treated with respect.</li>
                <li>Responsibility to advise the provider of any changes in your condition or any events that affect your service needs.</li>
                <li>Responsibility to treat the OPTIONS' caregivers with respect.</li>
                <li>For further assistance, you may call and speak with an OPTIONS manager at {manager_phone_display}</li>                
            </ol>
            <p style="font-size:11px;text-align:center;margin:3px 0;margin-top:7px;"><b><u>Notice of Complaint Procedures</u></b></p>
            <p style="font-size:11px;margin-bottom:5px;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
            <ol type="1" style="padding-left: 26px;margin:0;">
                <li>Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their office number is {complaint_phone}.</li>
                <li>OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
                <li>The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager or the Care Manager.</li>
                <li>OPTIONS will produce a written record of the findings of each complaint investigated.</li>
                <li>The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Manager.</li>
                <li>The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient's property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
                <li>The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
                <li>If you are not satisfied with the proposed resolution, you may appeal to an agency Director {director_info}, in which case they would review the case and get back to you in writing within 21 days of receipt of the appeal.</li>
            </ol>
        </div>
        """

    # 4. VIRGINIA BRANCHES (nvahomecare, rihomecare, mnhomecare, lovahomecare, etc.)
    elif branch_lower in ['nvahomecare', 'nvahomecare_staging', 'nvahomecarearchive', 'nvahomecarearchive_staging',
                          'rihomecare', 'rihomecare_staging', 'mnhomecare', 'mnhomecare_staging',
                          'lovahomecare', 'lovahomecare_staging', 'sfvahomecare', 'sfvahomecare_staging',
                          'amfvahomecare', 'amfvahomecare_staging', 'wfvahomecare', 'wfvahomecare_staging',
                          'cfairfaxhomecare', 'cfairfaxhomecare_staging']:
        
        # Set specific administrator info based on branch
        if branch_lower in ['nvahomecare', 'nvahomecare_staging', 'nvahomecarearchive', 'nvahomecarearchive_staging']:
            admin_phone = "(703) 442-9700"
            admin_name = "Ramzi Rihani"
            admin_alt = "the Administrator"
            office_addr = "6 Montgomery Village Avenue, Suite 330, Gaithersburg, MD 20879"
        elif branch_lower in ['rihomecare', 'rihomecare_staging']:
            admin_phone = "(804) 673-6730"
            admin_name = "Ramzi Rihani"
            admin_alt = "the Administrator"
            office_addr = "6 Montgomery Village Avenue, Suite 330, Gaithersburg, MD 20879"
        elif branch_lower in ['mnhomecare', 'mnhomecare_staging']:
            admin_phone = "(571) 449-6781"
            admin_name = "Michele Mezher"
            admin_alt = "the Administrator"
            office_addr = "10432 Balls Ford Road, Suite 300, Manassas, VA 20109"
        elif branch_lower in ['lovahomecare', 'lovahomecare_staging']:
            admin_phone = "571.999.5464"
            admin_name = "Danny Mezher"
            admin_alt = "the Administrator"
            office_addr = "13800 Coppermine Road, Suite 125-A, Herndon, VA 20171"
        elif branch_lower in ['sfvahomecare', 'sfvahomecare_staging']:
            admin_phone = "(571) 416-8260"
            admin_name = "Liza Sagudan"
            admin_alt = "the Administrator"
            office_addr = "7830 Backlick Road, Suite 200-A, Springfield, VA 22150"
        elif branch_lower in ['amfvahomecare', 'amfvahomecare_staging']:
            admin_phone = "571.449.6781"
            admin_name = "Viral Patel"
            admin_alt = "the Administrator"
            office_addr = "11350 Random Hills Rd, Suite 800, Fairfax, VA 22030"
        elif branch_lower in ['wfvahomecare', 'wfvahomecare_staging', 'cfairfaxhomecare', 'cfairfaxhomecare_staging']:
            admin_phone = "(703) 622-7132"
            admin_name = "Danny Mezher"
            admin_alt = "the Administrator"
            office_addr = "13800 Coppermine Road, Suite 104-B, Herndon, VA 20171"
        else:
            admin_phone = "(703) 442-9700"
            admin_name = "Ramzi Rihani"
            admin_alt = "the Administrator"
            office_addr = "6 Montgomery Village Avenue, Suite 330, Gaithersburg, MD 20879"

        rights_html = f"""
        <div style="font-size:11px;">
            <p style="font-size:11px;text-align:center;margin-bottom:5px;"><b><u>Notice of Patients' Rights and Responsibilities</u></b></p>
            <p style="font-size:11px;text-align:center;margin-bottom:5px;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE RIGHT TO BE:</p>
            <ol type="1" style="padding-left: 26px;margin:0;">
                <li>Treated with courtesy, consideration and respect and is assured of the right of privacy.</li>
                <li>Assured confidential treatment of medical and financial records as provided by law.</li>
                <li>Free from mental and physical abuse, neglect, and property exploitation.</li>
                <li>Assured the right to participate in the planning of the client's home care, including the right to refuse services.</li>
                <li>Served by individuals who are properly trained and competent to perform their duties.</li>
                <li>Assured the right to voice grievances and complaints related to the organizational services without fear of reprisal.</li>
                <li>Advised, before care is initiated, of the extent to which payment for the home care organization services may be expected from federal or state programs, and the extent to which payment may be required from the client.</li>
                <li>Advised orally and in writing of any changes in fees for services that are the client's responsibility. The home care organization shall advise the client of these changes as soon as possible, but no later than 30 calendar days from the date the home care organization became aware of the changes.</li>
                <li>Provided with advance directive information prior to start of services.</li>
                <li>Given at least five days written notice when the organization determines to terminate services.</li>
            </ol>
            <p style="font-size:11px;text-align:center;margin:3px 0;margin-top:5px;"><b><u>Notice of Complaint Procedures</u></b></p>
            <p style="font-size:11px;text-align:left;margin-bottom:5px;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
            <ol type="1" style="padding-left: 26px;margin:0;">
                <li>Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Administrator or the Administrator Alternate. Their office number is {admin_phone}.</li>
                <li>OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
                <li>The OPTIONS employee who will be responsible for investigating complaints is the Administrator or the Administrator Alternate.</li>
                <li>OPTIONS will produce a written record of the findings of each complaint investigated.</li>
                <li>The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Administrator or Administrator Alternate.</li>
                <li>The local social service department of Adult Protective Services will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient's property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
                <li>The Administrator or Administrator Alternate is the agency employee who will, within 30 days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
                <li>If you are not satisfied with the proposed resolution, you may appeal to {admin_name}, {admin_alt}, at {admin_phone}, or in writing to OPTIONS, {office_addr}, in which case they would review the case and get back to you in writing within 21 days of receipt of the appeal. You may also contact the Office of the State Long Term Care Ombudsman at 8004 Franklin Farms Drive, Richmond, VA 23229, Tel. (800) 522-3402 or the Office of Licensure and Certification of the Virginia Dept. of Health at 9960 Mayland Drive, Suite 401, Henrico, VA 23233-1485, Tel. (800) 828-1120 and Fax (804) 527-4502.</li>
            </ol>
        </div>
        """

    # 5. FLORIDA BRANCHES
    elif branch_lower in ['tahomecare', 'tahomecare_staging', 'woflhomecare', 'woflhomecare_staging', 
                          'lzflhomecare', 'lzflhomecare_staging', 'wpbflhomecare', 'wpbflhomecare_staging']:
        rights_html = """
        <div style="font-size:11px;">
            <p style="font-size:11px;text-align:center;margin-bottom:5px;"><b><u>NOTICE OF RIGHTS AND RESPONSIBILITIES</u></b></p>
            <p style="font-size:11px;text-align:center;margin-bottom:5px;"><b>You are a valued customer, and you have the following rights and responsibilities</b></p>
            <ol type="1" style="padding-left: 26px;margin:0;">
                <li>The patient, responsible party, or guardian have the right to be informed of the medical plan of treatment and/or plan of care, to participate in the development of the medical plan of treatment and/or plan of care and to have a copy of the medical plan of treatment and/or plan of care if requested. Our Registered Nurses are available to make initial assessments and develop a plan of care, as well as visits to patient's home per patient, responsible party, or guardian's request at an additional cost of $95.00/visit.</li>
                <li>Right to accept or refuse services.</li>
                <li>Right to be fully informed of the charges of services.</li>
                <li>Right to be informed of the name, business telephone number and business address of the person supervising the services and how to contact that person.</li>
                <li>Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time. The complaint procedure provided shall include the business address and telephone number of the person designated by the provider to handle complaints and questions.</li>
                <li>Right of confidentiality of client records.</li>
                <li>Right to have property and residence treated with respect.</li>
                <li>Responsibility to advise the provider of any changes in the care recipient's condition of any events that affect the care recipient's service needs.</li>
                <li>To report a complaint regarding the services you receive, please call toll free 1-888-419-3456.</li>
                <li>To report abuse, neglect, or exploitation, please call toll free 1-800-962-2873.</li>
            </ol>
        </div>
        """

    # 6. INDIANA BRANCH
    elif branch_lower in ['lkinhomecare', 'lkinhomecare_staging']:
        rights_html = """
        <div style="font-size:11px;">
            <p style="font-size:11px;text-align:center;margin-bottom:5px;"><b><u>Notice of Client's Rights and Responsibilities</u></b></p>
            <p style="font-size:11px;text-align:left;margin-bottom:5px;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE RIGHT TO:</p>
            <ol type="1" style="padding-left: 26px;margin:0;">
                <li>Have your property treated with respect.</li>
                <li>Temporarily suspend, permanently terminate, temporarily add, or permanently add services in the service plan.</li>
                <li>File grievances regarding services furnished or regarding the lack of respect for property by the personal services agency, and is not subject to discrimination or reprisal for filing a grievance.</li>
                <li>Be free from verbal, physical, and psychological abuse and to be treated with dignity. Furthermore, as part of the client rights and responsibilities, it is understood that:</li>
                <li>It is not within the scope of the personal services agency's license to manage the medical and health conditions of the client if a condition becomes unstable or unpredictable.</li>
                <li>The client is made aware of charges for services provided by the personal services agency.</li>
                <li>The personal services agency's policy for notifying the client of any increase in the cost of services is included below, under "Notice of Billing Procedures".</li>
                <li>The hours the personal services agency's office is open for business are made known to the client.</li>
                <li>Upon request by the client, the personal service agency will make available to the client a written list of the names and addresses of all persons having at least a five percent (5%) ownership or controlling interest in the personal services agency.</li>
                <li>The procedures for contacting the personal services agency's manager, or the manager's designee, while the personal services agency's office is open or closed, are made known to the client.</li>
                <li>The procedure and telephone number to call to file a complaint with the personal services agency are indicated below under "Notice of Complaint Procedures".</li>
                <li>That the state department does not inspect personal services agencies as a part of the licensing process but does investigate complaints concerning personal services agencies.</li>
                <li>The procedure and telephone number to call to file a complaint with the state department along with the business hours of the state department are included below in the "Notice of Complaint Procedures" section.</li>
            </ol>
            <p style="font-size:11px;text-align:center;margin:3px 0;margin-top:5px;"><b><u>Notice of Complaint Procedures</u></b></p>
            <p style="font-size:11px;text-align:left;margin-bottom:5px;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
            <ol type="1" style="padding-left: 26px;margin:0;">
                <li>Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Office Manager or the Franchise Owner. Their office number is 219.321.9130.</li>
                <li>OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
                <li>The OPTIONS employee who will be responsible for investigating complaints is the Franchise Owner or the Office Manager.</li>
                <li>OPTIONS will produce a written record of the findings of each complaint investigated.</li>
                <li>The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Franchise Owner or the Office Manager.</li>
                <li>The local social service department Adult Protective Services unit will be informed if, at any stage of investigating or resolving a complaint, the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient's property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
                <li>The Franchise Owner or the Office Manager is the agency employee who will, within 5 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
                <li>If you are not satisfied with the proposed resolution, you may appeal to an agency Director at 219.321.9130, or in writing to OPTIONS Director, 8488 Georgia Street, Suite D, Merrillville, IN 46410, in which case they would review the case and get back to you in writing within 5 business days of receipt of the appeal. You may also contact the Consumer Protection Division Complaint Hotline at 1-800-382-5516, the Indiana Department of Aging at 1-888-673-0002, or the Indiana State Department for Health at 317-233-1325 between 8:15AM and 4:45PM Monday through Friday.</li>
            </ol>
        </div>
        """

    # 7. NORTH CAROLINA BRANCHES (gbhomecare, rdhomecare)
    elif branch_lower in ['gbhomecare', 'gbhomecare_staging', 'rdhomecare', 'rdhomecare_staging']:
        if branch_lower in ['gbhomecare', 'gbhomecare_staging']:
            complaint_phone = "336.270.6647"
            nc_hotline = '<li>You may also contact the North Carolina Division of Health Service Regulation, complaints hotline, at 800.624.3004.</li>'
        else:  # rdhomecare
            complaint_phone = "919.380.6812"
            nc_hotline = '<li>You may also contact the North Carolina Division of Health Service Regulation, complaints hotline, at 800.624.3004.</li>'

        rights_html = f"""
        <div style="font-size:11px;">
            <p style="font-size:11px;text-align:center;margin-bottom:5px;"><b><u>Notice of Patients' Rights and Responsibilities</u></b></p>
            <p style="font-size:11px;text-align:left;margin-bottom:5px;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE FOLLOWING RIGHTS AND RESPONSIBILITIES:</p>
            <ol type="1" style="padding-left: 26px;margin:0;">
                <li>Right to participate in the planning of the client's home care, including the right to accept or refuse services.</li>
                <li>Right to be fully informed of the charges of the services.</li>
                <li>Right to be fully informed of the name, business telephone number and business address of the person supervising the service and how to contact that person.</li>
                <li>Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time.</li>
                <li>Right of confidentiality of patient records.</li>
                <li>Right to have your property and residence treated with respect.</li>
                <li>Right of nondiscrimination in obtaining services from Options because of race, color, religion, creed, national origin, ancestry, disability, sex, or age.</li>
                <li>Responsibility to advise the provider of any changes in your condition or any events that affect your service needs.</li>
                <li>Responsibility to treat the OPTIONS' caregivers with respect.</li>
            </ol>
            <p style="font-size:11px;text-align:center;margin:3px 0;"><b><u>Notice of Complaint Procedures</u></b></p>
            <p style="font-size:11px;text-align:left;margin-bottom:5px;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
            <ol type="1" style="padding-left: 26px;margin:0;">
                <li>Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their telephone number is {complaint_phone}.</li>
                <li>OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
                <li>The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager.</li>
                <li>OPTIONS will produce a written record of the findings of each complaint investigated.</li>
                <li>The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Manager.</li>
                <li>The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient's property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
                <li>The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
                {nc_hotline}
            </ol>
        </div>
        """

    # 8. PENNSYLVANIA BRANCHES (nspahomecare)
    elif branch_lower in ['nspahomecare', 'nspahomecare_staging']:
        rights_html = """
        <div style="font-size:11px;">
            <p style="font-size:11px;text-align:center;margin-bottom:5px;"><b><u>Notice of Patients' Rights and Responsibilities</u></b></p>
            <p style="font-size:11px;text-align:left;margin-bottom:5px;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE FOLLOWING RIGHTS AND RESPONSIBILITIES:</p>
            <ol type="1" style="padding-left: 26px;margin:0;">
                <li>Right to participate in the planning of the client's home care, including the right to accept or refuse services.</li>
                <li>Right to be fully informed of the charges of the services.</li>
                <li>Right to be fully informed of the name, business telephone number and business address of the person supervising the service and how to contact that person.</li>
                <li>Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time.</li>
                <li>Right of confidentiality of patient records.</li>
                <li>Right to have your property and residence treated with respect.</li>
                <li>Right of nondiscrimination in obtaining services from Options because of race, color, religion, creed, national origin, ancestry, disability, sex, or age.</li>
                <li>Responsibility to advise the provider of any changes in your condition or any events that affect your service needs.</li>
                <li>Responsibility to treat the OPTIONS' caregivers with respect.</li>
            </ol>
            <p style="font-size:11px;text-align:center;margin:3px 0;margin-top:5px;"><b><u>Notice of Complaint Procedures</u></b></p>
            <p style="font-size:11px;text-align:left;margin-bottom:5px;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
            <ol type="1" style="padding-left: 26px;margin:0;">
                <li>Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their telephone number is 610.975.4422.</li>
                <li>OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
                <li>The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager.</li>
                <li>OPTIONS will produce a written record of the findings of each complaint investigated.</li>
                <li>The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Manager.</li>
                <li>The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient's property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
                <li>The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
                <li>If you are not satisfied with the proposed resolution, you may appeal to Options Corporate office at 1-800-2-OPTIONS, or in writing to OPTIONS, 175 Strafford Avenue, Suite One Wayne, PA 19087, in which case your complaint would be reviewed and Options will get back to you in writing within 21 days of receipt of the appeal. You may also contact the Pennsylvania Department of Health complaint hotline at 1.800.254.5164 and/or the Ombudsman Program located with the local Area Agency on Aging (AAA) of each of the three counties we service: Chester - 610.344.6350, Delaware - 610.490.1300, and Montgomery - 215.784.5413. For licensing questions, you may contact 717.783.1379. You may also contact the Office of the State Long-Term Care Ombudsman, Pennsylvania Department of Aging, 555 Walnut Street, Harrisburg, PA 17101 Tel: 717.783.8975.</li>
            </ol>
        </div>
        """

    # 9. HARRISBURG PA BRANCH (hbhomecare)
    elif branch_lower in ['hbhomecare', 'hbhomecare_staging']:
        rights_html = """
        <div style="font-size:11px;">
            <p style="font-size:11px;text-align:center;margin-bottom:5px;"><b><u>Notice of Patients' Rights and Responsibilities</u></b></p>
            <p style="font-size:11px;text-align:left;margin-bottom:5px;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE FOLLOWING RIGHTS AND RESPONSIBILITIES:</p>
            <ol type="1" style="padding-left: 26px;margin:0;">
                <li>Right to participate in the planning of the client's home care, including the right to accept or refuse services.</li>
                <li>Right to be fully informed of the charges of the services.</li>
                <li>Right to be fully informed of the name, business telephone number and business address of the person supervising the service and how to contact that person.</li>
                <li>Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time.</li>
                <li>Right of confidentiality of patient records.</li>
                <li>Right to have your property and residence treated with respect.</li>
                <li>Right of nondiscrimination in obtaining services from Options because of race, color, religion, creed, national origin, ancestry, disability, sex, or age.</li>
                <li>Responsibility to advise the provider of any changes in your condition or any events that affect your service needs.</li>
                <li>Responsibility to treat the OPTIONS' caregivers with respect.</li>
            </ol>
            <p style="font-size:11px;text-align:center;margin:3px 0;margin-top:5px;"><b><u>Notice of Complaint Procedures</u></b></p>
            <p style="font-size:11px;text-align:left;margin-bottom:5px;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
            <ol type="1" style="padding-left: 26px;margin:0;">
                <li>Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their telephone number is 717-510-8613.</li>
                <li>OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
                <li>The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager.</li>
                <li>OPTIONS will produce a written record of the findings of each complaint investigated.</li>
                <li>The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Manager.</li>
                <li>The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient's property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
                <li>The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
                <li>If you are not satisfied with the proposed resolution, you may appeal to Options Corporate office at 1-800-2-OPTIONS, or in writing to OPTIONS, 6 Montgomery Village Avenue, Suite 330, Gaithersburg, MD 20879, in which case your complaint would be reviewed and Options will get back to you in writing within 21 days of receipt of the appeal. You may also contact the Pennsylvania Department of Health's complaint hotline at 1-800-254-5164 and/or the Ombudsman Program at 717-780-6130 which is located at the Dauphin County Area Agency on Aging (AAA) office.</li>
            </ol>
        </div>
        """

    # 10. DC BRANCH (special case with state check)
    elif branch_lower in ['dchomecare', 'dchomecare_staging']:
        if care_state == "DC":
            rights_html = """
            <div style="font-size:11px;">
                <p style="font-size:14px;text-align:center;margin-bottom:5px;"><b><u>Notice of Patients' Rights and Responsibilities</u></b></p>
                <p style="font-size:11px;margin-bottom:5px;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE FOLLOWING RIGHTS AND RESPONSIBILITIES:</p>
                <ol type="1" style="padding-left: 26px;margin:0;">
                    <li>Right to accept or refuse services.</li>
                    <li>Right to be fully informed of the charges of the services.</li>
                    <li>Right to be fully informed of the name, business telephone number and business address of the person supervising the service and how to contact that person.</li>
                    <li>Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time.</li>
                    <li>Right of confidentiality of patient records.</li>
                    <li>Right to have your property and residence treated with respect.</li>
                    <li>Responsibility to advise the provider of any changes in your condition or any events that affect your service needs.</li>
                    <li>Responsibility to treat the OPTIONS' caregivers with respect.</li>
                    <li>For further assistance, you may call and speak with an OPTIONS manager at 301.562.1100 or 800.267.8466</li>                
                </ol>
                <p style="font-size:11px;text-align:center;margin:3px 0;margin-top:5px;"><b><u>Notice of Complaint Procedures</u></b></p>
                <p style="font-size:11px;margin-bottom:5px;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
                <ol type="1" style="padding-left: 26px;margin:0;">
                    <li>Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their office number is 202.581.2000 for the District of Columbia, 301.562.3100 for Montgomery Co., MD and P.G. County, MD</li>
                    <li>OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
                    <li>The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager or the Care Manager.</li>
                    <li>OPTIONS will produce a written record of the findings of each complaint investigated.</li>
                    <li>The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Manager.</li>
                    <li>The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient's property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
                    <li>The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
                    <li>If you are not satisfied with the proposed resolution, you may appeal to an agency Director at 1-800-2-OPTIONS, or in writing to OPTIONS Director, 6 Montgomery Village Avenue, Suite 330, Gaithersburg, MD 20879, in which case they would review the case and get back to you in writing within 21 days of receipt of the appeal.</li>
                </ol>
            </div>
            """
        else:
            # DC branch in MD - use MD format
            top_margin = "0px"
            rights_html = f"""
            <div style="font-size:11px;">
                <p style="font-size:11px;text-align:center;margin-bottom:5px;"><b><u>Notice of Patients' Rights and Responsibilities</u></b></p>
                <ol type="1" style="padding-left: 26px;margin:0;">
                    <li>A client, or the client representative with legal authority to make health care decisions, has the right to:
                        <ol type="a" style="padding-left: 24px;margin:0;">
                            <li>Be treated with consideration, respect, and full recognition of the client's human dignity and individuality</li>
                            <li>Receive treatment, care, and services that are adequate, appropriate, and in compliance with relevant State, local, and federal laws and regulations</li>
                            <li>Participate in the development of the client's care plan and medical treatment</li>
                            <li>Refuse treatment after the possible consequences of refusing treatment have been fully explained</li>
                            <li>Privacy</li>
                            <li>Be free from mental, verbal, sexual, and physical abuse, neglect, involuntary seclusion, and exploitation</li>
                            <li>Confidentiality</li>
                        </ol>
                    </li>
                    <li>A client or client representative has the right to:
                        <ol type="a" style="padding-left: 24px;margin:0;">
                            <li>Make suggestions or complaints, or present grievances on behalf of the client to the agency, government agencies, or other persons without the threat or fear of retaliation</li>
                            <li>Receive a prompt response, through an established complaint or grievance procedure, to any complaints, suggestions, or grievances the participant may have</li>
                            <li>Have access to the procedures for making a complaint to the Office of Health Care Quality - see (3) below, and to:
                                <ol type="i" style="padding-left: 24px;">
                                    <li>The Adult Protective Services Program of the local department of social services, if the client is an adult; or</li>
                                    <li>The Child Protective Services Program of the local department of social services, if the client is a minor</li>
                                </ol>
                            </li>
                        </ol>
                    </li>
                    <li>A client or client representative has the responsibility to:
                        <ol type="a" style="padding-left: 24px;margin:0;">
                            <li>Advise the Options office of any changes in the care recipient's condition, or of any events that affect the care recipient's service needs.</li>
                            <li>Treat the Options caregivers with respect.</li>
                            <li>Pay Options invoices in a timely manner as indicated below under the "Notice of Billing Procedures" section.</li>
                        </ol>
                    </li>
                </ol>

                <p style="font-size:11px;text-align:center;margin:3px 0;margin-top:{top_margin};"><b><u>Notice of Complaint Procedures</u></b></p>
                <ol type="1" style="padding-left: 26px;margin:0;">
                    <li>Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their office number is 410.224.2700 for Annapolis, 410.448.1100 for Baltimore, 410.893.9914 for Bel Air, 301.562.3100 for Bethesda, 301.624.5630 for Frederick, and 301.392.1387 for La Plata</li>
                    <li>OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
                    <li>The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager or the Care Manager.</li>
                    <li>OPTIONS will produce a written record of the findings of each complaint investigated.</li>
                    <li>The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Manager.</li>
                    <li>The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient's property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
                    <li>The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
                    <li>If you are not satisfied with the proposed resolution, you may appeal to an agency Director at 1-800-2-OPTIONS, or in writing to OPTIONS Director, 555 Quince Orchard Road, Suite 240, Gaithersburg, MD 20878, in which case they would review the case and get back to you in writing within 21 days of receipt of the appeal. You may also write to Barbara Fagan, Survey Coordinator, Office of Health Care Quality, Bland Bryant Building, Spring Grove Hospital Center, 55 Wade Avenue, Catonsville, MD 21228, or you may call the State of Maryland's Residential Service Agency Hotline at 1-877-4MD-DHMH.</li>
                </ol>
            </div>
            """

    # 11. Default rights HTML if no branch matches
    if not rights_html:
        rights_html = f"""
        <div style="font-size:11px; margin-top:10px;">
            <p style="text-align:center;"><b><u>Notice of Patients' Rights and Responsibilities</u></b></p>
            <p>You have the right to be treated with dignity and respect, to receive quality care, and to have your privacy protected. You also have the responsibility to provide accurate information, treat caregivers with respect, and pay for services as agreed.</p>
            <p>For complaints, please contact the Community Relations Manager at {manager_phone}.</p>
        </div>
        """

    # Build styles with dynamic margins
    style = f"""
    <style>
        @page {{ 
            size: letter; 
            margin-top: {margins['top']}in;
            margin-bottom: {margins['bottom']}in;
            margin-left: {margins['left']}in;
            margin-right: {margins['right']}in;
        }}
        body {{ font-family: Helvetica, Arial, sans-serif; font-size: 7pt; line-height: 1.15; color: #000; }}
        .page-break {{ pdf-next-page: true; }}
        
        /* Page 1 Specific Styles */
        .header-table {{ width: 100%; border-collapse: collapse; }}
        .office-info {{ width: 45%; font-size: 7pt; vertical-align: top; }}
        .title-info {{ width: 55%; text-align: right; vertical-align: top; }}
        .logo-container {{ text-align: right; margin-bottom: 10px; }}
        .logo-img {{ max-width: 220px; max-height: 90px; display: block; margin-left: auto; margin-right: 0; }}
        .main-title {{ font-size: 26pt; font-weight: bold; color: #003366; margin: 0; line-height: 0.9; }}
        .sub-title {{ font-size: 10pt; font-weight: bold; margin-bottom: 5px; letter-spacing: 1px; }}
        .service-agreement-center {{ text-align: center; font-size: 16pt; font-weight: bold; margin: 15px 0; }}

        .admin-grid {{ width: 100%; border-collapse: collapse; margin: 12px 0; }}
        .admin-grid th {{ border: 0.5pt solid black; background-color: #f2f2f2; font-size: 7.5pt; padding: 4pt; line-height: 1; }}
        .admin-grid td {{ border: 0.5pt solid black; padding: 6pt; text-align: center; font-weight: bold; font-size: 9.5pt; }}
        .legal-text {{ text-align: justify; margin-bottom: 8px; }}

        /* Page 2 Specific Styles */
        .section-title {{ font-size: 10pt; text-align: center; font-weight: bold; text-decoration: underline; margin-bottom: 10px; }}
        .sub-section-title {{ font-size: 10pt; text-align: center; font-weight: bold; text-decoration: underline; margin-top: 20px; margin-bottom: 10px; }}
        
        ol {{ padding-left: 25px; margin-top: 0; }}
        ol li {{ margin-bottom: 5px; text-align: justify; }}
        ol.nested-alpha {{ list-style-type: lower-alpha; padding-left: 20px; }}
        
        /* Signatures & Footer */
        .sig-table {{ width: 100%; margin-top: 30px; border-collapse: collapse; }}
        .sig-box {{ border-top: 1px solid black; text-align: center; font-size: 8pt; padding-top: 2px; }}
        .footer-code {{ font-size: 8pt; margin-top: 20px; text-align: right; }}
        .force-page-break {{
            page-break-before: always;
            clear: both;
        }}
        
        /* Form Styles */
        .form-field {{ border-bottom: 1px solid black; min-height: 15px; margin: 5px 0; }}
        .form-label {{ font-weight: bold; margin-top: 10px; }}
        .checkbox-container {{ margin: 5px 0; }}
        .checkbox-label {{ margin-left: 5px; }}
        .check-box {{ border: 1px solid black; width: 12px; height: 12px; display: inline-block; margin-right: 5px; }}
        .voided-check-box {{ border: 2px double black; padding: 30px; text-align: center; margin-top: 15px; min-height: 100px; }}
    </style>
    """

    # Build logo section with proper image handling
    local_path = r"C:\Users\User\service-agreement-app\Image111.bmp"
    if logo_path and logo_path.strip():
        logo_html = f'<img src="{local_path}" class="logo-img" />'
    else:
        # Fallback to text-based logo
        logo_html = '<div class="main-title">OPTIONS</div><div class="sub-title">FOR SENIOR AMERICA</div>'
    
    # Build office address
    office_address_full = f"{office_address}"
    if office_suite:
        office_address_full += f"<br/>{office_suite}"
    office_address_full += f"<br/>{office_city}, {office_state} {office_zip}"
    
    # ========== PAGE 1: MAIN AGREEMENT ==========
    page1 = f"""
    <table class="header-table">
        <tr>
            <td class="office-info">
                {office_name}<br/>{office_address_full}<br/>
                _______________________________<br/>Tel: {office_tel}<br/>Fax: {office_fax}<br/><br/>
                <u>Name Address of Responsible Party</u><br/>
                <b>{resp_name}</b><br/>
                {safe_get('clt_address')}<br/>
                {safe_get('clt_city')}, {safe_get('clt_state')} {safe_get('clt_zip')}<br/><br/>
                
                
            </td>
            <td class="title-info">
                <div class="logo-container">
                    {logo_html}
                </div>
                <div style="font-weight: bold; margin-top: 5px; text-align: right;">Date: {agreement_date}</div>
            </td>
        </tr>
    </table>

    <div style="text-align: center; margin-top: 15px;">
        <div class="service-agreement-center" style="margin-bottom: 0px;">SERVICE AGREEMENT</div>
        <div style="font-size: 9pt; margin-top: 5px;"><b>For Care Recipient: {care_name} residing at <b>{care_addr}</b></div>
        
    </div>

    <table class="admin-grid">
        <tr>
            <th>Initial Inquiry<br/>date</th>
            <th>Start Order and/or Instructions<br/>Given by</th>
            <th>On</th>
            <th>Services to<br/>Start on</th>
            <th>At (time)</th>
        </tr>
        <tr>
            <td>{safe_get('initial_inquiry_date')}</td>
            <td>{safe_get('instructions_given_by', resp_name)}</td>
            <td>{agreement_date}</td>
            <td>{safe_get('start_date')}</td>
            <td>{safe_get('services_start_time', '12:00 pm')}</td>
        </tr>
    </table>


    <p class="legal-text"><b>REQUIRED SERVICES:</b> In addition to the general services that our caregivers provide such as assistance with activities of daily living, meal preparation, light housekeeping, and laundry, the required services as stated by the responsible party/client are: <b>{safe_get('care_type')}</b></p>
    
    <p class="legal-text"><b>FREQUENCY DURATION OF VISITS:</b></p>

    <p class="legal-text"><b>FEES:</b> <b>${hourly_rate:.2f}/hr</b></p>
    {hazards_html}
    
    {competency_html}

    {final_charges_html}

    <p class="legal-text"><b>PAYMENT OBLIGATIONS:</b> The parties responsible for payment include the person who initiates arrangements for our services, as well as the care recipient and the care recipient's power of attorney or guardian. The responsibility for payment cannot be shifted simply by asking us to bill an insurance company or a third party. Your responsibility extends to making timely and prompt payments at all times. In the event the client or care recipient cancels a shift with less than 24-hour notice, then a charge for our minimum 2-hour visit will apply.</p>

    {federal_holidays_html}
    {live_in_services_html}
    """

    # Add live-in services section if applicable
    if requires_live_in:
        page1 += f"""
    {live_in_services_html}
    """

    page1 += f"""
    <table class="sig-table">
        <tr>
            <td width="48%" align="center">
                <p><b>{resp_name}</b></p>
                <div class="sig-box">Name of Responsible Party</div>
            </td>
            <td width="4%"></td>
            <td width="48%" align="center">
                <p><b>{clt_relationship}</b></p>
                <div class="sig-box">Relationship to Care Recipient</div>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding-top:20px;">
                <p>(SEAL)</p>
                <div class="sig-box">Signature</div>
            </td>
            <td></td>
            <td align="center" style="padding-top:20px;">
                <p><b>{agreement_date}</b></p>
                <div class="sig-box">Date</div>
            </td>
        </tr>
    </table>
    <div class="footer-code">{footer_version}</div>
    """

    # ========== PAGE 1 CONTINUATION: ADDITIONAL TERMS ==========
    page1_cont = f"""
  <div style="page-break-before: always;">
    
    {needs_and_valuables_html}

    {notice_period_html}
    
    {medication_html}
    
    

    <p class="legal-text"><b>OUR CARE PROVIDERS CANNOT BE HIRED BY YOU:</b> OPTIONS is not a staffing agency. Our care providers introduced to you by OPTIONS cannot be employed directly by you, either during or after using OPTIONS' services. If you wish to employ a care provider after a one-year period of their termination of employment with OPTIONS, you must pay OPTIONS the larger of a $9,000 lump-sum placement fee or the value of eight (8) weeks of service charges. This payment is due within 10 calendar days of the care provider's employment with you.</p>

    <p class="legal-text"><b>RECORD KEEPING:</b> OPTIONS' care providers track time and tasks on a Daily Progress Notes form. You or your designee must allow time for this form to be completed and signed weekly. If you do not sign, you must inform OPTIONS in writing, and the lack of signature will not invalidate the recorded hours or tasks.</p>

    <p class="legal-text"><b>MILEAGE REIMBURSEMENT:</b> A charge of ${mileage_rate:.2f} per mile applies when the Care Provider uses their personal vehicle for duties such as errands or appointments for the Care Recipient. No mileage charge applies if the Care Provider uses the Care Recipient's vehicle.</p>

  {vehicle_html}
  {general_provisions_html}

    <p style="margin-top: 20px; font-size: 8.8pt; text-align: justify;">I have read and agree to the above listed terms, and understand that this agreement is a contract under seal.</p>

    <table style="width: 100%; margin-top: 20px; border-collapse: collapse;">
        <tr>
            <td width="48%" align="center">
                <div style="font-weight: bold; font-size: 9pt;">{resp_name}</div>
                <div style="border-top: 1px solid black; font-size: 8pt; padding-top: 2px; margin-top: 2px;">Name of Responsible Party</div>
            </td>
            <td width="4%"></td>
            <td width="48%" align="center">
                <div style="font-weight: bold; font-size: 9pt;">{clt_relationship}</div>
                <div style="border-top: 1px solid black; font-size: 8pt; padding-top: 2px; margin-top: 2px;">Relationship to Care Recipient</div>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding-top: 15px;">
                <div style="font-size: 8pt;">(SEAL)</div>
                <div style="border-top: 1px solid black; font-size: 8pt; padding-top: 2px; margin-top: 2px;">Signature</div>
            </td>
            <td></td>
            <td align="center" style="padding-top: 15px;">
                <div style="font-weight: bold; font-size: 9pt;">{agreement_date}</div>
                <div style="border-top: 1px solid black; font-size: 8pt; padding-top: 2px; margin-top: 2px;">Date</div>
            </td>
        </tr>
    </table>
    <div class="footer-code">{footer_version}</div>
    """

    # ========== PAGE 2: PATIENT RIGHTS AND RESPONSIBILITIES ==========
    page2 = f"""
     <div style="page-break-before: always;">
    
    {rights_html}

    <div style="margin-top: 10px;">
        <p style="font-size:11px;text-align:center;margin:3px 0;margin-top:3px;margin-bottom:3px;"><b><u>Notice of Billing Procedures</u></b></p>
        <p style="font-size:11px;">BILLING, BILLING ERRORS AND REFUNDS ARE TREATED AS FOLLOWS:</p>
        <ol type="1" style="padding-left: 18px;margin:0;">
            <li><u>Billing Method:</u> &nbsp;OPTIONS is a long-term home care agency, and billing is done, by way of invoices, on a weekly or bi-weekly basis. Given that billing is typically done after services are provided, invoices are due upon receipt.</li>
            <li><u>When Payers are Insurance Companies or Third Parties:</u> &nbsp;OPTIONS typically seeks to obtain an "Assignment of Benefits" form from the care recipient or their designees, and OPTIONS then invoices the third party, copying the care recipient or their designees with all invoices sent to the third party.</li>
            <li><u>Patient Notification of Changes in Fees and Charges:</u> &nbsp;We endeavor to notify the care recipient or their designees in writing of any changes in fees or charges, at least two (2) weeks ahead of the effective date of the new changes. Rate increases typically occur following each 12 months of service.</li>
            <li><u>Correction of Billing Errors and Refund Policy:</u> &nbsp;Billing errors will be corrected in subsequent invoices. All refunds are either credited to the care recipient's account if it is an ongoing case, or are paid back to the care recipient.</li>
            <li><u>Collection of Delinquent Care Recipient Accounts:</u> &nbsp;Any account more than 30 days past due shall be subject to interest charges of 1 ½ % per month (18% annual) from the invoice due date. If it becomes necessary to refer your account to an attorney for collection, you will be responsible for court costs and attorney's fees of no less than 1/3 (33.33%) of the principal balance, in addition to the interest charges listed above.</li>
        </ol>
    </div>

    <table style="width: 100%; margin-top: 5px; border-collapse: collapse;">
        <tr>
            <td width="48%" align="center">
                <div style="font-weight: bold; font-size: 9pt; height: 12pt;">{resp_name}</div>
                <div style="border-top: 1px solid black; font-size: 8pt; padding-top: 2px;">Name of Responsible Party</div>
            </td>
            <td width="4%"></td>
            <td width="48%" align="center">
                <div style="font-weight: bold; font-size: 9pt; height: 12pt;">{clt_relationship}</div>
                <div style="border-top: 1px solid black; font-size: 8pt; padding-top: 2px;">Relationship to Care Recipient</div>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding-top: 11px;">
                <div style="font-size: 8pt; height: 12pt;">(SEAL)</div>
                <div style="border-top: 1px solid black; font-size: 8pt; padding-top: 2px;">Signature</div>
            </td>
            <td></td>
            <td align="center" style="padding-top: 11px;">
                <div style="font-weight: bold; font-size: 9pt; height: 12pt;">{agreement_date}</div>
                <div style="border-top: 1px solid black; font-size: 8pt; padding-top: 2px;">Date</div>
            </td>
        </tr>
    </table>
    <div class="footer-code">{footer_version}</div>
    """

    # ========== PAGE 3: EFT AUTHORIZATION ==========
    page3 = f"""
    <div style="page-break-before: always;">
   <div style="text-align: center; margin-top: 10px;">
        <div style="font-size: 14pt; font-weight: bold; margin-bottom: 5px;">Authorization for a Repeating Electronic Funds Transfer</div>
        <div style="font-size: 9pt; font-style: italic; margin-bottom: 15px;">(Save time and postage. Avoid interest charges, late payments, and termination notices)</div>
    </div>

    <p class="legal-text" style="margin-top: 15px; text-align: justify;">
        I, the undersigned, acknowledge that invoices prepared by Options for Senior America (Options) are due upon receipt, and therefore hereby authorize Options to withdraw any amounts owed by me on the same day as the invoice is prepared and emailed to me. This funds withdrawal is made by initiating an electronic funds transfer, as a debit through ACH (Automated Clearing House) from my account at the financial institution (hereinafter "Bank") indicated below. I also agree that, in the event the below mentioned care recipient passes away, I will not close this referenced bank account until I receive notification from Options that the final Options invoice is paid in full using the method of payment herein described. Furthermore, I authorize Bank to accept and to debit entries indicated by Options from my account.
    </p>
    
    <p class="legal-text" style="text-align: justify;">
        This authorization is to remain in full force and effect until Options and Bank have received written notice from me of its termination in such time and in such manner as to afford Options and Bank reasonable opportunity to act on it.
    </p>

    <div style="margin-top: 20px;">
        <div class="form-label">Care Recipient Name:</div>
        <div class="form-field" style="font-weight: bold;">{care_name}</div>
    </div>

    <div style="margin-top: 15px;">
        <div class="form-label">Client Bank Account Signatory Name:</div>
        <div class="form-field" style="font-weight: bold;">{resp_name}</div>
    </div>

    <div style="margin-top: 15px;">
        <div class="form-label">Client Signature:</div>
        <div class="form-field"></div>
    </div>

    <div style="margin-top: 15px;">
        <div class="form-label">Date:</div>
        <div class="form-field" style="font-weight: bold;">{agreement_date}</div>
    </div>

    <div style="text-align: center; margin: 20px 0; font-size: 10pt;">****************************************************************</div>

    <div style="font-weight: bold; font-size: 10pt; margin-top: 20px; margin-bottom: 10px;">Account Information</div>

    <div style="margin-top: 10px;">
        <div class="form-label">Bank Name, City, and State:</div>
        <div class="form-field">{bank_name}{', ' + bank_city if bank_city else ''}{', ' + bank_state if bank_state else ''}</div>
    </div>

    <div style="margin-top: 10px;">
        <div class="form-label">Routing Transit #:</div>
        <div class="form-field">{routing_number}</div>
    </div>

    <div style="margin-top: 10px;">
        <div class="form-label">Account Number:</div>
        <div class="form-field">{account_number}</div>
    </div>

<div style="margin-top: 10px;">
    <span style="font-weight: bold;">Account Type:</span>
</div>
<div style="margin-left: 40px; margin-top: 5px;">
    <div>Checking</div>
    <div style="margin-top: 3px;">Saving</div>
</div>

    <div class="voided-check-box">
        <div style="font-size: 9pt; font-weight: bold;">-------Please Attach a Voided Check Here----------</div>
    </div>
    
    <div class="footer-code" style="margin-top: 20px;">{footer_version}</div>
    """

    # ========== PAGE 3.1: CONSUMER NOTICE (For PA and specific branches) ==========
    page3_1 = ""
    if requires_consumer_notice:
        page3_1 = f"""
      <div style="page-break-before: always;">
    
    <div class="section-title" style="text-align:center; font-weight:bold; text-decoration:underline; font-size:11pt; margin-top: 10px;">
        Consumer Notice
    </div>

    <p class="legal-text" style="margin-top: 15px; text-align: justify;">
        <b>IMPORTANT CONSUMER INFORMATION:</b> This service agreement is a legally binding contract. Please read all terms carefully before signing. You have the right to review this agreement and ask questions about any terms you do not understand.
    </p>

    <p class="legal-text" style="text-align: justify;">
        <b>YOUR RIGHTS:</b> You have the right to receive services in accordance with this agreement and applicable state regulations. You may file a complaint with {state_authority} if you believe your rights have been violated or if you have concerns about the quality of care provided.
    </p>

    <p class="legal-text" style="text-align: justify;">
        <b>TERMINATION:</b> Either party may terminate this agreement in accordance with the notice provisions specified herein. {notice_period_text}
    </p>

    <p class="legal-text" style="text-align: justify;">
        <b>DISPUTE RESOLUTION:</b> Any disputes arising from this agreement shall be resolved in accordance with the laws of the state of {state_code}.
    </p>

    <table style="width: 100%; margin-top: 20px; border-collapse: collapse;">
        <tr>
            <td width="48%" align="center">
                <div style="font-weight: bold; font-size: 9pt;">{resp_name}</div>
                <div style="border-top: 1px solid black; font-size: 8pt; padding-top: 2px; margin-top: 2px;">Name of Responsible Party</div>
            </td>
            <td width="4%"></td>
            <td width="48%" align="center">
                <div style="font-weight: bold; font-size: 9pt;">{agreement_date}</div>
                <div style="border-top: 1px solid black; font-size: 8pt; padding-top: 2px; margin-top: 2px;">Date</div>
            </td>
        </tr>
    </table>
    <div class="footer-code">{footer_version}</div>
    """

    # Combine all pages
    full_html = f"<html><head>{style}</head><body>{page1}{page1_cont}{page2}{page3}{page3_1}</body></html>"

    # Generate PDF
    pdf_buffer = BytesIO()
    try:
        result = pisa.CreatePDF(full_html, dest=pdf_buffer)
        if result.err:
            raise Exception(f"PDF generation error: {result.err}")
        pdf_buffer.seek(0)
        return pdf_buffer
    except Exception as e:
        pdf_buffer.close()
        raise Exception(f"Failed to generate PDF: {str(e)}")