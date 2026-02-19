from database import SessionLocal, engine
import models

# This ensures the table exists
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Helper function to parse address into address_line_1 and address_line_2
def parse_address(full_address):
    """Parse address string into address_line_1 and address_line_2"""
    if not full_address:
        return "", ""
    
    # Check if address contains "Suite" or similar
    parts = full_address.split(', Suite ')
    if len(parts) == 2:
        return parts[0], f"Suite {parts[1]}"
    elif ', Suite' in full_address:
        idx = full_address.find(', Suite')
        return full_address[:idx], full_address[idx+2:]
    else:
        return full_address, ""

branches_to_insert = [
    {"branch_code": "scgahomecare", "office_name": "Options For Senior America", "address_line_1": "2110 Powers Ferry Rd", "address_line_2": "Suite 306", "city": "Atlanta", "state_code": "GA", "zip_code": "30339", "tel": "404.634.1111", "fax": "404.634.1199", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False},
    {"branch_code": "gbhomecare", "office_name": "Options For Senior America", "address_line_1": "215 Alamance Road", "address_line_2": "", "city": "Burlington", "state_code": "NC", "zip_code": "27215", "tel": "336.270.6647", "fax": "", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False},
    {"branch_code": "rdhomecare", "office_name": "Options For Senior America", "address_line_1": "315 East Chatham Street", "address_line_2": "Suite 201", "city": "Cary", "state_code": "NC", "zip_code": "27511", "tel": "919.380.6812", "fax": "", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False},
    {"branch_code": "mnhomecare", "office_name": "Options For Senior America", "address_line_1": "10432 Balls Ford Road", "address_line_2": "Suite 300", "city": "Manassas", "state_code": "VA", "zip_code": "20109", "tel": "571.449.6781", "fax": "571.921.4622", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False},
    {"branch_code": "lovahomecare", "office_name": "Options For Senior America", "address_line_1": "13800 Coppermine Road", "address_line_2": "Suite 125-A", "city": "Herndon", "state_code": "VA", "zip_code": "20171", "tel": "571.999.5464", "fax": "571.207.7600", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False},
    {"branch_code": "lkinhomecare", "office_name": "Options for Senior America", "address_line_1": "8488 Georgia Street", "address_line_2": "Suite D", "city": "Merrillville", "state_code": "IN", "zip_code": "46410", "tel": "219.321.9130", "fax": "219.321.9133", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False},
    {"branch_code": "shmihomecare", "office_name": "Options For Senior America", "address_line_1": "13854 Lakeside Circle", "address_line_2": "Suite 250", "city": "Sterling Heights", "state_code": "MI", "zip_code": "48313", "tel": "586.344.8436", "fax": "586.532.5415", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False},
    {"branch_code": "wenjhomecare", "office_name": "Options For Senior America", "address_line_1": "70 S. Orange Avenue", "address_line_2": "Suite 105", "city": "Livingston", "state_code": "NJ", "zip_code": "07039", "tel": "973.803.0901", "fax": "973.808.1991", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False},
    {"branch_code": "wfvahomecare", "office_name": "Options for Senior America", "address_line_1": "13800 Coppermine Road", "address_line_2": "Suite 125-B", "city": "Herndon", "state_code": "VA", "zip_code": "20171", "tel": "571.999.5464", "fax": "571.207.7600", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False},
    {"branch_code": "cfairfaxhomecare", "office_name": "Options for Senior America", "address_line_1": "13800 Coppermine Road", "address_line_2": "Suite 125-C", "city": "Herndon", "state_code": "VA", "zip_code": "20171", "tel": "571.999.5464", "fax": "571.207.7600", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False},
    {"branch_code": "amfvahomecare", "office_name": "Options for Senior America", "address_line_1": "11350 Random Hills Road", "address_line_2": "Suite 800", "city": "Fairfax", "state_code": "VA", "zip_code": "22030", "tel": "571.449.6781", "fax": "571.921.4622", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False},
    {"branch_code": "woflhomecare", "office_name": "Options for Senior America", "address_line_1": "7061 Grand National Drive", "address_line_2": "Suite 105C", "city": "Orlando", "state_code": "FL", "zip_code": "32819", "tel": "407.729.7551", "fax": "", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False},
    {"branch_code": "chazhomecare", "office_name": "Options for Senior America", "address_line_1": "920 W. Chandler Blvd", "address_line_2": "Suite 3", "city": "Chandler", "state_code": "AZ", "zip_code": "85225", "tel": "480.673.3888", "fax": "888.511.8962", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False},
    {"branch_code": "nspahomecare", "office_name": "Options for Senior America", "address_line_1": "175 Strafford Avenue", "address_line_2": "Suite One", "city": "Wayne", "state_code": "PA", "zip_code": "19087", "tel": "610.975.4422", "fax": "610.514.5560", "notice_period_days": 10, "holiday_count": 12, "requires_consumer_notice": True},
    {"branch_code": "ciohhomecare", "office_name": "Options For Senior America", "address_line_1": "10925 Reed Hartman Hwy", "address_line_2": "Suite 310-E", "city": "Cincinnati", "state_code": "OH", "zip_code": "45242", "tel": "513.928.0042", "fax": "513.880.0044", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False},
    {"branch_code": "sfvahomecare", "office_name": "Options For Senior America", "address_line_1": "7830 Backlick Rd", "address_line_2": "Suite 200-A", "city": "Springfield", "state_code": "VA", "zip_code": "22150", "tel": "571.416.8260", "fax": "571.415.5460", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False},
    {"branch_code": "blmdhomecare", "office_name": "Options For Senior America", "address_line_1": "4690 Millennium Drive", "address_line_2": "", "city": "Belcamp", "state_code": "MD", "zip_code": "21017", "tel": "667.450.2289", "fax": "667.444.4042", "notice_period_days": 3, "holiday_count": 11, "requires_consumer_notice": False}
]

try:
    from branch_config import get_branch_config
    
    for branch_data in branches_to_insert:
        # Check if this branch code already exists
        existing_branch = db.query(models.Branch).filter(
            models.Branch.branch_code == branch_data['branch_code']
        ).first()

        # Get branch config for state-specific settings
        state_code = branch_data.get('state_code', 'MD')
        branch_config = get_branch_config(branch_data['branch_code'], state_code)
        
        # Add state-specific configuration
        branch_data['state_authority'] = branch_config.get('state_authority', '')
        branch_data['manager_phone'] = branch_config.get('manager_phone', '')
        branch_data['footer_version_tag'] = branch_config.get('footer_version', f'{state_code} 2019-09-16')
        branch_data['mileage_rate'] = 0.67  # Default mileage rate

        if existing_branch:
            # Update existing record
            for key, value in branch_data.items():
                if hasattr(existing_branch, key):
                    setattr(existing_branch, key, value)
        else:
            # Insert new record
            new_branch = models.Branch(**branch_data)
            db.add(new_branch)
    
    db.commit()
    print(f"Successfully synchronized {len(branches_to_insert)} branches.")
except Exception as e:
    db.rollback()
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()