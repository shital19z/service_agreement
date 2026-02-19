"""
Updated Branch-specific configuration and state-specific legal language
Includes logic from Page-1 Cont PHP template
"""
from typing import Dict, List, Optional

# Branch display names for dropdown - ADD THIS SECTION
BRANCH_DISPLAY_NAMES = {
    # Maryland Branches
    "anhomecare": "Annapolis Home Care (MD)",
    "anhomecare_staging": "Annapolis Home Care - Staging (MD)",
    "bahomecare": "Baltimore Home Care (MD)",
    "bahomecare_staging": "Baltimore Home Care - Staging (MD)",
    "blhomecare": "Bel Air Home Care (MD)",
    "blhomecare_staging": "Bel Air Home Care - Staging (MD)",
    "fkhomecare": "Frederick Home Care (MD)",
    "fkhomecare_staging": "Frederick Home Care - Staging (MD)",
    "lphomecare": "La Plata Home Care (MD)",
    "lphomecare_staging": "La Plata Home Care - Staging (MD)",
    "blmdhomecare": "Baltimore MD Home Care",
    "blmdhomecare_staging": "Baltimore MD Home Care - Staging",
    "testhomecare": "Test Home Care (MD)",
    "testhomecare_staging": "Test Home Care - Staging (MD)",
    
    # Georgia Branches
    "athomecare": "Atlanta Home Care (GA)",
    "athomecare_staging": "Atlanta Home Care - Staging (GA)",
    "scgahomecare": "South Carolina/Georgia Home Care",
    "scgahomecare_staging": "South Carolina/Georgia Home Care - Staging",
    
    # Ohio Branches
    "clhomecare": "Cleveland Home Care (OH)",
    "clhomecare_staging": "Cleveland Home Care - Staging (OH)",
    "ciohhomecare": "Cincinnati Home Care (OH)",
    "ciohhomecare_staging": "Cincinnati Home Care - Staging (OH)",
    
    # Arizona Branch
    "chazhomecare": "Chandler Home Care (AZ)",
    "chazhomecare_staging": "Chandler Home Care - Staging (AZ)",
    
    # Virginia Branches
    "nvahomecare": "NOVA Home Care (VA)",
    "nvahomecare_staging": "NOVA Home Care - Staging (VA)",
    "nvahomecarearchive": "NOVA Home Care Archive (VA)",
    "nvahomecarearchive_staging": "NOVA Home Care Archive - Staging (VA)",
    "rihomecare": "Richmond Home Care (VA)",
    "rihomecare_staging": "Richmond Home Care - Staging (VA)",
    "mnhomecare": "Manassas Home Care (VA)",
    "mnhomecare_staging": "Manassas Home Care - Staging (VA)",
    "lovahomecare": "Loudoun Valley Home Care (VA)",
    "lovahomecare_staging": "Loudoun Valley Home Care - Staging (VA)",
    "sfvahomecare": "Springfield Home Care (VA)",
    "sfvahomecare_staging": "Springfield Home Care - Staging (VA)",
    "amfvahomecare": "Arlington/Manassas/Fairfax Home Care (VA)",
    "amfvahomecare_staging": "Arlington/Manassas/Fairfax Home Care - Staging (VA)",
    "wfvahomecare": "Winchester/Frederick Home Care (VA)",
    "wfvahomecare_staging": "Winchester/Frederick Home Care - Staging (VA)",
    "cfairfaxhomecare": "Centreville/Fairfax Home Care (VA)",
    "cfairfaxhomecare_staging": "Centreville/Fairfax Home Care - Staging (VA)",
    
    # Florida Branches
    "tahomecare": "Tampa Home Care (FL)",
    "tahomecare_staging": "Tampa Home Care - Staging (FL)",
    "woflhomecare": "Winter Park/Orlando Home Care (FL)",
    "woflhomecare_staging": "Winter Park/Orlando Home Care - Staging (FL)",
    "lzflhomecare": "Lake Zurich FL Home Care",
    "lzflhomecare_staging": "Lake Zurich FL Home Care - Staging (FL)",
    "wpbflhomecare": "West Palm Beach Home Care (FL)",
    "wpbflhomecare_staging": "West Palm Beach Home Care - Staging (FL)",
    
    # North Carolina Branches
    "gbhomecare": "Greensboro Home Care (NC)",
    "gbhomecare_staging": "Greensboro Home Care - Staging (NC)",
    "rdhomecare": "Raleigh/Durham Home Care (NC)",
    "rdhomecare_staging": "Raleigh/Durham Home Care - Staging (NC)",
    
    # Indiana Branch
    "lkinhomecare": "Lake County Home Care (IN)",
    "lkinhomecare_staging": "Lake County Home Care - Staging (IN)",
    
    # Michigan Branch
    "shmihomecare": "Sterling Heights Home Care (MI)",
    "shmihomecare_staging": "Sterling Heights Home Care - Staging (MI)",
    
    # New Jersey Branch
    "wenjhomecare": "West Essex Home Care (NJ)",
    "wenjhomecare_staging": "West Essex Home Care - Staging (NJ)",
    
    # Pennsylvania Branches
    "hbhomecare": "Harrisburg Home Care (PA)",
    "hbhomecare_staging": "Harrisburg Home Care - Staging (PA)",
    "nspahomecare": "Newtown Square/Philadelphia Home Care (PA)",
    "nspahomecare_staging": "Newtown Square/Philadelphia Home Care - Staging (PA)",
    
    # DC Branch
    "dchomecare": "DC Home Care",
    "dchomecare_staging": "DC Home Care - Staging",
    
    # Test Branches
    "test2homecare": "Test 2 Home Care",
    "test2homecare_staging": "Test 2 Home Care - Staging",
    "tomdhomecare": "TO Maryland Home Care",
    "tomdhomecare_staging": "TO Maryland Home Care - Staging",
}

# Branch addresses for database seeding - ADD THIS NEW SECTION
BRANCH_ADDRESSES = {
    # Maryland Branches
    "anhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "200 Harry S. Truman Parkway",
        "address_line_2": "Suite 205",
        "city": "Annapolis",
        "zip_code": "21401",
        "tel": "410.224.2700",
        "fax": "410.224.2701"
    },
    "bahomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "6 St. Paul Street",
        "address_line_2": "Suite 1500",
        "city": "Baltimore",
        "zip_code": "21202",
        "tel": "410.448.1100",
        "fax": "410.448.1101"
    },
    "blhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "5 Bel Air South Parkway",
        "address_line_2": "Suite 104",
        "city": "Bel Air",
        "zip_code": "21015",
        "tel": "410.893.9914",
        "fax": "410.893.9915"
    },
    "fkhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "1300 W. Patrick Street",
        "address_line_2": "Suite 2B",
        "city": "Frederick",
        "zip_code": "21702",
        "tel": "301.624.5630",
        "fax": "301.624.5631"
    },
    "lphomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "100 La Grange Avenue",
        "address_line_2": "Suite 210",
        "city": "La Plata",
        "zip_code": "20646",
        "tel": "301.392.1387",
        "fax": "301.392.1388"
    },
    "blmdhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "4690 Millennium Drive",
        "address_line_2": "",
        "city": "Belcamp",
        "zip_code": "21017",
        "tel": "667.415.8317",
        "fax": ""
    },
    
    # Georgia Branches
    "athomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "5909 Peachtree Dunwoody Rd",
        "address_line_2": "Suite 800",
        "city": "Atlanta",
        "zip_code": "30328",
        "tel": "404.634.1111",
        "fax": ""
    },
    "scgahomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "5909 Peachtree Dunwoody Rd",
        "address_line_2": "Suite 800",
        "city": "Atlanta",
        "zip_code": "30328",
        "tel": "404.634.1111",
        "fax": ""
    },
    
    # Ohio Branches
    "clhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "2000 Auburn Drive",
        "address_line_2": "Suite 200",
        "city": "Beachwood",
        "zip_code": "44122",
        "tel": "216.861.3700",
        "fax": ""
    },
    "ciohhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "4555 Lake Forest Drive",
        "address_line_2": "Suite 650",
        "city": "Cincinnati",
        "zip_code": "45242",
        "tel": "513.928.0042",
        "fax": ""
    },
    
    # Arizona Branch
    "chazhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "920 W. Chandler Blvd",
        "address_line_2": "Suite 3",
        "city": "Chandler",
        "zip_code": "85225",
        "tel": "480.673.3888",
        "fax": ""
    },
    
    # Virginia Branches
    "nvahomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "6 Montgomery Village Avenue",
        "address_line_2": "Suite 330",
        "city": "Gaithersburg",
        "zip_code": "20879",
        "tel": "301.562.1100",
        "fax": "301.562.1133"
    },
    "rihomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "6 Montgomery Village Avenue",
        "address_line_2": "Suite 330",
        "city": "Gaithersburg",
        "zip_code": "20879",
        "tel": "804.673.6730",
        "fax": ""
    },
    "mnhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "10432 Balls Ford Road",
        "address_line_2": "Suite 300",
        "city": "Manassas",
        "zip_code": "20109",
        "tel": "571.449.6781",
        "fax": ""
    },
    "lovahomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "13800 Coppermine Road",
        "address_line_2": "Suite 125-A",
        "city": "Herndon",
        "zip_code": "20171",
        "tel": "571.999.5464",
        "fax": ""
    },
    "sfvahomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "7830 Backlick Road",
        "address_line_2": "Suite 200-A",
        "city": "Springfield",
        "zip_code": "22150",
        "tel": "571.416.8260",
        "fax": ""
    },
    "amfvahomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "11350 Random Hills Rd",
        "address_line_2": "Suite 800",
        "city": "Fairfax",
        "zip_code": "22030",
        "tel": "571.449.6781",
        "fax": ""
    },
    "wfvahomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "13800 Coppermine Road",
        "address_line_2": "Suite 104-B",
        "city": "Herndon",
        "zip_code": "20171",
        "tel": "703.622.7132",
        "fax": ""
    },
    "cfairfaxhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "13800 Coppermine Road",
        "address_line_2": "Suite 104-B",
        "city": "Herndon",
        "zip_code": "20171",
        "tel": "703.622.7132",
        "fax": ""
    },
    
    # Florida Branches
    "tahomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "3300 W. Cypress Street",
        "address_line_2": "Suite 100",
        "city": "Tampa",
        "zip_code": "33607",
        "tel": "813.555.0123",
        "fax": ""
    },
    "woflhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "100 W. Pine Street",
        "address_line_2": "Suite 200",
        "city": "Orlando",
        "zip_code": "32801",
        "tel": "407.555.0123",
        "fax": ""
    },
    "lzflhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "200 N. Dale Mabry Highway",
        "address_line_2": "Suite 300",
        "city": "Tampa",
        "zip_code": "33609",
        "tel": "813.555.0124",
        "fax": ""
    },
    "wpbflhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "500 S. Australian Avenue",
        "address_line_2": "Suite 400",
        "city": "West Palm Beach",
        "zip_code": "33401",
        "tel": "561.555.0123",
        "fax": ""
    },
    
    # North Carolina Branches
    "gbhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "701 Green Valley Road",
        "address_line_2": "Suite 300",
        "city": "Greensboro",
        "zip_code": "27408",
        "tel": "336.270.6647",
        "fax": ""
    },
    "rdhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "3605 Glenwood Avenue",
        "address_line_2": "Suite 200",
        "city": "Raleigh",
        "zip_code": "27612",
        "tel": "919.380.6812",
        "fax": ""
    },
    
    # Indiana Branch
    "lkinhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "8488 Georgia Street",
        "address_line_2": "Suite D",
        "city": "Merrillville",
        "zip_code": "46410",
        "tel": "219.321.9130",
        "fax": ""
    },
    
    # Michigan Branch
    "shmihomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "13854 Lakeside Circle",
        "address_line_2": "Suite 250",
        "city": "Sterling Heights",
        "zip_code": "48313",
        "tel": "586.344.8436",
        "fax": ""
    },
    
    # New Jersey Branch
    "wenjhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "70 South Orange Avenue",
        "address_line_2": "Suite 105",
        "city": "Livingston",
        "zip_code": "07039",
        "tel": "973.803.0901",
        "fax": ""
    },
    
    # Pennsylvania Branches
    "hbhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "6 Montgomery Village Avenue",
        "address_line_2": "Suite 330",
        "city": "Gaithersburg",
        "zip_code": "20879",
        "tel": "717.510.8613",
        "fax": ""
    },
    "nspahomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "175 Strafford Avenue",
        "address_line_2": "Suite One",
        "city": "Wayne",
        "zip_code": "19087",
        "tel": "610.975.4422",
        "fax": "610.514.5560"
    },
    
    # DC Branch
    "dchomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "6 Montgomery Village Avenue",
        "address_line_2": "Suite 330",
        "city": "Gaithersburg",
        "zip_code": "20879",
        "tel": "202.581.2000",
        "fax": ""
    },
    
    # Test Branches
    "testhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "6 Montgomery Village Avenue",
        "address_line_2": "Suite 330",
        "city": "Gaithersburg",
        "zip_code": "20879",
        "tel": "301.562.1100",
        "fax": "301.562.1133"
    },
    "test2homecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "6 Montgomery Village Avenue",
        "address_line_2": "Suite 330",
        "city": "Gaithersburg",
        "zip_code": "20879",
        "tel": "301.562.1100",
        "fax": "301.562.1133"
    },
    "tomdhomecare": {
        "office_name": "Options For Senior America",
        "address_line_1": "6 Montgomery Village Avenue",
        "address_line_2": "Suite 330",
        "city": "Gaithersburg",
        "zip_code": "20879",
        "tel": "301.562.1100",
        "fax": "301.562.1133"
    }
}

# State regulatory authorities
STATE_AUTHORITIES = {
    "MD": "Maryland Office of Health Care Quality",
    "VA": "Virginia Department of Health",
    "GA": "Georgia Department of Community Health, Healthcare Facility Regulation Division",
    "FL": "Florida Agency for Health Care Administration",
    "PA": "Pennsylvania Department of Health",
    "NJ": "New Jersey Department of Health",
    "OH": "Ohio Department of Health",
    "IN": "Indiana State Department of Health",
    "AZ": "Arizona Department of Health Services",
    "NC": "North Carolina Department of Health and Human Services",
    "MI": "Michigan Department of Health and Human Services",
    "DC": "District of Columbia Department of Health",
}

# Mapping for Governing Law text
STATE_GOVERNING_NAMES = {
    "NC": "North Carolina",
    "GA": "Georgia",
    "VA": "Commonwealth of Virginia",
    "OH": "Ohio",
    "PA": "Pennsylvania",
    "IN": "Indiana",
    "NJ": "New Jersey",
    "AZ": "Arizona",
    "FL": "Florida",
    "DC": "District of Columbia",
    "MD": "Maryland"
}

# Branches requiring the "Medication Administration" RN/CMT clause
MEDICATION_CLAUSE_BRANCHES = [
    'athomecare', 'scgahomecare', 'clhomecare', 'ciohhomecare', 'nvahomecare', 
    'rihomecare', 'tahomecare', 'mnhomecare', 'lovahomecare', 'sfvahomecare', 
    'lkinhomecare', 'shmihomecare', 'wfvahomecare', 'cfairfaxhomecare', 
    'amfvahomecare', 'woflhomecare', 'nspahomecare', 'lzflhomecare'
]

# Branches requiring "Needs Assessment & Valuables" sections
ASSESSMENT_FEE_BRANCHES = [
    'athomecare', 'scgahomecare', 'tahomecare', 'woflhomecare', 'dchomecare',
    'bahomecare', 'lphomecare', 'amfvahomecare', 'rihomecare', 'cfairfaxhomecare',
    'sfvahomecare', 'chazhomecare', 'hbhomecare', 'nspahomecare', 'lzflhomecare', 
    'blmdhomecare', 'wpbflhomecare'
]

# Standard holidays
STANDARD_11_HOLIDAYS = [
    "New Year's Day", "Martin Luther King Day", "Presidents' Day", "Memorial Day",
    "Juneteenth Day", "Independence Day", "Labor Day", "Columbus Day",
    "Veterans' Day", "Thanksgiving Day", "Christmas Day"
]

# Function to get branch options for dropdown
def get_branch_options():
    """
    Return list of branch options for dropdown
    Returns: List of dictionaries with 'code' and 'name' keys
    """
    options = []
    for code, name in BRANCH_DISPLAY_NAMES.items():
        options.append({"code": code, "name": name})
    # Sort alphabetically by name
    options.sort(key=lambda x: x["name"])
    return options

# Function to get branch options as HTML
def get_branch_options_html():
    """
    Return HTML options for branch select dropdown
    """
    html_options = ['<option value="">-- Select Branch --</option>']
    for code, name in sorted(BRANCH_DISPLAY_NAMES.items(), key=lambda x: x[1]):
        html_options.append(f'<option value="{code}">{name}</option>')
    return '\n'.join(html_options)

# NEW FUNCTION - Get branch address
def get_branch_address(branch_code: str) -> dict:
    """Get address for a specific branch"""
    return BRANCH_ADDRESSES.get(branch_code, {
        "office_name": "Options For Senior America",
        "address_line_1": "",
        "address_line_2": "",
        "city": "",
        "zip_code": "",
        "tel": "",
        "fax": ""
    })

# NEW FUNCTION - Get all branches with complete info
def get_all_branches_info() -> List[dict]:
    """Get complete information for all branches including addresses"""
    branches = []
    for code, display_name in BRANCH_DISPLAY_NAMES.items():
        addr = get_branch_address(code)
        branch_info = {
            "code": code,
            "display_name": display_name,
            "office_name": addr["office_name"],
            "address_line_1": addr["address_line_1"],
            "address_line_2": addr["address_line_2"],
            "city": addr["city"],
            "zip_code": addr["zip_code"],
            "tel": addr["tel"],
            "fax": addr["fax"]
        }
        branches.append(branch_info)
    return branches

def get_branch_config(branch_code: str, state_code: str) -> Dict:
    """
    Get branch-specific configuration
    
    Args:
        branch_code: The branch code (e.g., 'anhomecare')
        state_code: The state code (e.g., 'MD')
    
    Returns:
        Dictionary with branch configuration
    """
    b_code = branch_code.lower() if branch_code else ""
    s_code = state_code.upper() if state_code else "MD"
    
    # 1. Determine Notice Period 
    notice_days = 3
    notice_text = "OPTIONS, however, may end services with 3 calendar days' written notice."
    if b_code in ['hbhomecare', 'hbhomecare_staging', 'nspahomecare', 'nspahomecare_staging']:
        notice_days = 10
        notice_text = ("OPTIONS may end services under this agreement by giving at least 10 calendar days "
                       "advance written notice. Less than 10 days may be provided if client is more "
                       "than 14 days in arrears or caregiver safety is at risk.")

    # 2. Determine Governing Law 
    gov_state = STATE_GOVERNING_NAMES.get(s_code, "Maryland")
    
    # Override based on branch if needed
    if b_code in ['gbhomecare', 'gbhomecare_staging', 'rdhomecare', 'rdhomecare_staging']:
        gov_state = "North Carolina"
    elif b_code in ['scgahomecare', 'scgahomecare_staging', 'athomecare', 'athomecare_staging']:
        gov_state = "Georgia"
    elif b_code in ['nspahomecare', 'nspahomecare_staging', 'hbhomecare', 'hbhomecare_staging']:
        gov_state = "Pennsylvania"
    elif b_code in ['chazhomecare', 'chazhomecare_staging']:
        gov_state = "Arizona"
    elif b_code in ['wenjhomecare', 'wenjhomecare_staging']:
        gov_state = "New Jersey"
    elif b_code in ['lzflhomecare', 'lzflhomecare_staging', 'wpbflhomecare', 'wpbflhomecare_staging', 'woflhomecare', 'woflhomecare_staging']:
        gov_state = "Florida"
    
    # 3. Determine Margins 
    top_margin = 0.4
    if b_code in ['mnhomecare', 'mnhomecare_staging', 'lovahomecare', 'lovahomecare_staging', 
                  'amfvahomecare', 'amfvahomecare_staging', 'woflhomecare', 'woflhomecare_staging', 
                  'lzflhomecare', 'lzflhomecare_staging']:
        top_margin = 0.2
    elif b_code in ['bahomecare', 'bahomecare_staging', 'lphomecare', 'lphomecare_staging']:
        top_margin = 0.3

    # 4. Medication Administration Clause
    show_med_clause = b_code in [b.lower() for b in MEDICATION_CLAUSE_BRANCHES]
    if s_code == "DC" and b_code.startswith("dc"):
        show_med_clause = True

    # 5. Representative Signature 
    use_rep_sig = b_code in ['scgahomecare', 'scgahomecare_staging', 'athomecare', 'athomecare_staging']

    # 6. Consumer Notice requirement
    requires_consumer_notice = s_code == "PA" or b_code in ["nspahomecare", "bahomecare", "nspahomecare_staging", "bahomecare_staging"]

    # 7. Assessment fee text
    requires_assessment_fee_text = b_code in [b.lower() for b in ASSESSMENT_FEE_BRANCHES]

    # 8. Holiday count (12 for some branches)
    holiday_count = 12 if b_code in ['mnhomecare', 'mnhomecare_staging'] else 11
    holidays = ["Easter Sunday"] + STANDARD_11_HOLIDAYS if b_code in ['mnhomecare', 'mnhomecare_staging'] else STANDARD_11_HOLIDAYS

    # Get branch address if available
    branch_addr = get_branch_address(b_code)

    config = {
        "state_authority": STATE_AUTHORITIES.get(s_code, "State Health Department"),
        "governing_law": f"This agreement is governed by the laws of the state of {gov_state}.",
        "notice_period_days": notice_days,
        "notice_period_text": notice_text,
        "requires_live_in_text": b_code.startswith("test"),
        "requires_consumer_notice": requires_consumer_notice,
        "requires_assessment_fee_text": requires_assessment_fee_text,
        "requires_medication_clause": show_med_clause,
        "use_representative_signature": use_rep_sig,
        "holiday_count": holiday_count,
        "holidays": holidays,
        "pdf_margins": {
            "top": top_margin,
            "bottom": 0.4,
            "left": 0.4,
            "right": 0.4,
        },
        "footer_version": f"{s_code}",
        "branch_display_name": BRANCH_DISPLAY_NAMES.get(b_code, branch_code),
        # Add address info to config
        "office_name": branch_addr["office_name"],
        "address_line_1": branch_addr["address_line_1"],
        "address_line_2": branch_addr["address_line_2"],
        "city": branch_addr["city"],
        "zip_code": branch_addr["zip_code"],
        "tel": branch_addr["tel"],
        "fax": branch_addr["fax"]
    }
    
    return config

def format_holidays_list(holidays: List[str]) -> str:
    """Format holidays list into a readable string"""
    if not holidays: 
        return ""
    if len(holidays) == 1:
        return holidays[0] + "."
    return ", ".join(holidays[:-1]) + ", and " + holidays[-1] + "."

