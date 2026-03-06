"""Page 2 - Patient Rights and Billing Procedures (matches dynamic_sa_page2.php)"""
from datetime import datetime

def get_content_category(branch, care_state):
    """
    Categorize branches by content length for dynamic spacing
    Returns: 'long', 'medium', or 'short'
    """
    # ===== LONG CONTENT (MD/NJ style with nested lists) =====
    long_content_branches = [
        'anhomecare', 'anhomecare_staging', 
        'bahomecare', 'bahomecare_staging',
        'blhomecare', 'blhomecare_staging', 
        'fkhomecare', 'fkhomecare_staging',
        'lphomecare', 'lphomecare_staging', 
        'testhomecare',
        'wenjhomecare', 'wenjhomecare_staging',# NJ branches
        'tomdhomecare', 'tomdhomecare_staging' ,
        'wenjhomecare', 'wenjhomecare_staging'   
        
    ]
    
    # ===== MEDIUM CONTENT (VA, NC, PA, IN, etc.) =====
    medium_content_branches = [
        # Virginia branches
        'nvahomecare', 'nvahomecare_staging', 
        'nvahomecarearchive', 'nvahomecarearchive_staging',
        'rihomecare', 'rihomecare_staging', 
        'mnhomecare', 'mnhomecare_staging',
        'lovahomecare', 'lovahomecare_staging', 
        'sfvahomecare', 'sfvahomecare_staging',
        'amfvahomecare', 'amfvahomecare_staging', 
        'wfvahomecare', 'wfvahomecare_staging',
        'cfairfaxhomecare', 'cfairfaxhomecare_staging',
        
        # North Carolina branches
        'gbhomecare', 'gbhomecare_staging',
        'rdhomecare', 'rdhomecare_staging',
        
        # Pennsylvania branches
        'hbhomecare', 'hbhomecare_staging',
        'nspahomecare', 'nspahomecare_staging',
        
        # # Indiana branches
        'lkinhomecare', 'lkinhomecare_staging',
        
        # Cleveland/Other
        'clhomecare', 'clhomecare_staging',
        'ciohhomecare', 'ciohhomecare_staging',
        'blmdhomecare', 'blmdhomecare_staging'
    ]
    
    # ===== SHORT CONTENT (GA, FL, AZ, MI, etc.) =====
    short_content_branches = [
        # Georgia branches
        'athomecare', 'athomecare_staging',
        'scgahomecare', 'scgahomecare_staging',
        
        # Florida branches
        'tahomecare', 'tahomecare_staging',
        'woflhomecare', 'woflhomecare_staging',
        'lzflhomecare', 'lzflhomecare_staging',
        'wpbflhomecare', 'wpbflhomecare_staging',
        
        # Arizona branches
        'chazhomecare', 'chazhomecare_staging',
        
        # Michigan branches
        'shmihomecare', 'shmihomecare_staging'
    ]
    
    # Special case: DC branches
    if branch in ['dchomecare', 'dchomecare_staging']:
        if care_state == "DC":
            return 'medium'  # DC content is medium
        else:
            return 'long'    # MD content is long
    
    if branch in long_content_branches:
        return 'long'
    elif branch in medium_content_branches:
        return 'medium'
    else:
        return 'short'

def generate_page2(data):
    """
    Generate Page 2 HTML - matches dynamic_sa_page2.php logic
    """
    # Get values directly from data
    branch = data.get('branch_code', '').lower()
    care_state = data.get('care_state', '').upper()
        # ===== CRITICAL DEBUG =====
    print("\n" + "="*60)
    print("DEBUG - Page 2 Branch Detection")
    print("="*60)
    print(f"Branch: {branch}")
    print(f"Care State: {care_state}")
    print(f"Content Category: {get_content_category(branch, care_state)}")
    print("="*60 + "\n")

    # Get client information for signatures
    clt_first = data.get('clt_first_name', '')
    clt_last = data.get('clt_last_name', '')
    
    # Fix: Handle empty relationship properly
    clt_relationship = data.get('clt_relationship', '')
    if not clt_relationship or clt_relationship.strip() == '':
        clt_relationship = 'Self'
        print(f"DEBUG - page2 - Setting default relationship to: '{clt_relationship}'")
    
    handled_by = data.get('handled_by', '')
    
    # Get current date for signature
    current_date = datetime.now().strftime("%m/%d/%Y")
    
    # ===== Get content category for dynamic spacing =====
    content_category = get_content_category(branch, care_state)
    print(f"DEBUG - Page 2 content category: {content_category}")
    
    # Set dynamic styles based on content category
    if content_category == 'long':
        # Tight spacing for long content (MD/NJ)
        base_font_size = "6.5px"
        title_font_size = "8.5px"
        line_height = "1.0"
        section_margin = "2px"
        list_margin = "0"
        list_padding = "14px"
        billing_margin = "2px"
        signature_margin = "5px"
        container_min_height = "auto"
        use_flex_spacer = False
    elif content_category == 'medium':
        # Medium spacing (VA, NC, PA, IN)
        base_font_size = "6.8px"        
        title_font_size = "8.5px"       
        line_height = "1.0"              
        section_margin = "2px"          
        list_margin = "0"
        list_padding = "14px"           
        billing_margin = "2px"           
        signature_margin = "5px"          
        container_min_height = "auto"    
        use_flex_spacer = False    
    else:  # short
        # Loose spacing for short content (GA, FL, AZ, MI)
        base_font_size = "7.5px"
        title_font_size = "9px"
        line_height = "1.2"
        section_margin = "5px"
        list_margin = "2px"
        list_padding = "16px"
        billing_margin = "5px"
        signature_margin = "10px"
        container_min_height = "9in"
        use_flex_spacer = True
    
    # Start HTML with dynamic styles
    html = f'<div><div style="font-size:{base_font_size};margin-top:0;line-height:{line_height};'
    
    if use_flex_spacer:
        html += f' min-height:{container_min_height}; display:flex; flex-direction:column;">'
    else:
        html += '">'
    
    # ===== MARYLAND & NEW JERSEY BRANCHES =====
    md_nj_branches = [
        'anhomecare', 'anhomecare_staging', 'bahomecare', 'bahomecare_staging', 
        'blhomecare', 'blhomecare_staging', 'fkhomecare', 'fkhomecare_staging', 
        'lphomecare', 'lphomecare_staging', 'testhomecare',
        'tomdhomecare', 'tomdhomecare_staging',
        'wenjhomecare', 'wenjhomecare_staging'
    ]
    
    # Also include dchomecare when it's NOT in DC (Maryland)
    if branch in md_nj_branches or (branch in ['dchomecare', 'dchomecare_staging'] and care_state != "DC"):
        print("✓ MD/NJ CONDITION MET - Generating Patient Rights")
    
    if branch in md_nj_branches:
        top_margin = "0px"
        if branch in ['bahomecare', 'bahomecare_staging', 'lphomecare', 'lphomecare_staging']:
            top_margin = "0px"
        
        # Check if NJ branch
        is_nj = branch in ['wenjhomecare', 'wenjhomecare_staging']
        
        # Barbara Fagan / Maryland Hotline clause
        md_hotline = ""
        if not is_nj:
            md_hotline = f'<li style="margin-bottom:{list_margin};">You may write to Barbara Fagan, Survey Coordinator, Office of Health Care Quality, Bland Bryant Building, Spring Grove Hospital Center, 55 Wade Avenue, Catonsville, MD 21228, or you may call the State of Maryland’s Residential Service Agency Hotline at 1-877-4MD-DHMH.</li>'
        
        # Phone numbers for Complaint Intake
        if is_nj:
            office_num = "973.803.0901"
        else:
            office_num = "410.224.2700 for Annapolis, 410.448.1100 for Baltimore, 410.893.9914 for Bel Air, 301.562.3100 for Bethesda, 301.624.5630 for Frederick, and 301.392.1387 for La Plata"
        
        html += f'''
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Patients’ Rights and Responsibilities</u></b></p>
        <ol class="main-list" style="padding-left: {list_padding}; margin:0; list-style-type: decimal;">
            <li style="margin-bottom: {list_margin};">
                A client, or the client representative with legal authority to make health care decisions, has the right to:
                <ol class="alpha-list" style="padding-left: 14px; margin:0; list-style-type: lower-alpha;">
                    <li style="margin-bottom:{list_margin};">Be treated with consideration, respect, and full recognition of the client’s human dignity and individuality</li>
                    <li style="margin-bottom:{list_margin};">Receive treatment, care, and services that are adequate, appropriate, and in compliance with relevant State, local, and federal laws and regulations</li>
                    <li style="margin-bottom:{list_margin};">Participate in the development of the client’s care plan and medical treatment</li>
                    <li style="margin-bottom:{list_margin};">Refuse treatment after the possible consequences of refusing treatment have been fully explained</li>
                    <li style="margin-bottom:{list_margin};">Privacy</li>
                    <li style="margin-bottom:{list_margin};">Be free from mental, verbal, sexual, and physical abuse, neglect, involuntary seclusion, and exploitation</li>
                    <li style="margin-bottom:{list_margin};">Confidentiality</li>
                </ol>
            </li>
            <li style="margin-bottom: {list_margin};">A client or client representative has the right to:
                <ol class="alpha-list" style="padding-left: 14px; margin:0; list-style-type: lower-alpha;">
                    <li style="margin-bottom:{list_margin};">Make suggestions or complaints, or present grievances on behalf of the client to the agency, government agencies, or other persons without the threat or fear of retaliation</li>
                    <li style="margin-bottom:{list_margin};">Receive a prompt response, through an established complaint or grievance procedure, to any complaints, suggestions, or grievances the participant may have</li>
                    <li style="margin-bottom:{list_margin};">Have access to the procedures for making a complaint to the Office of Health Care Quality - see (3) below, and to:
                        <ol class="roman-list" style="padding-left: 14px; margin:0; list-style-type: lower-roman;">
                            <li style="margin-bottom:{list_margin};">The Adult Protective Services Program of the local department of social services, if the client is an adult; or</li>
                            <li style="margin-bottom:{list_margin};">The Child Protective Services Program of the local department of social services, if the client is a minor</li>
                        </ol>
                    </li>
                </ol>
            </li>
            {md_hotline}
            <li style="margin-bottom: {list_margin};">A client or client representative has the responsibility to:
                <ol class="alpha-list" style="padding-left: 14px; margin:0; list-style-type: lower-alpha;">
                    <li style="margin-bottom:{list_margin};">Advise the Options office of any changes in the care recipient’s condition, or of any events that affect the care recipient’s service needs.</li>
                    <li style="margin-bottom:{list_margin};">Treat the Options caregivers with respect.</li>
                    <li style="margin-bottom:{list_margin};">Pay Options invoices in a timely manner as indicated below under the “Notice of Billing Procedures” section.</li>
                </ol>
            </li>
        </ol>

        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;margin-top:{top_margin};"><b><u>Notice of Complaint Procedures</u></b></p>
        <ol class="main-list" style="padding-left: {list_padding}; margin:0; list-style-type: decimal;">
            <li style="margin-bottom:{list_margin};">Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their office number is {office_num}.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
            <li style="margin-bottom:{list_margin};">The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager or the Care Manager.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS will produce a written record of the findings of each complaint investigated.</li>
            <li style="margin-bottom:{list_margin};">The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Manager.</li>
            <li style="margin-bottom:{list_margin};">The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient’s property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
            <li style="margin-bottom:{list_margin};">The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
'''
        if is_nj:
            html += f'<li style="margin-bottom:{list_margin};">If you are not satisfied with the proposed resolution, you may appeal to an agency Director at 973.803.0901, or in writing to OPTIONS Director, 70 South Orange Avenue, Suite 105, Livingston, NJ 07039 in which case they would review the case and get back to you in writing within 21 days of receipt of the appeal. You may also write to he New Jersey Office of the Attorney General, Division of Consumer Affairs, Certified Homemaker-Home Health Aide Unit, 124 Halsey Street, 6th Floor, P.O. Box 47030, Newark, NJ 07101 - 973.504.6430.</li>'
        else:
            html += f'<li style="margin-bottom:{list_margin};">If you are not satisfied with the proposed resolution, you may appeal to an agency Director at 1-800-2-OPTIONS, or in writing to OPTIONS Director, 555 Quince Orchard Road, Suite 240, Gaithersburg, MD 20878, in which case they would review the case and get back to you in writing within 21 days of receipt of the appeal.  You may also write to Barbara Fagan, Survey Coordinator, Office of Health Care Quality, Bland Bryant Building, Spring Grove Hospital Center, 55 Wade Avenue, Catonsville, MD 21228, or you may call the State of Maryland’s Residential Service Agency Hotline at 1-877-4MD-DHMH.</li>'
        
        html += '</ol>'
    
    # ===== GEORGIA BRANCHES =====
    elif branch in ['athomecare', 'athomecare_staging', 'scgahomecare', 'scgahomecare_staging']:
        html += f'''
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>NOTICE OF RIGHTS AND RESPONSIBILITIES</u></b></p>
        <p style="font-size:{base_font_size};text-align:center;margin:{section_margin} 0;"><b>You are a valued customer, and you have the following rights and responsibilities</b></p>
        <ol type="1" style="padding-left: {list_padding}; margin:0">
            <li style="margin-bottom:{list_margin};">Right to be promptly and fully informed of any changes in the plan of service.</li>
            <li style="margin-bottom:{list_margin};">Right to accept or refuse services.</li>
            <li style="margin-bottom:{list_margin};">Right to be fully informed of the charges of services.</li>
            <li style="margin-bottom:{list_margin};">Right to be informed of the name, business telephone number and business address of the person supervising the services and how to contact that person.</li>
            <li style="margin-bottom:{list_margin};">Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time. The complaint procedure provided shall include the business address and telephone number of the person designated by the provider to handle complaints and questions.</li>
            <li style="margin-bottom:{list_margin};">Right of confidentiality of client records.</li>
            <li style="margin-bottom:{list_margin};">Right to have property and residence treated with respect.</li>
            <li style="margin-bottom:{list_margin};">Right to receive a written notice of the address and telephone number of the state licensing authority, namely the department of Human Resources which is charged the responsibility of licensing the provider and investigating client complaints that appear to violate licensing regulation.</li>
            <li style="margin-bottom:{list_margin};">Right to obtain a copy of the provider’s most recent completed report of licensure inspection from the provider upon written request. The provider is not required to release the report of licensure inspection until the provider has had an opportunity to file a written plan of correction for the violations, if any, identified.</li>
            <li style="margin-bottom:{list_margin};">The facility may charge the client reasonable photocopying charges.</li>
            <li style="margin-bottom:{list_margin};">Responsibility to advise the provider of any changes in the care recipient’s condition of any events that affect the care recipient’s service needs</li>
            <li style="margin-bottom:{list_margin};">For further assistance or other issues, you may call the OPTIONS Manager, at 404-634-1111, or you may call the State Licensing authority for private home care providers at: Georgia Department of Community Health, Healthcare Facility Regulation Division, 2 Peachtree Street, NW, Suite 31-447, Atlanta, GA 30303-3142, (404) 657-5850. For complaints (404) 657-5728. It is your right to report abuse, neglect or exploitation. Please call toll free 1-800-962-2873.</li>
        </ol>
        '''
    
    # ===== CLEVELAND/DC/OTHER BRANCHES (excluding shmihomecare which has its own section) =====
    elif branch in ['clhomecare', 'clhomecare_staging', 'blmdhomecare', 'blmdhomecare_staging', 
                    'ciohhomecare', 'ciohhomecare_staging', 'chazhomecare', 'chazhomecare_staging']:
        
        manager_info = get_manager_info(branch)
        html += f'''
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Patients’ Rights and Responsibilities</u></b></p>
        <p style="font-size:{base_font_size};margin:{section_margin} 0;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE FOLLOWING RIGHTS AND RESPONSIBILITIES:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Right to accept or refuse services.</li>
            <li style="margin-bottom:{list_margin};">Right to be fully informed of the charges of the services.</li>
            <li style="margin-bottom:{list_margin};">Right to be fully informed of the name, business telephone number and business address of the person supervising the service and how to contact that person.</li>
            <li style="margin-bottom:{list_margin};">Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time.</li>
            <li style="margin-bottom:{list_margin};">Right of confidentiality of patient records.</li>
            <li style="margin-bottom:{list_margin};">Right to have your property and residence treated with respect.</li>
            <li style="margin-bottom:{list_margin};">Responsibility to advise the provider of any changes in your condition or any events that affect your service needs.</li>
            <li style="margin-bottom:{list_margin};">Responsibility to treat the OPTIONS’ caregivers with respect.</li>
            <li style="margin-bottom:{list_margin};">For further assistance, you may call and speak with an OPTIONS manager at {manager_info['manager_phone']}</li>                
        </ol>
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Complaint Procedures</u></b></p>
        <p style="font-size:{base_font_size};margin:{section_margin} 0;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their office number is {manager_info['complaint_phone']}.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
            <li style="margin-bottom:{list_margin};">The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager or the Care Manager.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS will produce a written record of the findings of each complaint investigated.</li>
            <li style="margin-bottom:{list_margin};">The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Manager.</li>
            <li style="margin-bottom:{list_margin};">The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient’s property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
            <li style="margin-bottom:{list_margin};">The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
            <li style="margin-bottom:{list_margin};">If you are not satisfied with the proposed resolution, you may appeal to an agency Director {manager_info['director_info']}, in which case they would review the case and get back to you in writing within 21 days of receipt of the appeal.</li>
        </ol>
        '''
    
    # ===== MICHIGAN BRANCHES (shmihomecare) =====
    elif branch in ['shmihomecare', 'shmihomecare_staging']:
        html += f'''
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Patients’ Rights and Responsibilities</u></b></p>
        <p style="font-size:{base_font_size};text-align:left;margin:{section_margin} 0;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE FOLLOWING RIGHTS AND RESPONSIBILITIES:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Right to accept or refuse services.</li>
            <li style="margin-bottom:{list_margin};">Right to be fully informed of the charges of the services.</li>
            <li style="margin-bottom:{list_margin};">Right to be fully informed of the name, business telephone number and business address of the person supervising the service and how to contact that person.</li>
            <li style="margin-bottom:{list_margin};">Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time.</li>
            <li style="margin-bottom:{list_margin};">Right of confidentiality of patient records.</li>
            <li style="margin-bottom:{list_margin};">Right to have your property and residence treated with respect.</li>
            <li style="margin-bottom:{list_margin};">Responsibility to advise the provider of any changes in your condition or any events that affect your service needs.</li>
            <li style="margin-bottom:{list_margin};">Responsibility to treat the OPTIONS’ caregivers with respect.</li>
            <li style="margin-bottom:{list_margin};">For further assistance, you may call and speak with an OPTIONS manager at 586.344.8436.</li>
        </ol>
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Complaint Procedures</u></b></p>
        <p style="font-size:{base_font_size};text-align:left;margin:{section_margin} 0;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Director. Their office number is 586.344.8436.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
            <li style="margin-bottom:{list_margin};">The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Director.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS will produce a written record of the findings of each complaint investigated.</li>
            <li style="margin-bottom:{list_margin};">The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Director.</li>
            <li style="margin-bottom:{list_margin};">The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient’s property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
            <li style="margin-bottom:{list_margin};">The Community Relations Director is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
            <li style="margin-bottom:{list_margin};">If you are not satisfied with the proposed resolution, you may appeal to an agency Director in writing to 13854 Lakeside Circle, Suite 250, Sterling Heights, MI 48313, in which case they would review the case and get back to you in writing within 21 days of receipt of the appeal.</li>
        </ol>
        '''
    
    # ===== VIRGINIA BRANCHES (excluding wfvahomecare and cfairfaxhomecare which have their own section) =====
    elif branch in ['nvahomecare', 'nvahomecare_staging', 'nvahomecarearchive', 'nvahomecarearchive_staging',
                    'rihomecare', 'rihomecare_staging', 'mnhomecare', 'mnhomecare_staging',
                    'lovahomecare', 'lovahomecare_staging', 'sfvahomecare', 'sfvahomecare_staging',
                    'amfvahomecare', 'amfvahomecare_staging']:
        
        admin_info = get_admin_info(branch)
        html += f'''
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Patients’ Rights and Responsibilities</u></b></p>
        <p style="font-size:{base_font_size};text-align:center;margin:{section_margin} 0;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE RIGHT TO BE:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Treated with courtesy, consideration and respect and is assured of the right of privacy.</li>
            <li style="margin-bottom:{list_margin};">Assured confidential treatment of medical and financial records as provided by law.</li>
            <li style="margin-bottom:{list_margin};">Free from mental and physical abuse, neglect, and property exploitation.</li>
            <li style="margin-bottom:{list_margin};">Assured the right to participate in the planning of the client\'s home care, including the right to refuse services.</li>
            <li style="margin-bottom:{list_margin};">Served by individuals who are properly trained and competent to perform their duties.</li>
            <li style="margin-bottom:{list_margin};">Assured the right to voice grievances and complaints related to the organizational services without fear of reprisal.</li>
            <li style="margin-bottom:{list_margin};">Advised, before care is initiated, of the extent to which payment for the home care organization services may be expected from federal or state programs, and the extent to which payment may be required from the client.</li>
            <li style="margin-bottom:{list_margin};">Advised orally and in writing of any changes in fees for services that are the client\'s responsibility. The home care organization shall advise the client of these changes as soon as possible, but no later than 30 calendar days from the date the home care organization became aware of the changes.</li>
            <li style="margin-bottom:{list_margin};">Provided with advance directive information prior to start of services.</li>
            <li style="margin-bottom:{list_margin};">Given at least five days written notice when the organization determines to terminate services.</li>
        </ol>
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Complaint Procedures</u></b></p>
        <p style="font-size:{base_font_size};text-align:left;margin:{section_margin} 0;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Administrator or the Administrator Alternate. Their office number is {admin_info['phone']}.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
            <li style="margin-bottom:{list_margin};">The OPTIONS employee who will be responsible for investigating complaints is the Administrator or the Administrator Alternate.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS will produce a written record of the findings of each complaint investigated.</li>
            <li style="margin-bottom:{list_margin};">The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Administrator or Administrator Alternate.</li>
            <li style="margin-bottom:{list_margin};">The local social service department of Adult Protective Services will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient’s property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
            <li style="margin-bottom:{list_margin};">The Administrator or Administrator Alternate is the agency employee who will, within 30 days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
            <li style="margin-bottom:{list_margin};">If you are not satisfied with the proposed resolution, you may appeal to {admin_info['name']}, {admin_info['title']}, at {admin_info['phone']}, or in writing to OPTIONS, {admin_info['address']}, in which case they would review the case and get back to you in writing within 21 days of receipt of the appeal. You may also contact the Office of the State Long Term Care Ombudsman at 8004 Franklin Farms Drive, Richmond, VA 23229, Tel. (800) 522-3402 or the Office of Licensure and Certification of the Virginia Dept. of Health at 9960 Mayland Drive, Suite 401, Henrico, VA 23233-1485, Tel. (800) 828-1120 and Fax (804) 527-4502.</li>
        </ol>
        '''
    
    # ===== WFVA/CFAIRFAX VIRGINIA BRANCHES =====
    elif branch in ['wfvahomecare', 'wfvahomecare_staging', 'cfairfaxhomecare', 'cfairfaxhomecare_staging']:
        html += f'''
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Patients’ Rights and Responsibilities</u></b></p>
        <p style="font-size:{base_font_size};text-align:left;margin:{section_margin} 0;padding-left:10px;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE RIGHT TO BE:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Treated with courtesy, consideration and respect and is assured of the right of privacy.</li>
            <li style="margin-bottom:{list_margin};">Assured confidential treatment of medical and financial records as provided by law.</li>
            <li style="margin-bottom:{list_margin};">Free from mental and physical abuse, neglect, and property exploitation.</li>
            <li style="margin-bottom:{list_margin};">Assured the right to participate in the planning of the client\'s home care, including the right to refuse services.</li>
            <li style="margin-bottom:{list_margin};">Served by individuals who are properly trained and competent to perform their duties.</li>
            <li style="margin-bottom:{list_margin};">Assured the right to voice grievances and complaints related to the organizational services without fear of reprisal.</li>
            <li style="margin-bottom:{list_margin};">Advised, before care is initiated, of the extent to which payment for the home care organization services may be expected from federal or state programs, and the extent to which payment may be required from the client.</li>
            <li style="margin-bottom:{list_margin};">Advised orally and in writing of any changes in fees for services that are the client\'s responsibility. The home care organization shall advise the client of these changes as soon as possible, but no later than 30 calendar days from the date the home care organization became aware of the changes.</li>
            <li style="margin-bottom:{list_margin};">Provided with advance directive information prior to start of services.</li>
            <li style="margin-bottom:{list_margin};">Given at least five days written notice when the organization determines to terminate services.</li>
        </ol>
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Complaint Procedures</u></b></p>
        <p style="font-size:{base_font_size};text-align:left;margin:{section_margin} 0;padding-left:10px;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Administrator and the Administrator Alternate. Their office number is 571.999.5464.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
            <li style="margin-bottom:{list_margin};">The OPTIONS employee who will be responsible for investigating complaints is the Administrator or the Administrator Alternate.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS will produce a written record of the findings of each complaint investigated.</li>
            <li style="margin-bottom:{list_margin};">The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Administrator or Administrator Alternate.</li>
            <li style="margin-bottom:{list_margin};">The local social service department of Adult Protective Services will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient’s property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
            <li style="margin-bottom:{list_margin};">The Administrator or Administrator Alternate is the agency employee who will, within 30 days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
            <li style="margin-bottom:{list_margin};">If you are not satisfied with the proposed resolution, you may appeal to Danny Mezher, the Administrator, at (703) 622-7132, or in writing to OPTIONS, 13800 Coppermine Road, Suite 104-B, Herndon, VA 20171, in which case he would review the case and get back to you in writing within 21 days of receipt of the appeal. You may also contact the Office of the State Long Term Care Ombudsman at 8004 Franklin Farms Drive, Richmond, VA 23229, Tel. (800) 522-3402 or the Office of Licensure and Certification of the Virginia Dept. of Health at 9960 Mayland Drive, Suite 401, Henrico, VA 23233-1485, Tel. (800) 828-1120 and Fax (804) 527-4502.</li>
        </ol>
        '''
    
    # ===== FLORIDA BRANCHES =====
    elif branch in ['tahomecare', 'tahomecare_staging', 'woflhomecare', 'woflhomecare_staging', 
                    'lzflhomecare', 'lzflhomecare_staging', 'wpbflhomecare', 'wpbflhomecare_staging']:
        html += f'''
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>NOTICE OF RIGHTS AND RESPONSIBILITIES</u></b></p>
        <p style="font-size:{base_font_size};text-align:center;margin:{section_margin} 0;"><b>You are a valued customer, and you have the following rights and responsibilities</b></p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">The patient, responsible party, or guardian have the right to be informed of the medical plan of treatment and/or plan of care, to participate in the development of the medical plan of treatment and/or plan of care and to have a copy of the medical plan of treatment and/or plan of care if requested. Our Registered Nurses are available to make initial assessments and develop a plan of care, as well as visits to patient’s home per patient, responsible party, or guardian’s request at an additional cost of $95.00/visit.</li>
            <li style="margin-bottom:{list_margin};">Right to accept or refuse services.</li>
            <li style="margin-bottom:{list_margin};">Right to be fully informed of the charges of services.</li>
            <li style="margin-bottom:{list_margin};">Right to be informed of the name, business telephone number and business address of the person supervising the services and how to contact that person.</li>
            <li style="margin-bottom:{list_margin};">Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time. The complaint procedure provided shall include the business address and telephone number of the person designated by the provider to handle complaints and questions.</li>
            <li style="margin-bottom:{list_margin};">Right of confidentiality of client records.</li>
            <li style="margin-bottom:{list_margin};">Right to have property and residence treated with respect.</li>
            <li style="margin-bottom:{list_margin};">Responsibility to advise the provider of any changes in the care recipient’s condition of any events that affect the care recipient’s service needs.</li>
            <li style="margin-bottom:{list_margin};">To report a complaint regarding the services you receive, please call toll free 1-888-419-3456.</li>
            <li style="margin-bottom:{list_margin};">To report abuse, neglect, or exploitation, please call toll free 1-800-962-2873.</li>
        </ol>
        '''
    
    # ===== NORTH CAROLINA BRANCHES - GBHOMECARE =====
    elif branch in ['gbhomecare', 'gbhomecare_staging']:
        complaint_phone = "336.270.6647"
        html += f'''
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Patients’ Rights Responsibilities</u></b></p>
        <p style="font-size:{base_font_size};text-align:left;margin:{section_margin} 0;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE FOLLOWING RIGHTS AND RESPONSIBILITIES:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Right to participate in the planning of the client\'s home care, including the right to accept or refuse services.</li>
            <li style="margin-bottom:{list_margin};">Right to be fully informed of the charges of the services.</li>
            <li style="margin-bottom:{list_margin};">Right to be fully informed of the name, business telephone number and business address of the person supervising the service and how to contact that person.</li>
            <li style="margin-bottom:{list_margin};">Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time.</li>
            <li style="margin-bottom:{list_margin};">Right of confidentiality of patient records.</li>
            <li style="margin-bottom:{list_margin};">Right to have your property and residence treated with respect.</li>
            <li style="margin-bottom:{list_margin};">Right of nondiscrimination in obtaining services from Options because of race, color, religion, creed, national origin, ancestry, disability, sex, or age.</li>
            <li style="margin-bottom:{list_margin};">Responsibility to advise the provider of any changes in your condition or any events that affect your service needs.</li>
            <li style="margin-bottom:{list_margin};">Responsibility to treat the OPTIONS\' caregivers with respect.</li>
        </ol>
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Complaints Procedures</u></b></p>
        <p style="font-size:{base_font_size};text-align:left;margin:{section_margin} 0;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their telephone number is {complaint_phone}.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
            <li style="margin-bottom:{list_margin};">The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS will produce a written record of the findings of each complaint investigated.</li>
            <li style="margin-bottom:{list_margin};">The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Manager.</li>
            <li style="margin-bottom:{list_margin};">The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient’s property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
            <li style="margin-bottom:{list_margin};">The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
            <li style="margin-bottom:{list_margin};">You may also contact the North Carolina Division of Health Service Regulation, complaints hotline, at 800.624.3004.</li>
        </ol>
        '''
    
    # ===== NORTH CAROLINA BRANCHES - RDHOMECARE =====
    elif branch in ['rdhomecare', 'rdhomecare_staging']:
        html += f'''
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Patients’ Rights and Responsibilities</u></b></p>
        <p style="font-size:{base_font_size};text-align:left;margin:{section_margin} 0;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE FOLLOWING RIGHTS AND RESPONSIBILITIES:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Right to participate in the planning of the client\'s home care, including the right to accept or refuse services.</li>
            <li style="margin-bottom:{list_margin};">Right to be fully informed of the charges of the services.</li>
            <li style="margin-bottom:{list_margin};">Right to be fully informed of the name, business telephone number and business address of the person supervising the service and how to contact that person.</li>
            <li style="margin-bottom:{list_margin};">Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time.</li>
            <li style="margin-bottom:{list_margin};">Right of confidentiality of patient records.</li>
            <li style="margin-bottom:{list_margin};">Right to have your property and residence treated with respect.</li>
            <li style="margin-bottom:{list_margin};">Right of nondiscrimination in obtaining services from Options because of race, color, religion, creed, national origin, ancestry, disability, sex, or age.</li>
            <li style="margin-bottom:{list_margin};">Responsibility to advise the provider of any changes in your condition or any events that affect your service needs.</li>
            <li style="margin-bottom:{list_margin};">Responsibility to treat the OPTIONS\' caregivers with respect.</li>
        </ol>
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Complaint Procedures</u></b></p>
        <p style="font-size:{base_font_size};text-align:left;margin:{section_margin} 0;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their telephone number is 919.380.6812.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
            <li style="margin-bottom:{list_margin};">The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS will produce a written record of the findings of each complaint investigated.</li>
            <li style="margin-bottom:{list_margin};">The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Director.</li>
            <li style="margin-bottom:{list_margin};">The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient’s property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
            <li style="margin-bottom:{list_margin};">The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
            <li style="margin-bottom:{list_margin};">You may also contact the North Carolina Division of Health Service Regulation, complaints hotline, at 800.624.3004.</li>
        </ol>
        '''
    
    # ===== PENNSYLVANIA BRANCHES (hbhomecare, nspahomecare) =====
    elif branch in ['hbhomecare', 'hbhomecare_staging', 'nspahomecare', 'nspahomecare_staging']:
        
        if branch in ['hbhomecare', 'hbhomecare_staging']:
            complaint_phone = "717-510-8613"
            address = "6 Montgomery Village Avenue, Suite 330, Gaithersburg, MD 20879"
        else:  # nspahomecare
            complaint_phone = "610.975.4422"
            address = "175 Strafford Avenue, Suite One Wayne, PA 19087"
        
        html += f'''
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Patients’ Rights and Responsibilities</u></b></p>
        <p style="font-size:{base_font_size};text-align:left;margin:{section_margin} 0;padding-left:10px;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE FOLLOWING RIGHTS AND RESPONSIBILITIES:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Right to participate in the planning of the client\'s home care, including the right to accept or refuse services.</li>
            <li style="margin-bottom:{list_margin};">Right to be fully informed of the charges of the services.</li>
            <li style="margin-bottom:{list_margin};">Right to be fully informed of the name, business telephone number and business address of the person supervising the service and how to contact that person.</li>
            <li style="margin-bottom:{list_margin};">Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time.</li>
            <li style="margin-bottom:{list_margin};">Right of confidentiality of patient records.</li>
            <li style="margin-bottom:{list_margin};">Right to have your property and residence treated with respect.</li>
            <li style="margin-bottom:{list_margin};">Right of nondiscrimination in obtaining services from Options because of race, color, religion, creed, national origin, ancestry, disability, sex, or age.</li>
            <li style="margin-bottom:{list_margin};">Responsibility to advise the provider of any changes in your condition or any events that affect your service needs.</li>
            <li style="margin-bottom:{list_margin};">Responsibility to treat the OPTIONS\' caregivers with respect.</li>
        </ol>
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Complaint Procedures</u></b></p>
        <p style="font-size:{base_font_size};text-align:left;margin:{section_margin} 0;padding-left:10px;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their telephone number is {complaint_phone}.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
            <li style="margin-bottom:{list_margin};">The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS will produce a written record of the findings of each complaint investigated.</li>
            <li style="margin-bottom:{list_margin};">The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Manager.</li>
            <li style="margin-bottom:{list_margin};">The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient’s property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
            <li style="margin-bottom:{list_margin};">The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
            <li style="margin-bottom:{list_margin};">If you are not satisfied with the proposed resolution, you may appeal to Options Corporate office at 1-800-2-OPTIONS, or in writing to OPTIONS, {address}, in which case your complaint would be reviewed and Options will get back to you in writing within 21 days of receipt of the appeal. You may also contact the Pennsylvania Department of Health\'s complaint hotline at 1-800-254-5164 and/or the Ombudsman Program at 717-780-6130 which is located at the Dauphin County Area Agency on Aging (AAA) office.</li>
        </ol>
        '''
    
    # ===== INDIANA BRANCHES (lkinhomecare) =====
    elif branch in ['lkinhomecare', 'lkinhomecare_staging']:
        html += f'''
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Client\'s Rights and Responsibilities</u></b></p>
        <p style="font-size:{base_font_size};text-align:left;margin:{section_margin} 0;padding-left:10px;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE RIGHT TO:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Have your property treated with respect.</li>
            <li style="margin-bottom:{list_margin};">Temporarily suspend, permanently terminate, temporarily add, or permanently add services in the service plan.</li>
            <li style="margin-bottom:{list_margin};">File grievances regarding services furnished or regarding the lack of respect for property by the personal services agency, and is not subject to discrimination or reprisal for filing a grievance.</li>
            <li style="margin-bottom:{list_margin};">Be free from verbal, physical, and psychological abuse and to be treated with dignity. Furthermore, as part of the client rights and responsibilities, it is understood that:</li>
            <li style="margin-bottom:{list_margin};">It is not within the scope of the personal services agency\'s license to manage the medical and health conditions of the client if a condition becomes unstable or unpredictable.</li>
            <li style="margin-bottom:{list_margin};">The client is made aware of charges for services provided by the personal services agency.</li>
            <li style="margin-bottom:{list_margin};">The personal services agency\'s policy for notifying the client of any increase in the cost of services is included below, under "Notice of Billing Procedures".</li>
            <li style="margin-bottom:{list_margin};">The hours the personal services agency\'s office is open for business are made known to the client.</li>
            <li style="margin-bottom:{list_margin};">Upon request by the client, the personal service agency will make available to the client a written list of the names and addresses of all persons having at least a five percent (5%) ownership or controlling interest in the personal services agency.</li>
            <li style="margin-bottom:{list_margin};">The procedures for contacting the personal services agency\'s manager, or the manager\'s designee, while the personal services agency\'s office is open or closed, are made known to the client.</li>
            <li style="margin-bottom:{list_margin};">The procedure and telephone number to call to file a complaint with the personal services agency are indicated below under "Notice of Complaint Procedures".</li>
            <li style="margin-bottom:{list_margin};">That the state department does not inspect personal services agencies as a part of the licensing process but does investigate complaints concerning personal services agencies.</li>
            <li style="margin-bottom:{list_margin};">The procedure and telephone number to call to file a complaint with the state department along with the business hours of the state department are included below in the "Notice of Complaint Procedures" section.</li>
        </ol>
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Complaint Procedures</u></b></p>
        <p style="font-size:{base_font_size};text-align:left;margin:{section_margin} 0;padding-left:10px;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
        <ol type="1" style="padding-left: {list_padding};margin:0">
            <li style="margin-bottom:{list_margin};">Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Office Manager or the Franchise Owner. Their office number is 219.321.9130.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
            <li style="margin-bottom:{list_margin};">The OPTIONS employee who will be responsible for investigating complaints is the Franchise Owner or the Office Manager.</li>
            <li style="margin-bottom:{list_margin};">OPTIONS will produce a written record of the findings of each complaint investigated.</li>
            <li style="margin-bottom:{list_margin};">The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Franchise Owner or the Office Manager.</li>
            <li style="margin-bottom:{list_margin};">The local social service department Adult Protective Services unit will be informed if, at any stage of investigating or resolving a complaint, the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient’s property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
            <li style="margin-bottom:{list_margin};">The Franchise Owner or the Office Manager is the agency employee who will, within 5 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
            <li style="margin-bottom:{list_margin};">If you are not satisfied with the proposed resolution, you may appeal to an agency Director at 219.321.9130, or in writing to OPTIONS Director, 8488 Georgia Street, Suite D, Merrillville, IN 46410, in which case they would review the case and get back to you in writing within 5 business days of receipt of the appeal. You may also contact the Consumer Protection Division Complaint Hotline at 1-800-382-5516, the Indiana Department of Aging at 1-888-673-0002, or the Indiana State Department for Health at 317-233-1325 between 8:15AM and 4:45PM Monday through Friday.</li>
        </ol>
        '''
    
    # ===== DC BRANCHES with STATE-SPECIFIC LOGIC =====
    elif branch in ['dchomecare', 'dchomecare_staging']:
        if care_state == "DC":
            html += f'''
            <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Patients’ Rights and Responsibilities</u></b></p>
            <p style="font-size:{base_font_size};margin:{section_margin} 0;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE FOLLOWING RIGHTS AND RESPONSIBILITIES:</p>
            <ol type="1" style="padding-left: {list_padding};margin:0">
                <li style="margin-bottom:{list_margin};">Right to accept or refuse services.</li>
                <li style="margin-bottom:{list_margin};">Right to be fully informed of the charges of the services.</li>
                <li style="margin-bottom:{list_margin};">Right to be fully informed of the name, business telephone number and business address of the person supervising the service and how to contact that person.</li>
                <li style="margin-bottom:{list_margin};">Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time.</li>
                <li style="margin-bottom:{list_margin};">Right of confidentiality of patient records.</li>
                <li style="margin-bottom:{list_margin};">Right to have your property and residence treated with respect.</li>
                <li style="margin-bottom:{list_margin};">Responsibility to advise the provider of any changes in your condition or any events that affect your service needs.</li>
                <li style="margin-bottom:{list_margin};">Responsibility to treat the OPTIONS’ caregivers with respect.</li>
                <li style="margin-bottom:{list_margin};">For further assistance, you may call and speak with an OPTIONS manager at 301.562.1100 or 800.267.8466</li>                
            </ol>
            <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Complaint Procedures</u></b></p>
            <p style="font-size:{base_font_size};margin:{section_margin} 0;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
            <ol type="1" style="padding-left: {list_padding};margin:0">
                <li style="margin-bottom:{list_margin};">Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their office number is 202.581.2000 for the District of Columbia, 301.562.3100 for Montgomery Co., MD and P.G. County, MD</li>
                <li style="margin-bottom:{list_margin};">OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
                <li style="margin-bottom:{list_margin};">The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager or the Care Manager.</li>
                <li style="margin-bottom:{list_margin};">OPTIONS will produce a written record of the findings of each complaint investigated.</li>
                <li style="margin-bottom:{list_margin};">The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Manager.</li>
                <li style="margin-bottom:{list_margin};">The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient’s property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
                <li style="margin-bottom:{list_margin};">The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
                <li style="margin-bottom:{list_margin};">If you are not satisfied with the proposed resolution, you may appeal to an agency Director at 1-800-2-OPTIONS, or in writing to OPTIONS Director, 6 Montgomery Village Avenue, Suite 330, Gaithersburg, MD 20879, in which case they would review the case and get back to you in writing within 21 days of receipt of the appeal.</li>
            </ol>
            '''
        else:
            top_margin = "0px"
            html += f'''
            <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Patients’ Rights and Responsibilities</u></b></p>
            <ol class="main-list" style="padding-left: {list_padding}; margin:0; list-style-type: decimal;">
                <li style="margin-bottom: {list_margin};">A client, or the client representative with legal authority to make health care decisions, has the right to:
                    <ol class="alpha-list" style="padding-left: 14px; margin:0; list-style-type: lower-alpha;">
                        <li style="margin-bottom:{list_margin};">Be treated with consideration, respect, and full recognition of the client’s human dignity and individuality</li>
                        <li style="margin-bottom:{list_margin};">Receive treatment, care, and services that are adequate, appropriate, and in compliance with relevant State, local, and federal laws and regulations</li>
                        <li style="margin-bottom:{list_margin};">Participate in the development of the client’s care plan and medical treatment</li>
                        <li style="margin-bottom:{list_margin};">Refuse treatment after the possible consequences of refusing treatment have been fully explained</li>
                        <li style="margin-bottom:{list_margin};">Privacy</li>
                        <li style="margin-bottom:{list_margin};">Be free from mental, verbal, sexual, and physical abuse, neglect, involuntary seclusion, and exploitation</li>
                        <li style="margin-bottom:{list_margin};">Confidentiality</li>
                    </ol>
                </li>
                <li style="margin-bottom: {list_margin};">A client or client representative has the right to:
                    <ol class="alpha-list" style="padding-left: 14px; margin:0; list-style-type: lower-alpha;">
                        <li style="margin-bottom:{list_margin};">Make suggestions or complaints, or present grievances on behalf of the client to the agency, government agencies, or other persons without the threat or fear of retaliation</li>
                        <li style="margin-bottom:{list_margin};">Receive a prompt response, through an established complaint or grievance procedure, to any complaints, suggestions, or grievances the participant may have</li>
                        <li style="margin-bottom:{list_margin};">Have access to the procedures for making a complaint to the Office of Health Care Quality - see (3) below, and to:
                            <ol class="roman-list" style="padding-left: 14px; margin:0; list-style-type: lower-roman;">
                                <li style="margin-bottom:{list_margin};">The Adult Protective Services Program of the local department of social services, if the client is an adult; or</li>
                                <li style="margin-bottom:{list_margin};">The Child Protective Services Program of the local department of social services, if the client is a minor</li>
                            </ol>
                        </li>
                    </ol>
                </li>
                <li style="margin-bottom: {list_margin};">A client or client representative has the responsibility to:
                    <ol class="alpha-list" style="padding-left: 14px; margin:0; list-style-type: lower-alpha;">
                        <li style="margin-bottom:{list_margin};">Advise the Options office of any changes in the care recipient’s condition, or of any events that affect the care recipient’s service needs.</li>
                        <li style="margin-bottom:{list_margin};">Treat the Options caregivers with respect.</li>
                        <li style="margin-bottom:{list_margin};">Pay Options invoices in a timely manner as indicated below under the “Notice of Billing Procedures” section.</li>
                    </ol>
                </li>
            </ol>

            <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;margin-top:{top_margin};"><b><u>Notice of Complaint Procedures</u></b></p>
            <ol class="main-list" style="padding-left: {list_padding}; margin:0; list-style-type: decimal;">
                <li style="margin-bottom:{list_margin};">Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their office number is 410.224.2700 for Annapolis, 410.448.1100 for Baltimore, 410.893.9914 for Bel Air, 301.562.3100 for Bethesda, 301.624.5630 for Frederick, and 301.392.1387 for La Plata</li>
                <li style="margin-bottom:{list_margin};">OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
                <li style="margin-bottom:{list_margin};">The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager or the Care Manager.</li>
                <li style="margin-bottom:{list_margin};">OPTIONS will produce a written record of the findings of each complaint investigated.</li>
                <li style="margin-bottom:{list_margin};">The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Manager.</li>
                <li style="margin-bottom:{list_margin};">The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient’s property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
                <li style="margin-bottom:{list_margin};">The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
                <li style="margin-bottom:{list_margin};">If you are not satisfied with the proposed resolution, you may appeal to an agency Director at 1-800-2-OPTIONS, or in writing to OPTIONS Director, 555 Quince Orchard Road, Suite 240, Gaithersburg, MD 20878, in which case they would review the case and get back to you in writing within 21 days of receipt of the appeal. You may also write to Barbara Fagan, Survey Coordinator, Office of Health Care Quality, Bland Bryant Building, Spring Grove Hospital Center, 55 Wade Avenue, Catonsville, MD 21228, or you may call the State of Maryland’s Residential Service Agency Hotline at 1-877-4MD-DHMH.</li>
            </ol>
            '''
    
    # ===== DEFAULT to MD/NJ template if no match (shouldn't happen) =====
    else:
        html += f'''
        <p style="font-size:{title_font_size};text-align:center;margin:{section_margin} 0;"><b><u>Notice of Patients’ Rights and Responsibilities</u></b></p>
        <p style="font-size:{base_font_size};text-align:left;margin:{section_margin} 0;">Default template - please contact administrator.</p>
        '''
    
    # ===== NOTICE OF BILLING PROCEDURES (for ALL branches) =====
    html += f'''
    <p style="font-size:{title_font_size};text-align:center;margin:{billing_margin} 0;"><b><u>Notice of Billing Procedures</u></b></p>
    <p style="font-size:{base_font_size};margin:{billing_margin} 0;">BILLING, BILLING ERRORS AND REFUNDS ARE TREATED AS FOLLOWS:</p>
    <ol type="1" style="padding-left: 10px;margin:{billing_margin} 0;">
        <li style="margin-bottom:{list_margin};"><u>Billing Method:</u> &nbsp;OPTIONS is a long-term home care agency, and billing is done, by way of invoices, on a weekly or bi-weekly basis. Given that billing is typically done after services are provided, invoices are due upon receipt.</li>
        <li style="margin-bottom:{list_margin};"><u>When Payers are Insurance Companies or Third Parties:</u> &nbsp;OPTIONS typically seeks to obtain an "Assignment of Benefits" form from the care recipient or their designees, and OPTIONS then invoices the third party, copying the care recipient or their designees with all invoices sent to the third party.</li>
        <li style="margin-bottom:{list_margin};"><u>Patient Notification of Changes in Fees and Charges:</u> &nbsp;We endeavor to notify the care recipient or their designees in writing of any changes in fees or charges, at least two (2) weeks ahead of the effective date of the new changes. Rate increases typically occur following each 12 months of service.</li>
        <li style="margin-bottom:{list_margin};"><u>Correction of Billing Errors and Refund Policy:</u> &nbsp;Billing errors will be corrected in subsequent invoices. All refunds are either credited to the care recipient\'s account if it is an ongoing case, or are paid back to the care recipient.</li>
        <li style="margin-bottom:{list_margin};"><u>Collection of Delinquent Care Recipient Accounts:</u> &nbsp;Any account more than 30 days past due shall be subject to interest charges of 1 ½ % per month (18% annual) from the invoice due date. If it becomes necessary to refer your account to an attorney for collection, you will be responsible for court costs and attorney\'s fees of no less than 1/3 (33.33%) of the principal balance, in addition to the interest charges listed above.</li>
    </ol>
    '''
    
    # ===== FLEXIBLE SPACER for short/medium content =====
    if use_flex_spacer:
        html += '<div style="flex: 1;"></div>'
    
    # Close the inner div
    html += '</div>'
    
    # ===== SIGNATURE SECTION =====
    html += f'<div style="page-break-inside: avoid; margin-top: {signature_margin};">'
    
    if branch in ['athomecare', 'athomecare_staging', 'scgahomecare', 'scgahomecare_staging']:
        html += get_signature_3col_page2(clt_first, clt_last, clt_relationship, handled_by, current_date, base_font_size)
    else:
        html += get_signature_2col_page2(clt_first, clt_last, clt_relationship, current_date, base_font_size)
    
    html += '</div>'
    html += '</div>'
    return html

def get_manager_info(branch):
    """Get manager contact info for Cleveland/DC/other branches"""
    info = {
        'manager_phone': '301.562.1100 or 800.267.8466',
        'complaint_phone': '301.562.3100',
        'director_info': 'at 1-800-2-OPTIONS'
    }
    
    if branch in ['clhomecare', 'clhomecare_staging']:
        info['complaint_phone'] = '301.562.3100 for the District of Columbia, 216.861.3700 for the Cleveland area'
        info['director_info'] = 'at 1-800-2-OPTIONS, or in writing to OPTIONS Director, 555 Quince Orchard Road, Suite 240, Gaithersburg, MD 20878'
    elif branch in ['blmdhomecare', 'blmdhomecare_staging']:
        info['manager_phone'] = '667.415.8317'
        info['complaint_phone'] = '667.415.8317'
        info['director_info'] = 'at 1-800-2-OPTIONS, or in writing to OPTIONS Director, 4690 Millennium Drive, Belcamp MD 21017'
    elif branch in ['ciohhomecare', 'ciohhomecare_staging']:
        info['manager_phone'] = '513.928.0042'
        info['complaint_phone'] = '513.928.0042'
        info['director_info'] = 'at 1-800-2-OPTIONS, or in writing to OPTIONS Director, 555 Quince Orchard Road, Suite 240, Gaithersburg, MD 20878'
    elif branch in ['chazhomecare', 'chazhomecare_staging']:
        info['manager_phone'] = '480.673.3888'
        info['complaint_phone'] = '480.673.3888'
        info['director_info'] = 'at 480.673.3888, or in writing to OPTIONS Director, 920 W. Chandler Blvd, Suite 3, Chandler, AZ 85225'
    
    return info

def get_admin_info(branch):
    """Get administrator info for Virginia branches"""
    info = {}
    
    if branch in ['nvahomecare', 'nvahomecare_staging', 'nvahomecarearchive', 'nvahomecarearchive_staging']:
        info = {
            'phone': '(703) 442-9700',
            'name': 'Ramzi Rihani',
            'title': 'the Administrator',
            'address': '6 Montgomery Village Avenue, Suite 330, Gaithersburg, MD 20879'
        }
    elif branch in ['rihomecare', 'rihomecare_staging']:
        info = {
            'phone': '(804) 673-6730',
            'name': 'Ramzi Rihani',
            'title': 'the Administrator',
            'address': '6 Montgomery Village Avenue, Suite 330, Gaithersburg, MD 20879'
        }
    elif branch in ['mnhomecare', 'mnhomecare_staging']:
        info = {
            'phone': '(571) 449-6781',
            'name': 'Michele Mezher',
            'title': 'the Administrator',
            'address': '10432 Balls Ford Road, Suite 300, Manassas, VA 20109'
        }
    elif branch in ['lovahomecare', 'lovahomecare_staging']:
        info = {
            'phone': '571.999.5464',
            'name': 'Danny Mezher',
            'title': 'the Administrator',
            'address': '13800 Coppermine Road, Suite 125-A, Herndon, VA 20171'
        }
    elif branch in ['sfvahomecare', 'sfvahomecare_staging']:
        info = {
            'phone': '(571) 416-8260',
            'name': 'Liza Sagudan',
            'title': 'the Administrator',
            'address': '7830 Backlick Road, Suite 200-A, Springfield, VA 22150'
        }
    elif branch in ['amfvahomecare', 'amfvahomecare_staging']:
        info = {
            'phone': '571.449.6781',
            'name': 'Viral Patel',
            'title': 'the Administrator',
            'address': '11350 Random Hills Rd, Suite 800, Fairfax, VA 22030'
        }
    elif branch in ['wfvahomecare', 'wfvahomecare_staging', 'cfairfaxhomecare', 'cfairfaxhomecare_staging']:
        # These are handled in their own section, but provide defaults
        info = {
            'phone': '(703) 622-7132',
            'name': 'Danny Mezher',
            'title': 'the Administrator',
            'address': '13800 Coppermine Road, Suite 104-B, Herndon, VA 20171'
        }
    else:
        info = {
            'phone': '(703) 442-9700',
            'name': 'Ramzi Rihani',
            'title': 'the Administrator',
            'address': '6 Montgomery Village Avenue, Suite 330, Gaithersburg, MD 20879'
        }
    
    return info

def get_signature_3col_page2(clt_first, clt_last, clt_relationship, handled_by, current_date, font_size="7px"):
    """3-column signature for GA/SC branches on page 2 - BALANCED SPACING"""
    return f'''
    <table width="100%" style="font-size:{font_size};margin-top:5px; border-collapse: collapse;" cellpadding="3" cellspacing="0">
        <tr>
            <td width="33%" align="center" style="padding:3px;">
                <p style="margin:0 0 3px 0; text-align:center;"><b>{clt_first} {clt_last}</b></p>
                <div style="border-top:1.5px solid black; width:90%; margin:3px auto 3px auto;"></div>
                <p style="margin:3px 0 0 0; text-align:center;">Name of Responsible Party</p>
            </td>
            <td width="34%" align="center" style="padding:3px;">
                <p style="margin:0 0 3px 0; text-align:center;"><b>{clt_relationship}</b></p>
                <div style="border-top:1.5px solid black; width:90%; margin:3px auto 3px auto;"></div>
                <p style="margin:3px 0 0 0; text-align:center;">Relationship to Care Recipient</p>
            </td>
            <td width="33%" align="center" style="padding:3px;">
                <p style="margin:0 0 3px 0; text-align:center;"><b>{handled_by}</b></p>
                <div style="border-top:1.5px solid black; width:90%; margin:3px auto 3px auto;"></div>
                <p style="margin:3px 0 0 0; text-align:center;">Options Representative</p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding:8px 3px 3px 3px;">
                <div style="border-top:1px solid black; width:80%; margin:0 auto 5px auto;"></div>
                <p style="margin:3px 0 0 0;">Signature (SEAL)</p>
            </td>
            <td align="center" style="padding:8px 3px 3px 3px;">&nbsp;</td>
            <td align="center" style="padding:8px 3px 3px 3px;">
                <div style="border-top:1px solid black; width:80%; margin:0 auto 5px auto;"></div>
                <p style="margin:3px 0 0 0;">Signature</p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding:8px 3px 3px 3px;">
                <div style="border-top:1px solid black; width:80%; margin:0 auto 5px auto;"></div>
                <p style="margin:3px 0 0 0;">Date: {current_date}</p>
            </td>
            <td align="center" style="padding:8px 3px 3px 3px;">&nbsp;</td>
            <td align="center" style="padding:8px 3px 3px 3px;">
                <div style="border-top:1px solid black; width:80%; margin:0 auto 5px auto;"></div>
                <p style="margin:3px 0 0 0;">Date: {current_date}</p>
            </td>
        </tr>
    </table>
    '''

def get_signature_2col_page2(clt_first, clt_last, clt_relationship, current_date, font_size="7px"):
    """2-column signature for most branches on page 2 - BALANCED SPACING"""
    return f'''
    <table width="100%" style="font-size:{font_size};margin-top:8px; border-collapse: collapse;" cellpadding="4" cellspacing="0">
        <tr>
            <td align="center" width="50%" style="padding:4px;">
                <p style="margin:0 0 4px 0;"><b>{clt_first} {clt_last}</b></p>
                <div style="border-top:1.5px solid black; width:90%; margin:3px auto 4px auto;"></div>
                <p style="margin:4px 0 0 0;">Name of Responsible Party</p>
            </td>
            <td align="center" width="50%" style="padding:4px;">
                <p style="margin:0 0 4px 0;"><b>{clt_relationship}</b></p>
                <div style="border-top:1.5px solid black; width:90%; margin:3px auto 4px auto;"></div>
                <p style="margin:4px 0 0 0;">Relationship to Care Recipient</p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding:10px 4px 4px 4px;">
                <p style="margin:0 0 3px 0;">(SEAL)</p>
                <div style="border-top:1px solid black; width:75%; margin:3px auto 5px auto;"></div>
                <p style="margin:4px 0 0 0;">Signature</p>
            </td>
            <td align="center" style="padding:10px 4px 4px 4px;">
                <div style="border-top:1px solid black; width:75%; margin:0 auto 5px auto;"></div>
                <p style="margin:4px 0 0 0;">Date: {current_date}</p>
            </td>
        </tr>
    </table>
    '''