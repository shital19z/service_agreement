"""Page 2 - Patient Rights and Billing Procedures (matches dynamic_sa_page2.php)"""
from datetime import datetime

def generate_page2(data):
    """
    Generate Page 2 HTML - matches dynamic_sa_page2.php logic
    """
    # Get values directly from data
    branch = data.get('branch_code', '').lower()
    care_state = data.get('care_state', '').upper()
    
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
    
    html = '<div><div style="font-size:7px;margin-top:0;line-height:1.1;">'  # Reduced to 7px, removed top margin
    
    # MARYLAND & NEW JERSEY BRANCHES
    md_nj_branches = [
        'anhomecare', 'anhomecare_staging', 'bahomecare', 'bahomecare_staging', 
        'blhomecare', 'blhomecare_staging', 'fkhomecare', 'fkhomecare_staging', 
        'lphomecare', 'lphomecare_staging', 'testhomecare'
    ]
    
    if branch in md_nj_branches:
        top_margin = "0px"
        if branch in ['bahomecare', 'bahomecare_staging', 'lphomecare', 'lphomecare_staging']:
            top_margin = "0px"
        
        # Check if NJ branch
        is_nj = branch in ['wenjhomecare', 'wenjhomecare_staging']
        
        # Barbara Fagan / Maryland Hotline clause
        md_hotline = ""
        if not is_nj:
            md_hotline = '<li style="margin-bottom:0;">You may write to Barbara Fagan, Survey Coordinator, Office of Health Care Quality, Bland Bryant Building, Spring Grove Hospital Center, 55 Wade Avenue, Catonsville, MD 21228, or you may call the State of Maryland’s Residential Service Agency Hotline at 1-877-4MD-DHMH.</li>'
        
        # Phone numbers for Complaint Intake
        if is_nj:
            office_num = "973.803.0901"
        else:
            office_num = "410.224.2700 for Annapolis, 410.448.1100 for Baltimore, 410.893.9914 for Bel Air, 301.562.3100 for Bethesda, 301.624.5630 for Frederick, and 301.392.1387 for La Plata"
        
        html += f'''
        <p style="font-size:9px;text-align:center;margin:0;"><b><u>Notice of Patients’ Rights and Responsibilities</u></b></p>
        <ol class="main-list" style="padding-left: 16px; margin:0; list-style-type: decimal;">
            <li style="margin-bottom: 0;">A client, or the client representative with legal authority to make health care decisions, has the right to:
                <ol class="alpha-list" style="padding-left: 14px; margin:0; list-style-type: lower-alpha;">
                    <li style="margin-bottom:0;">Be treated with consideration, respect, and full recognition of the client’s human dignity and individuality</li>
                    <li style="margin-bottom:0;">Receive treatment, care, and services that are adequate, appropriate, and in compliance with relevant State, local, and federal laws and regulations</li>
                    <li style="margin-bottom:0;">Participate in the development of the client’s care plan and medical treatment</li>
                    <li style="margin-bottom:0;">Refuse treatment after the possible consequences of refusing treatment have been fully explained</li>
                    <li style="margin-bottom:0;">Privacy</li>
                    <li style="margin-bottom:0;">Be free from mental, verbal, sexual, and physical abuse, neglect, involuntary seclusion, and exploitation</li>
                    <li style="margin-bottom:0;">Confidentiality</li>
                </ol>
            </li>
            <li style="margin-bottom: 0;">A client or client representative has the right to:
                <ol class="alpha-list" style="padding-left: 14px; margin:0; list-style-type: lower-alpha;">
                    <li style="margin-bottom:0;">Make suggestions or complaints, or present grievances on behalf of the client to the agency, government agencies, or other persons without the threat or fear of retaliation</li>
                    <li style="margin-bottom:0;">Receive a prompt response, through an established complaint or grievance procedure, to any complaints, suggestions, or grievances the participant may have</li>
                    <li style="margin-bottom:0;">Have access to the procedures for making a complaint to the Office of Health Care Quality - see (3) below, and to:
                        <ol class="roman-list" style="padding-left: 14px; margin:0; list-style-type: lower-roman;">
                            <li style="margin-bottom:0;">The Adult Protective Services Program of the local department of social services, if the client is an adult; or</li>
                            <li style="margin-bottom:0;">The Child Protective Services Program of the local department of social services, if the client is a minor</li>
                        </ol>
                    </li>
                </ol>
            </li>
            {md_hotline}
            <li style="margin-bottom: 0;">A client or client representative has the responsibility to:
                <ol class="alpha-list" style="padding-left: 14px; margin:0; list-style-type: lower-alpha;">
                    <li style="margin-bottom:0;">Advise the Options office of any changes in the care recipient’s condition, or of any events that affect the care recipient’s service needs.</li>
                    <li style="margin-bottom:0;">Treat the Options caregivers with respect.</li>
                    <li style="margin-bottom:0;">Pay Options invoices in a timely manner as indicated below under the “Notice of Billing Procedures” section.</li>
                </ol>
            </li>
        </ol>

        <p style="font-size:9px;text-align:center;margin:0;margin-top:{top_margin};"><b><u>Notice of Complaint Procedures</u></b></p>
        <ol class="main-list" style="padding-left: 16px; margin:0; list-style-type: decimal;">
            <li style="margin-bottom:0;">Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their office number is {office_num}.</li>
            <li style="margin-bottom:0;">OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
            <li style="margin-bottom:0;">The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager or the Care Manager.</li>
            <li style="margin-bottom:0;">OPTIONS will produce a written record of the findings of each complaint investigated.</li>
            <li style="margin-bottom:0;">The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Manager.</li>
            <li style="margin-bottom:0;">The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient’s property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
            <li style="margin-bottom:0;">The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
'''
        if is_nj:
            html += '<li style="margin-bottom:0;">If you are not satisfied with the proposed resolution, you may appeal to an agency Director at 973.803.0901, or in writing to OPTIONS Director, 70 South Orange Avenue, Suite 105, Livingston, NJ 07039 in which case they would review the case and get back to you in writing within 21 days of receipt of the appeal. You may also write to he New Jersey Office of the Attorney General, Division of Consumer Affairs, Certified Homemaker-Home Health Aide Unit, 124 Halsey Street, 6th Floor, P.O. Box 47030, Newark, NJ 07101 - 973.504.6430.</li>'
        else:
            html += '<li style="margin-bottom:0;">If you are not satisfied with the proposed resolution, you may appeal to an agency Director at 1-800-2-OPTIONS, or in writing to OPTIONS Director, 555 Quince Orchard Road, Suite 240, Gaithersburg, MD 20878, in which case they would review the case and get back to you in writing within 21 days of receipt of the appeal.  You may also write to Barbara Fagan, Survey Coordinator, Office of Health Care Quality, Bland Bryant Building, Spring Grove Hospital Center, 55 Wade Avenue, Catonsville, MD 21228, or you may call the State of Maryland’s Residential Service Agency Hotline at 1-877-4MD-DHMH.</li>'
        
        html += '</ol>'
    
    # GEORGIA BRANCHES
    elif branch in ['athomecare', 'athomecare_staging', 'scgahomecare', 'scgahomecare_staging']:
        html += '''
        <p style="font-size:9px;text-align:center;margin:0;"><b><u>NOTICE OF RIGHTS AND RESPONSIBILITIES</u></b></p>
        <p style="font-size:7px;text-align:center;margin:0;"><b>You are a valued customer, and you have the following rights and responsibilities</b></p>
        <ol type="1" style="padding-left: 16px; margin:0">
            <li style="margin-bottom:0;">Right to be promptly and fully informed of any changes in the plan of service.</li>
            <li style="margin-bottom:0;">Right to accept or refuse services.</li>
            <li style="margin-bottom:0;">Right to be fully informed of the charges of services.</li>
            <li style="margin-bottom:0;">Right to be informed of the name, business telephone number and business address of the person supervising the services and how to contact that person.</li>
            <li style="margin-bottom:0;">Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time. The complaint procedure provided shall include the business address and telephone number of the person designated by the provider to handle complaints and questions.</li>
            <li style="margin-bottom:0;">Right of confidentiality of client records.</li>
            <li style="margin-bottom:0;">Right to have property and residence treated with respect.</li>
            <li style="margin-bottom:0;">Right to receive a written notice of the address and telephone number of the state licensing authority, namely the department of Human Resources which is charged the responsibility of licensing the provider and investigating client complaints that appear to violate licensing regulation.</li>
            <li style="margin-bottom:0;">Right to obtain a copy of the provider’s most recent completed report of licensure inspection from the provider upon written request. The provider is not required to release the report of licensure inspection until the provider has had an opportunity to file a written plan of correction for the violations, if any, identified.</li>
            <li style="margin-bottom:0;">The facility may charge the client reasonable photocopying charges.</li>
            <li style="margin-bottom:0;">Responsibility to advise the provider of any changes in the care recipient’s condition of any events that affect the care recipient’s service needs</li>
            <li style="margin-bottom:0;">For further assistance or other issues, you may call the OPTIONS Manager, at 404-634-1111, or you may call the State Licensing authority for private home care providers at: Georgia Department of Community Health, Healthcare Facility Regulation Division, 2 Peachtree Street, NW, Suite 31-447, Atlanta, GA 30303-3142, (404) 657-5850. For complaints (404) 657-5728. It is your right to report abuse, neglect or exploitation. Please call toll free 1-800-962-2873.</li>
        </ol>
        '''
    
    # CLEVELAND/DC/OTHER BRANCHES
    elif branch in ['clhomecare', 'clhomecare_staging', 'blmdhomecare', 'blmdhomecare_staging', 
                    'ciohhomecare', 'ciohhomecare_staging', 'chazhomecare', 'chazhomecare_staging',
                    'shmihomecare', 'shmihomecare_staging']:
        
        manager_info = get_manager_info(branch)
        html += f'''
        <p style="font-size:9px;text-align:center;margin:0;"><b><u>Notice of Patients’ Rights and Responsibilities</u></b></p>
        <p style="font-size:7px;margin:0;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE FOLLOWING RIGHTS AND RESPONSIBILITIES:</p>
        <ol type="1" style="padding-left: 16px;margin:0">
            <li style="margin-bottom:0;">Right to accept or refuse services.</li>
            <li style="margin-bottom:0;">Right to be fully informed of the charges of the services.</li>
            <li style="margin-bottom:0;">Right to be fully informed of the name, business telephone number and business address of the person supervising the service and how to contact that person.</li>
            <li style="margin-bottom:0;">Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time.</li>
            <li style="margin-bottom:0;">Right of confidentiality of patient records.</li>
            <li style="margin-bottom:0;">Right to have your property and residence treated with respect.</li>
            <li style="margin-bottom:0;">Responsibility to advise the provider of any changes in your condition or any events that affect your service needs.</li>
            <li style="margin-bottom:0;">Responsibility to treat the OPTIONS’ caregivers with respect.</li>
            <li style="margin-bottom:0;">For further assistance, you may call and speak with an OPTIONS manager at {manager_info['manager_phone']}</li>                
        </ol>
        <p style="font-size:7px;text-align:center;margin:0;"><b><u>Notice of Complaint Procedures</u></b></p>
        <p style="font-size:7px;margin:0;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
        <ol type="1" style="padding-left: 16px;margin:0">
            <li style="margin-bottom:0;">Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Community Relations Manager. Their office number is {manager_info['complaint_phone']}.</li>
            <li style="margin-bottom:0;">OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
            <li style="margin-bottom:0;">The OPTIONS employee who will be responsible for investigating complaints is the Community Relations Manager or the Care Manager.</li>
            <li style="margin-bottom:0;">OPTIONS will produce a written record of the findings of each complaint investigated.</li>
            <li style="margin-bottom:0;">The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Community Relations Manager.</li>
            <li style="margin-bottom:0;">The local social service department Adult Protective Services unit will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient’s property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
            <li style="margin-bottom:0;">The Community Relations Manager is the agency employee who will, within 10 business days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
            <li style="margin-bottom:0;">If you are not satisfied with the proposed resolution, you may appeal to an agency Director {manager_info['director_info']}, in which case they would review the case and get back to you in writing within 21 days of receipt of the appeal.</li>
        </ol>
        '''
    
    # VIRGINIA BRANCHES
    elif branch in ['nvahomecare', 'nvahomecare_staging', 'nvahomecarearchive', 'nvahomecarearchive_staging',
                    'rihomecare', 'rihomecare_staging', 'mnhomecare', 'mnhomecare_staging',
                    'lovahomecare', 'lovahomecare_staging', 'sfvahomecare', 'sfvahomecare_staging',
                    'amfvahomecare', 'amfvahomecare_staging', 'wfvahomecare', 'wfvahomecare_staging',
                    'cfairfaxhomecare', 'cfairfaxhomecare_staging']:
        
        admin_info = get_admin_info(branch)
        html += f'''
        <p style="font-size:7px;text-align:center;margin:0;"><b><u>Notice of Patients’ Rights and Responsibilities</u></b></p>
        <p style="font-size:7px;text-align:center;margin:0;">YOU ARE A VALUED CUSTOMER, AND YOU HAVE THE RIGHT TO BE:</p>
        <ol type="1" style="padding-left: 16px;margin:0">
            <li style="margin-bottom:0;">Treated with courtesy, consideration and respect and is assured of the right of privacy.</li>
            <li style="margin-bottom:0;">Assured confidential treatment of medical and financial records as provided by law.</li>
            <li style="margin-bottom:0;">Free from mental and physical abuse, neglect, and property exploitation.</li>
            <li style="margin-bottom:0;">Assured the right to participate in the planning of the client\'s home care, including the right to refuse services.</li>
            <li style="margin-bottom:0;">Served by individuals who are properly trained and competent to perform their duties.</li>
            <li style="margin-bottom:0;">Assured the right to voice grievances and complaints related to the organizational services without fear of reprisal.</li>
            <li style="margin-bottom:0;">Advised, before care is initiated, of the extent to which payment for the home care organization services may be expected from federal or state programs, and the extent to which payment may be required from the client.</li>
            <li style="margin-bottom:0;">Advised orally and in writing of any changes in fees for services that are the client\'s responsibility. The home care organization shall advise the client of these changes as soon as possible, but no later than 30 calendar days from the date the home care organization became aware of the changes.</li>
            <li style="margin-bottom:0;">Provided with advance directive information prior to start of services.</li>
            <li style="margin-bottom:0;">Given at least five days written notice when the organization determines to terminate services.</li>
        </ol>
        <p style="font-size:7px;text-align:center;margin:0;"><b><u>Notice of Complaint Procedures</u></b></p>
        <p style="font-size:7px;text-align:left;margin:0;">ANY COMPLAINT YOU MAY HAVE WILL BE TREATED EXPEDITIOUSLY AS FOLLOWS:</p>
        <ol type="1" style="padding-left: 16px;margin:0">
            <li style="margin-bottom:0;">Please be advised that at OPTIONS, the person responsible for complaints intake and acknowledgement of complaints is the Administrator or the Administrator Alternate. Their office number is {admin_info['phone']}.</li>
            <li style="margin-bottom:0;">OPTIONS has in place a system for logging receipt of complaints, investigation, and resolution of complaints.</li>
            <li style="margin-bottom:0;">The OPTIONS employee who will be responsible for investigating complaints is the Administrator or the Administrator Alternate.</li>
            <li style="margin-bottom:0;">OPTIONS will produce a written record of the findings of each complaint investigated.</li>
            <li style="margin-bottom:0;">The agency employee who will be responsible for review of investigation findings and resolution of the complaint will be the Administrator or Administrator Alternate.</li>
            <li style="margin-bottom:0;">The local social service department of Adult Protective Services will be informed if at any stage of investigating or resolving a complaint the investigating employee deems that a practical resolution of the complaint is not possible, and that harm may result to the patient or to the patient’s property. At such a point, the investigating employee will contact Adult Protective Services and give them an intake.</li>
            <li style="margin-bottom:0;">The Administrator or Administrator Alternate is the agency employee who will, within 30 days from the date of receipt of a complaint, provide written notification to the complainant of the proposed resolution.</li>
            <li style="margin-bottom:0;">If you are not satisfied with the proposed resolution, you may appeal to {admin_info['name']}, {admin_info['title']}, at {admin_info['phone']}, or in writing to OPTIONS, {admin_info['address']}, in which case they would review the case and get back to you in writing within 21 days of receipt of the appeal. You may also contact the Office of the State Long Term Care Ombudsman at 8004 Franklin Farms Drive, Richmond, VA 23229, Tel. (800) 522-3402 or the Office of Licensure and Certification of the Virginia Dept. of Health at 9960 Mayland Drive, Suite 401, Henrico, VA 23233-1485, Tel. (800) 828-1120 and Fax (804) 527-4502.</li>
        </ol>
        '''
    
    # FLORIDA BRANCHES
    elif branch in ['tahomecare', 'tahomecare_staging', 'woflhomecare', 'woflhomecare_staging', 
                    'lzflhomecare', 'lzflhomecare_staging', 'wpbflhomecare', 'wpbflhomecare_staging']:
        html += '''
        <p style="font-size:7px;text-align:center;margin:0;"><b><u>NOTICE OF RIGHTS AND RESPONSIBILITIES</u></b></p>
        <p style="font-size:7px;text-align:center;margin:0;"><b>You are a valued customer, and you have the following rights and responsibilities</b></p>
        <ol type="1" style="padding-left: 16px;margin:0">
            <li style="margin-bottom:0;">The patient, responsible party, or guardian have the right to be informed of the medical plan of treatment and/or plan of care, to participate in the development of the medical plan of treatment and/or plan of care and to have a copy of the medical plan of treatment and/or plan of care if requested. Our Registered Nurses are available to make initial assessments and develop a plan of care, as well as visits to patient’s home per patient, responsible party, or guardian’s request at an additional cost of $95.00/visit.</li>
            <li style="margin-bottom:0;">Right to accept or refuse services.</li>
            <li style="margin-bottom:0;">Right to be fully informed of the charges of services.</li>
            <li style="margin-bottom:0;">Right to be informed of the name, business telephone number and business address of the person supervising the services and how to contact that person.</li>
            <li style="margin-bottom:0;">Right to be informed of the complaint procedures and the right to submit complaints without fear of discrimination or retaliation and to have them investigated by the provider within a reasonable period of time. The complaint procedure provided shall include the business address and telephone number of the person designated by the provider to handle complaints and questions.</li>
            <li style="margin-bottom:0;">Right of confidentiality of client records.</li>
            <li style="margin-bottom:0;">Right to have property and residence treated with respect.</li>
            <li style="margin-bottom:0;">Responsibility to advise the provider of any changes in the care recipient’s condition of any events that affect the care recipient’s service needs.</li>
            <li style="margin-bottom:0;">To report a complaint regarding the services you receive, please call toll free 1-888-419-3456.</li>
            <li style="margin-bottom:0;">To report abuse, neglect, or exploitation, please call toll free 1-800-962-2873.</li>
        </ol>
        '''
    
    # Add Notice of Billing Procedures for all branches
    html += f'''
    <p style="font-size:9px;text-align:center;margin:0;"><b><u>Notice of Billing Procedures</u></b></p>
    <p style="font-size:7px;margin:0;">BILLING, BILLING ERRORS AND REFUNDS ARE TREATED AS FOLLOWS:</p>
    <ol type="1" style="padding-left: 10px;margin:0">
        <li style="margin-bottom:0;"><u>Billing Method:</u> &nbsp;OPTIONS is a long-term home care agency, and billing is done, by way of invoices, on a weekly or bi-weekly basis. Given that billing is typically done after services are provided, invoices are due upon receipt.</li>
        <li style="margin-bottom:0;"><u>When Payers are Insurance Companies or Third Parties:</u> &nbsp;OPTIONS typically seeks to obtain an "Assignment of Benefits" form from the care recipient or their designees, and OPTIONS then invoices the third party, copying the care recipient or their designees with all invoices sent to the third party.</li>
        <li style="margin-bottom:0;"><u>Patient Notification of Changes in Fees and Charges:</u> &nbsp;We endeavor to notify the care recipient or their designees in writing of any changes in fees or charges, at least two (2) weeks ahead of the effective date of the new changes. Rate increases typically occur following each 12 months of service.</li>
        <li style="margin-bottom:0;"><u>Correction of Billing Errors and Refund Policy:</u> &nbsp;Billing errors will be corrected in subsequent invoices. All refunds are either credited to the care recipient\'s account if it is an ongoing case, or are paid back to the care recipient.</li>
        <li style="margin-bottom:0;"><u>Collection of Delinquent Care Recipient Accounts:</u> &nbsp;Any account more than 30 days past due shall be subject to interest charges of 1 ½ % per month (18% annual) from the invoice due date. If it becomes necessary to refer your account to an attorney for collection, you will be responsible for court costs and attorney\'s fees of no less than 1/3 (33.33%) of the principal balance, in addition to the interest charges listed above.</li>
    </ol>
    </div>
    '''
    
    # Signature section - with page break protection, no top margin
    html += '<div style="page-break-inside: avoid; margin-top: 0;">'
    
    if branch in ['athomecare', 'athomecare_staging', 'scgahomecare', 'scgahomecare_staging']:
        html += get_signature_3col_page2(clt_first, clt_last, clt_relationship, handled_by, current_date)
    else:
        html += get_signature_2col_page2(clt_first, clt_last, clt_relationship, current_date)
    
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
    elif branch in ['shmihomecare', 'shmihomecare_staging']:
        info['manager_phone'] = '586.344.8436'
        info['complaint_phone'] = '586.344.8436'
        info['director_info'] = 'in writing to 13854 Lakeside Circle, Suite 250, Sterling Heights, MI 48313'
    
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

def get_signature_3col_page2(clt_first, clt_last, clt_relationship, handled_by, current_date):
    """3-column signature for GA/SC branches on page 2"""
    return f'''
    <table width="100%" style="font-size:7px;margin-top:0; border-collapse: collapse;">
        <tr>
            <td style="padding-left:1px;" width="33.33%">
                <p style="margin:0;"><b>{clt_first} {clt_last}</b></p>
                <div style="border-top:1px solid black; width:98%; margin:0 auto;"></div>
                <p style="margin:0; text-align:center;">Name of Responsible Party</p>
            </td>
            <td style="padding-left:1px;" width="33.33%">
                <p style="margin:0;"><b>{clt_relationship}</b></p>
                <div style="border-top:1px solid black; width:98%; margin:0 auto;"></div>
                <p style="margin:0; text-align:center;">Relationship to Care Recipient</p>
            </td>
            <td style="padding-left:1px;" width="33.33%">
                <p style="margin:0;"><b>{handled_by}</b></p>
                <div style="border-top:1px solid black; width:98%; margin:0 auto;"></div>
                <p style="margin:0; text-align:center;">Options Representative</p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding-top:2px;">
                <div style="border-top:1px solid black; width:85%; margin:0 auto;"></div>
                <p style="margin:0;">Signature (SEAL)</p>
            </td>
            <td align="center" style="padding-top:2px;">&nbsp;</td>
            <td align="center" style="padding-top:2px;">
                <div style="border-top:1px solid black; width:85%; margin:0 auto;"></div>
                <p style="margin:0;">Signature</p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding-top:2px;">
                <div style="border-top:1px solid black; width:85%; margin:0 auto;"></div>
                <p style="margin:0;">Date: {current_date}</p>
            </td>
            <td align="center" style="padding-top:2px;">&nbsp;</td>
            <td align="center" style="padding-top:2px;">
                <div style="border-top:1px solid black; width:85%; margin:0 auto;"></div>
                <p style="margin:0;">Date: {current_date}</p>
            </td>
        </tr>
    </table>
    '''

def get_signature_2col_page2(clt_first, clt_last, clt_relationship, current_date):
    """2-column signature for most branches on page 2"""
    return f'''
    <table width="100%" style="font-size:7px;margin-top:0; border-collapse: collapse;">
        <tr>
            <td align="center" width="50%" style="padding-right:1px;">
                <p style="margin:0;"><b>{clt_first} {clt_last}</b></p>
                <div style="border-top:1px solid black; width:95%; margin:0 auto;"></div>
                <p style="margin:0;">Name of Responsible Party</p>
            </td>
            <td align="center" width="50%" style="padding-left:1px;">
                <p style="margin:0;"><b>{clt_relationship}</b></p>
                <div style="border-top:1px solid black; width:95%; margin:0 auto;"></div>
                <p style="margin:0;">Relationship to Care Recipient</p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding-top:2px;">
                <p style="margin:0;">(SEAL)</p>
                <div style="border-top:1px solid black; width:80%; margin:0 auto;"></div>
                <p style="margin:0;">Signature</p>
            </td>
            <td align="center" style="padding-top:2px;">
                <div style="border-top:1px solid black; width:80%; margin:0 auto;"></div>
                <p style="margin:0;">Date: {current_date}</p>
            </td>
        </tr>
    </table>
    '''