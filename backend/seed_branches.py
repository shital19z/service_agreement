# seed_branches.py
from database import SessionLocal, engine
import models
from branch_config import BRANCH_DISPLAY_NAMES, get_branch_address
import re

def seed_branches():
    """Seed branches from config to database"""
    db = SessionLocal()
    try:
        # Check if branches table exists and has data
        existing_count = db.query(models.Branch).count()
        print(f"Found {existing_count} existing branches in database")
        
        if existing_count > 0:
            print("\nWhat would you like to do?")
            print("1. Skip - keep existing branches")
            print("2. Update existing branches with new addresses")
            print("3. Delete all and reseed from config")
            choice = input("Enter choice (1/2/3): ").strip()
            
            if choice == "1":
                print("Keeping existing branches. Exiting.")
                return
            elif choice == "2":
                print("Updating existing branches...")
                for code, display_name in BRANCH_DISPLAY_NAMES.items():
                    branch = db.query(models.Branch).filter(
                        models.Branch.branch_code == code
                    ).first()
                    
                    if branch:
                        addr = get_branch_address(code)
                        # Update only columns that exist in tblbranch
                        branch.branch_name = display_name
                        branch.office_name = addr['office_name']
                        branch.street = addr['address_line_1']  # Use street instead of address_line_1
                        branch.city = addr['city']
                        branch.branch_state = state_code  # Will need state_code variable
                        branch.zipcode = addr['zip_code']  # Use zipcode instead of zip_code
                        branch.branch_phone = addr['tel']  # Use branch_phone instead of tel
                        branch.branch_fax = addr['fax']  # Use branch_fax instead of fax
                        print(f"Updated: {code}")
                db.commit()
                print("Update complete!")
                return
            elif choice == "3":
                print("Deleting all branches...")
                db.query(models.Branch).delete()
                db.commit()
                print("All branches deleted.")
            else:
                print("Invalid choice. Exiting.")
                return
        
        # Seed new branches
        print("\nSeeding branches from config...")
        created_count = 0
        
        for code, display_name in BRANCH_DISPLAY_NAMES.items():
            # Check if branch already exists
            existing = db.query(models.Branch).filter(
                models.Branch.branch_code == code
            ).first()
            
            if existing:
                print(f"Branch {code} already exists, skipping...")
                continue
            
            # Get address from config
            addr = get_branch_address(code)
            
            # Extract state from display name (e.g., "(MD)" at the end)
            state_match = re.search(r'\(([A-Z]{2})\)', display_name)
            state_code = state_match.group(1) if state_match else 'MD'
            
            # Create new branch - ONLY using columns that exist in tblbranch
            branch = models.Branch(
                branch_code=code,
                branch_name=display_name,  # Use branch_name field
                office_name=addr['office_name'],
                street=addr['address_line_1'],  # Use street instead of address_line_1
                # address_line_2 doesn't exist in tblbranch - skip it
                city=addr['city'],
                branch_state=state_code,  # Use branch_state instead of state_code
                zipcode=addr['zip_code'],  # Use zipcode instead of zip_code
                branch_phone=addr['tel'],  # Use branch_phone instead of tel
                branch_fax=addr['fax'],  # Use branch_fax instead of fax
                # Set default values for other tblbranch columns
                responsible_title=None,
                care_coordinator_name=None,
                mileage=None,
                admin_meds=False,
                corp_state_long=None,
                office_phone_corp=None,
                fein=None,
                is_corporate=False
            )
            db.add(branch)
            created_count += 1
            print(f"Added: {code} - {display_name}")
        
        db.commit()
        print(f"\nSuccess! Added {created_count} new branches.")
        print(f"Total branches in database: {db.query(models.Branch).count()}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

def show_branches():
    """Display all branches in database"""
    db = SessionLocal()
    try:
        branches = db.query(models.Branch).all()
        print(f"\n{'='*100}")
        print(f"{'Code':15} {'Branch Name':30} {'City':20} {'State':5} {'Phone':15}")
        print(f"{'='*100}")
        for b in branches:
            # Use the correct field names from tblbranch
            print(f"{b.branch_code:15} {b.branch_name or b.office_name or '':30} {b.city or '':20} {b.branch_state or '':5} {b.branch_phone or '':15}")
        print(f"{'='*100}")
        print(f"Total: {len(branches)} branches")
    except Exception as e:
        print(f"Error showing branches: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--show":
            show_branches()
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python seed_branches.py         - Run interactive seeding")
            print("  python seed_branches.py --show  - Show all branches")
            print("  python seed_branches.py --help  - Show this help")
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        seed_branches()