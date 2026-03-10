# seed_branch_content.py
from database import SessionLocal, engine
import models
from branch_config import get_branch_config, BRANCH_DISPLAY_NAMES
from sqlalchemy import text
import json

# This ensures all tables exist
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Default content template for agreements
default_agreement_content = {
    "required_services": "In addition to the general services that our caregivers provide such as assistance with activities of daily living, meal preparation, light housekeeping, and laundry, the required services as stated by the responsible party/client are:",
    "freq_of_visit": "",
    "hourly_rate": 36.00,
    "perc_charged": "100",
    "hazards": "None Reported",
    "mileage_rate": 0.67,
    "care_type": "Home Care",
    "has_initial_contact": False,
    "notice_period": "3 calendar days",
    "holiday_count": 11,
    "requires_consumer_notice": False,
    "special_instructions": ""
}

try:
    # First, check if branch_content table exists, if not create it
    print("Checking if branch_content table exists...")
    
    # Create the branch_content table if it doesn't exist - FIXED: Added text() wrapper
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS branch_content (
            id SERIAL PRIMARY KEY,
            branch_code VARCHAR(50) NOT NULL,
            content_type VARCHAR(50) NOT NULL DEFAULT 'agreement',
            content_data JSONB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (branch_code) REFERENCES tblbranch(branch_code) ON DELETE CASCADE,
            UNIQUE(branch_code, content_type)
        );
    """))
    
    # Create index for faster lookups - FIXED: Added text() wrapper
    db.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_branch_content_branch_code 
        ON branch_content(branch_code);
    """))
    
    db.commit()
    print("✅ branch_content table ready.")
    
    # Get all branches from tblbranch - FIXED: Added text() wrapper
    branches = db.execute(text("SELECT branch_code FROM tblbranch")).fetchall()
    print(f"\nFound {len(branches)} branches in database.")
    
    # Insert/Update content for each branch
    content_added = 0
    content_updated = 0
    
    for branch in branches:
        branch_code = branch[0]
        
        # Get branch-specific config
        state_code = 'MD'  # Default, you can extract from branch name if needed
        config = get_branch_config(branch_code, state_code)
        
        # Start with default content
        content_data = default_agreement_content.copy()
        
        # Override with branch-specific values from config
        content_data.update({
            "hourly_rate": config.get('hourly_rate', 36.00),
            "notice_period": config.get('notice_period_text', '3 calendar days'),
            "holiday_count": config.get('holiday_count', 11),
            "requires_consumer_notice": config.get('requires_consumer_notice', False),
            "has_initial_contact": branch_code in ['scgahomecare', 'scgahomecare_staging', 'athomecare', 'athomecare_staging'],
            "special_instructions": "Initial Contact Date required" if branch_code in ['scgahomecare', 'scgahomecare_staging', 'athomecare', 'athomecare_staging'] else ""
        })
        
        # Check if content already exists for this branch - FIXED: Added text() wrapper
        existing = db.execute(
            text("SELECT id FROM branch_content WHERE branch_code = :code AND content_type = 'agreement'"),
            {"code": branch_code}
        ).fetchone()
        
        if existing:
            # Update existing - FIXED: Added text() wrapper
            db.execute(
                text("""
                    UPDATE branch_content 
                    SET content_data = :data, updated_at = CURRENT_TIMESTAMP 
                    WHERE branch_code = :code AND content_type = 'agreement'
                """),
                {"code": branch_code, "data": json.dumps(content_data)}
            )
            content_updated += 1
            print(f"🔄 Updated content for {branch_code}")
        else:
            # Insert new - FIXED: Added text() wrapper
            db.execute(
                text("""
                    INSERT INTO branch_content (branch_code, content_type, content_data, created_at, updated_at)
                    VALUES (:code, 'agreement', :data, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """),
                {"code": branch_code, "data": json.dumps(content_data)}
            )
            content_added += 1
            print(f"✅ Added content for {branch_code}")
    
    db.commit()
    print(f"\n{'='*50}")
    print(f"SUMMARY:")
    print(f"{'='*50}")
    print(f"Total branches processed: {len(branches)}")
    print(f"New content added: {content_added}")
    print(f"Existing content updated: {content_updated}")
    print(f"{'='*50}")
    
    # Show sample
    sample = db.execute(
        text("SELECT branch_code, content_data FROM branch_content LIMIT 1")
    ).first()
    if sample:
        print(f"\nSample content for {sample[0]}:")
        print(json.dumps(sample[1], indent=2))
    
except Exception as e:
    db.rollback()
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
    print("\n✅ Script execution completed.")