from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Optional
from datetime import datetime, timedelta
import secrets
import os
from utils import send_reset_email

from sqlalchemy.orm import Session
from pydantic import BaseModel

import models
import schemas
import auth
from database import engine, get_db
from auth import get_current_user, authenticate_user, create_access_token
from pdf_generator import json_to_pdf
from branch_config import get_branch_options, get_branch_config, BRANCH_DISPLAY_NAMES, get_branch_address

# -------------------- TEMPLATES --------------------
templates = Jinja2Templates(directory="templates")

# -------------------- DATABASE INIT --------------------
models.Base.metadata.create_all(bind=engine)

# -------------------- APP INIT --------------------
app = FastAPI()

# -------------------- CORS - UPDATED --------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*", "Content-Disposition"],
)

# -------------------- USER SCHEMA --------------------
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "client"

# -------------------- BRANCH RESPONSE SCHEMA - FIXED --------------------
class BranchResponse(BaseModel):
    branch_code: str
    branch_name: str
    office_name: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    branch_state: Optional[str] = None
    zipcode: Optional[str] = None
    tel: Optional[str] = None  # Keep tel for frontend compatibility
    fax: Optional[str] = None  # Keep fax for frontend compatibility

# -------------------- PASSWORD RESET SCHEMAS --------------------
class ForgotPasswordRequest(BaseModel):
    username: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

# -------------------- IN-MEMORY TOKEN STORAGE (FOR DEVELOPMENT) --------------------
# In production, use a database table
reset_tokens = {}

# -------------------- AUTH --------------------
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(
        username=user.username,
        hashed_password=auth.get_password_hash(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    return {"message": "Account created successfully"}


@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(data={"sub": user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role
    }

# -------------------- FORGOT PASSWORD ENDPOINT --------------------
@app.post("/forgot-password")
def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.email).first()

    if user:
        reset_token = secrets.token_urlsafe(32)
        reset_tokens[reset_token] = {
            "user_id": user.id,
            "username": user.username,
            "expires_at": datetime.now() + timedelta(hours=24),
            "used": False
        }

        # CALL THE FUNCTION FROM UTILS.PY
        send_reset_email(user.username, reset_token)

    return {"message": "If your email exists, you will receive a link."}
# -------------------- RESET PASSWORD ENDPOINT --------------------
@app.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password using token"""
    try:
        # Check if token exists
        if request.token not in reset_tokens:
            raise HTTPException(status_code=400, detail="Invalid or expired reset token")
        
        token_data = reset_tokens[request.token]
        
        # Check if expired
        if token_data["expires_at"] < datetime.now():
            del reset_tokens[request.token]
            raise HTTPException(status_code=400, detail="Token has expired")
        
        # Check if already used
        if token_data["used"]:
            del reset_tokens[request.token]
            raise HTTPException(status_code=400, detail="Token already used")
        
        # Find user
        user = db.query(models.User).filter(models.User.id == token_data["user_id"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update password
        user.hashed_password = auth.get_password_hash(request.new_password)
        
        # Mark token as used
        token_data["used"] = True
        
        db.commit()
        
        print(f"Password reset successful for: {user.username}")
        
        # Clean up used token
        del reset_tokens[request.token]
        
        return {"message": "Password reset successful"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in reset-password: {e}")
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")



    
    
# -------------------- AGREEMENT FORM PAGE --------------------
@app.get("/agreement-form", response_class=HTMLResponse)
async def agreement_form(request: Request):
    """Render the agreement form with branch dropdown populated"""
    branch_options = get_branch_options()
    return templates.TemplateResponse(
        "agreement_form.html", 
        {
            "request": request, 
            "branch_options": branch_options,
            "today": datetime.now().strftime("%Y-%m-%d")
        }
    )

# -------------------- AGREEMENTS --------------------
@app.get("/agreements", response_model=List[schemas.Agreement])
def list_agreements(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "agent":
        return db.query(models.Agreement).all()
    
    return db.query(models.Agreement).filter(
        models.Agreement.owner_id == current_user.id
    ).all()
    
@app.post("/agreements", response_model=schemas.Agreement)
def create_agreement(
    agreement: schemas.AgreementCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    agreement_data = agreement.model_dump(exclude_unset=True)

    agreement_data["owner_id"] = current_user.id
    agreement_data["client_sign_date"] = datetime.now().date()
    agreement_data["status"] = "Pending"

    # Check if branch exists in database
    branch = db.query(models.Branch).filter(
        models.Branch.branch_code == agreement.branch_code
    ).first()

    # If branch not in database, still allow it if it's in our branch_config
    if not branch:
        # Try to get branch config to validate
        try:
            # Use a default state code or get from agreement
            state_code = getattr(agreement, 'state_code', 'MD')
            config = get_branch_config(agreement.branch_code, state_code)
            # Branch is valid in config, proceed
            print(f"Branch {agreement.branch_code} found in config, continuing...")
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid branch code: {agreement.branch_code}"
            )

    new_agreement = models.Agreement(**agreement_data)

    db.add(new_agreement)
    db.commit()
    db.refresh(new_agreement)

    return new_agreement

# -------------------- AGREEMENT PDF --------------------
@app.get("/agreements/{agreement_id}/pdf")
def download_agreement_pdf(
    agreement_id: int,
    current_user: models.User = Depends(get_current_user),     
    db: Session = Depends(get_db)
):
    # Set CORS headers for all responses
    cors_headers = {
        "Access-Control-Allow-Origin": "http://localhost:5173",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Authorization, Content-Type",
        "Access-Control-Allow-Credentials": "true",
    }
    
    try:
        # 1. Fetch agreement
        query = db.query(models.Agreement).filter(models.Agreement.id == agreement_id)
        if current_user.role != "agent":
            query = query.filter(models.Agreement.owner_id == current_user.id)

        agreement = query.first()
        if not agreement:
            return JSONResponse(
                status_code=404,
                content={"detail": "Agreement not found"},
                headers=cors_headers
            )

        # 2. Fetch branch with a safety check
        branch = db.query(models.Branch).filter(
            models.Branch.branch_code == agreement.branch_code
        ).first()
        
        if not branch:
            # Try to get branch info from config
            addr = get_branch_address(agreement.branch_code)
            branch_state = 'MD'
            office_name = addr['office_name']
            street = addr['address_line_1']
            city = addr['city']
            zipcode = addr['zip_code']
            branch_phone = addr['tel']
            branch_fax = addr['fax']
            
            # Extract state from display name
            import re
            display_name = BRANCH_DISPLAY_NAMES.get(agreement.branch_code, "")
            state_match = re.search(r'\(([A-Z]{2})\)', display_name)
            branch_state = state_match.group(1) if state_match else 'MD'
            
            print(f"Branch {agreement.branch_code} not found in database, using config defaults")
        else:
            # Use actual tblbranch column names
            branch_state = branch.branch_state or 'MD'
            office_name = branch.office_name or "Options For Senior America"
            street = branch.street or branch.address_line_1 or ""
            city = branch.city or ""
            zipcode = branch.zipcode or branch.zip_code or ""
            branch_phone = branch.branch_phone or ""
            branch_fax = branch.branch_fax or branch.fax or ""
        
        # 3. Create PDF data with all fields
        pdf_data = {
            "branch_code": agreement.branch_code,
            "office_name": office_name,
            "address_line_1": street,
            "address_line_2": "",
            "city": city,
            "state_code": branch_state,
            "zip_code": zipcode,
            "tel": branch_phone,
            "fax": branch_fax,
            
            # Client information
            "clt_title": agreement.clt_title or "",
            "clt_first_name": agreement.clt_first_name,
            "clt_last_name": agreement.clt_last_name,
            "clt_address": agreement.clt_address,
            "clt_city": agreement.clt_city,
            "clt_state": agreement.clt_state,
            "clt_zip": agreement.clt_zip,
            "clt_relationship": agreement.clt_relationship,
            "responsible_party": agreement.responsible_party or f"{agreement.clt_first_name} {agreement.clt_last_name}",

            # Care recipient information
            "care_title": agreement.care_title or "",
            "care_first_name": agreement.care_first_name,
            "care_last_name": agreement.care_last_name,
            "care_recipient_address": agreement.care_recipient_address or "",
            "care_city": agreement.care_city or "",
            "care_state": agreement.care_state,
            "care_zip": agreement.care_zip or "",

            # Service information
            "initial_inquiry_date": agreement.initial_inquiry_date.strftime("%m/%d/%Y") if agreement.initial_inquiry_date else "",
            "agreement_date": agreement.agreement_date.strftime("%m/%d/%Y") if agreement.agreement_date else "",
            "start_date": agreement.start_date.strftime("%m/%d/%Y") if agreement.start_date else "",
            "services_start_time": agreement.services_start_time or "",
            "instructions_given_by": agreement.instructions_given_by or "",
            "handled_by": agreement.handled_by or "",
            "frequency_duration": agreement.frequency_duration or "",
            "care_type": agreement.care_type,
            "is_live_in": str(agreement.is_live_in).lower(),
            "hourly_rate": f"{float(agreement.hourly_rate):.2f}",
            "mileage_rate": f"{float(agreement.mileage_rate):.2f}",
            "vehicle_authorized": str(agreement.vehicle_authorized).lower(),
            "vehicle_authorization_initials": agreement.vehicle_authorization_initials or "",
            "PercCharged": str(getattr(agreement, 'perc_charged', '100')),
            "hazards": getattr(agreement, 'hazards', 'None Reported'),
            
            # Payment/Banking information
            "bank_name": agreement.bank_name or "",
            "bank_city": agreement.bank_city or "",
            "bank_state": agreement.bank_state or "",
            "routing_number": agreement.routing_number or "",
            "account_number": agreement.account_number or "",
            "account_type": agreement.account_type or "Checking",
            
            # Signatures
            "client_signature": agreement.client_signature or "",
        }

        # Generate PDF
        pdf_stream = json_to_pdf(pdf_data)
        filename = f"Agreement_{agreement.clt_last_name}.pdf"
        
        # Return PDF with CORS headers
        return StreamingResponse(
            pdf_stream,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Access-Control-Allow-Origin": "http://localhost:5173",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Authorization, Content-Type",
                "Access-Control-Allow-Credentials": "true",
            }
        )
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"PDF Generation Error: {e}")
        print(f"Full traceback: {error_trace}")
        
        # Return error with CORS headers
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal PDF Generation Error: {str(e)}"},
            headers={
                "Access-Control-Allow-Origin": "http://localhost:5173",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Authorization, Content-Type",
                "Access-Control-Allow-Credentials": "true",
            }
        )

# -------------------- BRANCHES API - SHOW ALL BRANCHES --------------------
@app.get("/branches")
def get_branches(db: Session = Depends(get_db)):
    """Get all branches from database"""
    try:
        # Get all branches from database
        branches = db.query(models.Branch).all()
        print(f"Found {len(branches)} branches in database")
        
        result = []
        for branch in branches:
            # Skip if no branch_code (shouldn't happen)
            if not branch.branch_code:
                continue
                
            # Get display name from config, fallback to branch_name or branch_code
            display_name = BRANCH_DISPLAY_NAMES.get(branch.branch_code)
            if not display_name:
                display_name = branch.branch_name or branch.branch_code
                print(f"Warning: No display name for {branch.branch_code}, using '{display_name}'")
            
            # Use actual tblbranch column names
            branch_state = branch.branch_state or 'MD'
            office_name = branch.office_name or "Options For Senior America"
            street = branch.street or branch.address_line_1 or ""
            # Handle address_line_2 if it exists (some branches have it)
            street_full = street
            if branch.address_line_2:
                street_full = f"{street}, {branch.address_line_2}" if street else branch.address_line_2
                
            city = branch.city or ""
            zipcode = branch.zipcode or branch.zip_code or ""
            branch_phone = branch.branch_phone or ""
            branch_fax = branch.branch_fax or branch.fax or ""
            
            result.append({
                "branch_code": branch.branch_code,
                "branch_name": display_name,
                "office_name": office_name,
                "street": street_full,
                "city": city,
                "branch_state": branch_state,
                "zipcode": zipcode,
                "tel": branch_phone,
                "fax": branch_fax
            })
        
        # Sort by branch_name
        result.sort(key=lambda x: x["branch_name"])
        print(f"Returning {len(result)} branches to frontend")
        return result
        
    except Exception as e:
        print(f"Error fetching branches: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)},
            headers={
                "Access-Control-Allow-Origin": "http://localhost:5173",
            }
        )

# -------------------- BRANCH SYNC API --------------------
@app.post("/branches/sync")
def sync_branches(db: Session = Depends(get_db)):
    """Sync branches from config to database"""
    from branch_config import BRANCH_DISPLAY_NAMES, get_branch_address
    import re
    
    results = {
        "created": [],
        "updated": [],
        "total": 0
    }
    
    for code, display_name in BRANCH_DISPLAY_NAMES.items():
        # Check if branch exists
        branch = db.query(models.Branch).filter(
            models.Branch.branch_code == code
        ).first()
        
        # Get address
        addr = get_branch_address(code)
        
        # Extract state from display name
        state_match = re.search(r'\(([A-Z]{2})\)', display_name)
        state_code = state_match.group(1) if state_match else 'MD'
        
        if branch:
            # Update existing - use tblbranch column names
            branch.office_name = addr['office_name']
            branch.street = addr['address_line_1']
            branch.city = addr['city']
            branch.branch_state = state_code
            branch.zipcode = addr['zip_code']
            branch.branch_phone = addr['tel']
            branch.branch_fax = addr['fax']
            results["updated"].append(code)
        else:
            # Create new - use tblbranch column names
            new_branch = models.Branch(
                branch_code=code,
                branch_name=display_name,
                office_name=addr['office_name'],
                street=addr['address_line_1'],
                city=addr['city'],
                branch_state=state_code,
                zipcode=addr['zip_code'],
                branch_phone=addr['tel'],
                branch_fax=addr['fax'],
                # Set default values for required fields
                responsible_title=None,
                care_coordinator_name=None,
                mileage=None,
                admin_meds=False,
                corp_state_long=None,
                office_phone_corp=None,
                fein=None,
                is_corporate=False
            )
            db.add(new_branch)
            results["created"].append(code)
    
    db.commit()
    results["total"] = len(results["created"]) + len(results["updated"])
    
    return {
        "message": "Branches synced successfully",
        "results": results
    }

# -------------------- BRANCH CONFIG API --------------------
@app.get("/branch-config/{branch_code}")
def get_branch_config_api(branch_code: str, state_code: str = "MD"):
    """Get configuration for a specific branch"""
    try:
        config = get_branch_config(branch_code, state_code)
        return config
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Branch config not found: {str(e)}")

# -------------------- HEALTH --------------------
@app.get("/health")
def health():
    return {"status": "online", "timestamp": datetime.now()}