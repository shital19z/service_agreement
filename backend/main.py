from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Optional
from datetime import datetime, timedelta
import secrets
import os
import re  
from email_config import send_reset_email

from config import Config
from sqlalchemy import text
import json

from sqlalchemy.orm import Session
from pydantic import BaseModel

import models
import schemas
import auth
from database import engine, get_db, SessionLocal
from auth import get_current_user, authenticate_user, create_access_token
from pdf_generator import json_to_pdf
from branch_config import get_branch_options, get_branch_config, BRANCH_DISPLAY_NAMES, get_branch_address

# ===== AUTO-SEED FUNCTION =====
def ensure_branches_exist():
    """Automatically seed branches if none exist"""
    db = SessionLocal()
    try:
        existing_count = db.query(models.Branch).count()
        print(f"Database check: {existing_count} branches found")
        
        if existing_count == 0:
            print("No branches found. Auto-seeding from config...")
            created_count = 0
            
            for code, display_name in BRANCH_DISPLAY_NAMES.items():
                addr = get_branch_address(code)
                state_match = re.search(r'\(([A-Z]{2})\)', display_name)
                state_code = state_match.group(1) if state_match else 'MD'
                
                default_mileage = 0.67
                if code == 'dchomecare':
                    default_mileage = 0.70
                
                branch = models.Branch(
                    branch_code=code,
                    branch_name=display_name,
                    office_name=addr['office_name'],
                    street=addr['address_line_1'],
                    city=addr['city'],
                    branch_state=state_code,
                    zipcode=addr['zip_code'],
                    branch_phone=addr['tel'],
                    branch_fax=addr['fax'],
                    mileage=default_mileage,
                    responsible_title=None,
                    care_coordinator_name=None,
                    admin_meds=False,
                    corp_state_long=None,
                    office_phone_corp=None,
                    fein=None,
                    is_corporate=False
                )
                db.add(branch)
                created_count += 1
                print(f"Auto-seeded: {code} - {display_name}")
            
            db.commit()
            print(f"Success! Added {created_count} branches automatically.")
        else:
            print(f"Branches already exist. No action needed.")
            branches_without_mileage = db.query(models.Branch).filter(
                models.Branch.mileage == None
            ).count()
            if branches_without_mileage > 0:
                print(f"⚠️  Warning: {branches_without_mileage} branches have no mileage set. Using default 0.67.")
                
    except Exception as e:
        print(f"Error auto-seeding branches: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

# -------------------- TEMPLATES --------------------
templates = Jinja2Templates(directory="templates")

# -------------------- DATABASE INIT --------------------
models.Base.metadata.create_all(bind=engine)

# -------------------- APP INIT --------------------
app = FastAPI()

# ===== CALL AUTO-SEED AT STARTUP =====
ensure_branches_exist()

# -------------------- CORS --------------------
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
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*", "Content-Disposition"],
)

# ===== OPTIONS HANDLERS =====
@app.options("/agreements")
async def agreements_options():
    return JSONResponse(content={"message": "OK"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173","Access-Control-Allow-Methods": "GET, POST, OPTIONS","Access-Control-Allow-Headers": "Authorization, Content-Type, Accept","Access-Control-Allow-Credentials": "true","Access-Control-Max-Age": "3600"})

@app.options("/agreements/{agreement_id}")
async def agreement_options():
    return JSONResponse(content={"message": "OK"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173","Access-Control-Allow-Methods": "GET, PUT, PATCH, DELETE, OPTIONS","Access-Control-Allow-Headers": "Authorization, Content-Type, Accept","Access-Control-Allow-Credentials": "true","Access-Control-Max-Age": "3600"})

@app.options("/agreements/{agreement_id}/pdf")
async def agreement_pdf_options():
    return JSONResponse(content={"message": "OK"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173","Access-Control-Allow-Methods": "GET, OPTIONS","Access-Control-Allow-Headers": "Authorization, Content-Type, Accept","Access-Control-Allow-Credentials": "true","Access-Control-Max-Age": "3600"})

@app.options("/branches")
async def branches_options():
    return JSONResponse(content={"message": "OK"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173","Access-Control-Allow-Methods": "GET, POST, OPTIONS","Access-Control-Allow-Headers": "Authorization, Content-Type, Accept","Access-Control-Allow-Credentials": "true","Access-Control-Max-Age": "3600"})

@app.options("/branches/{branch_code}")
async def branch_options():
    return JSONResponse(content={"message": "OK"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173","Access-Control-Allow-Methods": "GET, PUT, DELETE, OPTIONS","Access-Control-Allow-Headers": "Authorization, Content-Type, Accept","Access-Control-Allow-Credentials": "true","Access-Control-Max-Age": "3600"})

@app.options("/branches/{branch_code}/content")
async def branch_content_options():
    return JSONResponse(content={"message": "OK"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173","Access-Control-Allow-Methods": "GET, PUT, OPTIONS","Access-Control-Allow-Headers": "Authorization, Content-Type, Accept","Access-Control-Allow-Credentials": "true","Access-Control-Max-Age": "3600"})

@app.options("/branches/copy-content")
async def copy_content_options():
    return JSONResponse(content={"message": "OK"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173","Access-Control-Allow-Methods": "POST, OPTIONS","Access-Control-Allow-Headers": "Authorization, Content-Type, Accept","Access-Control-Allow-Credentials": "true","Access-Control-Max-Age": "3600"})

# ===== DEBUG ENDPOINT =====
@app.get("/debug-auth")
def debug_auth(current_user: models.User = Depends(get_current_user)):
    return JSONResponse(
        content={"authenticated": True, "user_id": current_user.id, "username": current_user.username, "role": current_user.role},
        headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"}
    )

# -------------------- USER SCHEMA --------------------
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "client"

# -------------------- BRANCH MANAGEMENT SCHEMAS --------------------
class BranchCreate(BaseModel):
    branch_code: str
    branch_name: str
    office_name: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    branch_state: Optional[str] = None
    zipcode: Optional[str] = None
    branch_phone: Optional[str] = None
    branch_fax: Optional[str] = None
    mileage: Optional[float] = 0.67
    admin_meds: bool = False
    is_corporate: bool = False

class CopyContentRequest(BaseModel):
    source_branch: str
    target_branches: List[str]
    content_types: dict

class BranchResponse(BaseModel):
    branch_code: str
    branch_name: str
    office_name: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    branch_state: Optional[str] = None
    zipcode: Optional[str] = None
    tel: Optional[str] = None
    fax: Optional[str] = None

class ForgotPasswordRequest(BaseModel):
    username: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

# -------------------- IN-MEMORY TOKEN STORAGE --------------------
reset_tokens = {}

# -------------------- AUTH --------------------
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == user.username).first():
        return JSONResponse(status_code=400, content={"detail": "Username already exists"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
    new_user = models.User(username=user.username, hashed_password=auth.get_password_hash(user.password), role=user.role)
    db.add(new_user)
    db.commit()
    return JSONResponse(content={"message": "Account created successfully"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return JSONResponse(status_code=401, content={"detail": "Incorrect username or password"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
    token = create_access_token(data={"sub": user.username})
    print(f"Login successful for user: {user.username}, token created")
    return JSONResponse(content={"access_token": token, "token_type": "bearer", "username": user.username, "role": user.role}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

# -------------------- FORGOT PASSWORD --------------------
@app.post("/forgot-password")
def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.email).first()
    if user:
        reset_token = secrets.token_urlsafe(32)
        reset_tokens[reset_token] = {"user_id": user.id, "username": user.username, "expires_at": datetime.now() + timedelta(hours=24), "used": False}
        send_reset_email(user.username, reset_token)
    return JSONResponse(content={"message": "If your email exists, you will receive a link."}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

# -------------------- RESET PASSWORD --------------------
@app.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        if request.token not in reset_tokens:
            return JSONResponse(status_code=400, content={"detail": "Invalid or expired reset token"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        token_data = reset_tokens[request.token]
        if token_data["expires_at"] < datetime.now():
            del reset_tokens[request.token]
            return JSONResponse(status_code=400, content={"detail": "Token has expired"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        if token_data["used"]:
            del reset_tokens[request.token]
            return JSONResponse(status_code=400, content={"detail": "Token already used"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        user = db.query(models.User).filter(models.User.id == token_data["user_id"]).first()
        if not user:
            return JSONResponse(status_code=404, content={"detail": "User not found"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        user.hashed_password = auth.get_password_hash(request.new_password)
        token_data["used"] = True
        db.commit()
        print(f"Password reset successful for: {user.username}")
        del reset_tokens[request.token]
        return JSONResponse(content={"message": "Password reset successful"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
    except Exception as e:
        print(f"Error in reset-password: {e}")
        return JSONResponse(status_code=400, content={"detail": "Invalid or expired reset token"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

# -------------------- AGREEMENT FORM PAGE --------------------
@app.get("/agreement-form", response_class=HTMLResponse)
async def agreement_form(request: Request):
    branch_options = get_branch_options()
    return templates.TemplateResponse("agreement_form.html", {"request": request, "branch_options": branch_options, "today": datetime.now().strftime("%Y-%m-%d")})

# -------------------- AGREEMENTS --------------------
@app.get("/agreements")
def list_agreements(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        print(f"Listing agreements for user: {current_user.username} (role: {current_user.role})")
        if current_user.role == "agent":
            agreements = db.query(models.Agreement).all()
        else:
            agreements = db.query(models.Agreement).filter(models.Agreement.owner_id == current_user.id).all()
        print(f"Found {len(agreements)} agreements")
        agreements_list = []
        for agreement in agreements:
            agreement_dict = {
                "id": agreement.id, "clt_first_name": agreement.clt_first_name, "clt_last_name": agreement.clt_last_name,
                "branch_code": agreement.branch_code, "hourly_rate": agreement.hourly_rate, "care_type": agreement.care_type,
                "status": agreement.status, "owner_id": agreement.owner_id,
                "agreement_date": agreement.agreement_date.isoformat() if agreement.agreement_date else None,
                "start_date": agreement.start_date.isoformat() if agreement.start_date else None,
                "client_sign_date": agreement.client_sign_date.isoformat() if agreement.client_sign_date else None,
            }
            if hasattr(agreement, 'created_at') and agreement.created_at:
                agreement_dict["created_at"] = agreement.created_at.isoformat()
            if hasattr(agreement, 'updated_at') and agreement.updated_at:
                agreement_dict["updated_at"] = agreement.updated_at.isoformat()
            agreements_list.append(agreement_dict)
        return JSONResponse(content=agreements_list, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
    except Exception as e:
        print(f"Error in list_agreements: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

@app.post("/agreements")
def create_agreement(agreement: schemas.AgreementCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        agreement_data = agreement.model_dump(exclude_unset=True)
        agreement_data["owner_id"] = current_user.id
        agreement_data["client_sign_date"] = datetime.now().date()
        agreement_data["status"] = "Pending"
        branch = db.query(models.Branch).filter(models.Branch.branch_code == agreement.branch_code).first()
        if not branch:
            try:
                state_code = getattr(agreement, 'state_code', 'MD')
                config = get_branch_config(agreement.branch_code, state_code)
                print(f"Branch {agreement.branch_code} found in config, continuing...")
            except Exception as e:
                return JSONResponse(status_code=400, content={"detail": f"Invalid branch code: {agreement.branch_code}"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        new_agreement = models.Agreement(**agreement_data)
        db.add(new_agreement)
        db.commit()
        db.refresh(new_agreement)
        print(f"Agreement created with ID: {new_agreement.id}")
        return JSONResponse(content={"id": new_agreement.id, "clt_first_name": new_agreement.clt_first_name, "clt_last_name": new_agreement.clt_last_name, "branch_code": new_agreement.branch_code, "status": new_agreement.status, "message": "Agreement created successfully"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
    except Exception as e:
        print(f"Error creating agreement: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

# -------------------- GET SINGLE AGREEMENT --------------------
@app.get("/agreements/{agreement_id}")
def get_agreement(agreement_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        query = db.query(models.Agreement).filter(models.Agreement.id == agreement_id)
        if current_user.role != "agent":
            query = query.filter(models.Agreement.owner_id == current_user.id)
        agreement = query.first()
        if not agreement:
            return JSONResponse(status_code=404, content={"detail": "Agreement not found"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        agreement_dict = {
            "id": agreement.id, "clt_title": agreement.clt_title, "clt_first_name": agreement.clt_first_name,
            "clt_last_name": agreement.clt_last_name, "clt_address": agreement.clt_address, "clt_city": agreement.clt_city,
            "clt_state": agreement.clt_state, "clt_zip": agreement.clt_zip, "clt_relationship": agreement.clt_relationship,
            "care_title": agreement.care_title, "care_first_name": agreement.care_first_name, "care_last_name": agreement.care_last_name,
            "care_recipient_address": agreement.care_recipient_address, "care_city": agreement.care_city,
            "care_state": agreement.care_state, "care_zip": agreement.care_zip, "branch_code": agreement.branch_code,
            "initial_inquiry_date": agreement.initial_inquiry_date.isoformat() if agreement.initial_inquiry_date else None,
            "agreement_date": agreement.agreement_date.isoformat() if agreement.agreement_date else None,
            "start_date": agreement.start_date.isoformat() if agreement.start_date else None,
            "services_start_time": agreement.services_start_time, "care_type": agreement.care_type,
            "hourly_rate": agreement.hourly_rate,
            "inicontactdate": agreement.inicontactdate.isoformat() if agreement.inicontactdate else None,
            "date_of_order": agreement.date_of_order.isoformat() if agreement.date_of_order else None,
            "required_services": agreement.required_services, "freq_of_visit": agreement.freq_of_visit,
            "hazards": agreement.hazards, "perc_charged": agreement.perc_charged, "handled_by": agreement.handled_by,
            "status": agreement.status, "owner_id": agreement.owner_id,
            "client_sign_date": agreement.client_sign_date.isoformat() if agreement.client_sign_date else None,
            "instructions_given_by": agreement.instructions_given_by,
        }
        return JSONResponse(content=agreement_dict, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
    except Exception as e:
        print(f"Error fetching agreement: {e}")
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

# -------------------- UPDATE AGREEMENT --------------------
@app.put("/agreements/{agreement_id}")
def update_agreement(agreement_id: int, agreement: schemas.AgreementCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        query = db.query(models.Agreement).filter(models.Agreement.id == agreement_id)
        if current_user.role != "agent":
            query = query.filter(models.Agreement.owner_id == current_user.id)
        existing_agreement = query.first()
        if not existing_agreement:
            return JSONResponse(status_code=404, content={"detail": "Agreement not found"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        update_data = agreement.model_dump(exclude_unset=True)
        update_data = {k: v for k, v in update_data.items() if v != "string"}
        for key, value in update_data.items():
            if hasattr(existing_agreement, key):
                setattr(existing_agreement, key, value)
        db.commit()
        db.refresh(existing_agreement)
        return JSONResponse(content={"id": existing_agreement.id, "message": "Agreement updated successfully"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

@app.patch("/agreements/{agreement_id}")
def patch_agreement(agreement_id: int, agreement: dict, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        query = db.query(models.Agreement).filter(models.Agreement.id == agreement_id)
        if current_user.role != "agent":
            query = query.filter(models.Agreement.owner_id == current_user.id)
        existing_agreement = query.first()
        if not existing_agreement:
            return JSONResponse(status_code=404, content={"detail": "Agreement not found"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        clean_data = {k: v for k, v in agreement.items() if v != "string"}
        for key, value in clean_data.items():
            if hasattr(existing_agreement, key):
                setattr(existing_agreement, key, value)
        db.commit()
        db.refresh(existing_agreement)
        print(f"✅ Agreement {agreement_id} partially updated with fields: {list(clean_data.keys())}")
        return JSONResponse(content={"id": existing_agreement.id, "message": "Agreement updated successfully", "updated_fields": list(clean_data.keys())}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
    except Exception as e:
        print(f"❌ Error in patch_agreement: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

# ===== SHARE FUNCTIONALITY ENDPOINTS =====
@app.post("/agreements/{agreement_id}/share-link")
def generate_share_link(agreement_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        query = db.query(models.Agreement).filter(models.Agreement.id == agreement_id)
        if current_user.role != "agent":
            query = query.filter(models.Agreement.owner_id == current_user.id)
        agreement = query.first()
        if not agreement:
            return JSONResponse(status_code=404, content={"detail": "Agreement not found"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(days=7)
        shared = models.SharedAgreement(token=token, agreement_id=agreement_id, created_by=current_user.id, expires_at=expires_at, views=0, is_active=True)
        db.add(shared)
        db.commit()
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        share_link = f"{frontend_url}/shared-agreement/{token}"
        return JSONResponse(content={"share_link": share_link, "token": token}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
    except Exception as e:
        print(f"Error generating share link: {e}")
        db.rollback()
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

@app.post("/agreements/{agreement_id}/share-email")
def share_via_email(agreement_id: int, request: dict, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        email = request.get('email')
        if not email:
            return JSONResponse(status_code=400, content={"detail": "Email is required"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        query = db.query(models.Agreement).filter(models.Agreement.id == agreement_id)
        if current_user.role != "agent":
            query = query.filter(models.Agreement.owner_id == current_user.id)
        agreement = query.first()
        if not agreement:
            return JSONResponse(status_code=404, content={"detail": "Agreement not found"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(days=7)
        shared = models.SharedAgreement(token=token, agreement_id=agreement_id, created_by=current_user.id, expires_at=expires_at, views=0, is_active=True)
        db.add(shared)
        db.commit()
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        share_link = f"{frontend_url}/shared-agreement/{token}"
        client_name = f"{agreement.clt_first_name} {agreement.clt_last_name}".strip()
        from email_config import send_share_email
        email_sent = send_share_email(email, share_link, client_name)
        if not email_sent:
            return JSONResponse(content={"message": "Link generated but email delivery failed. You can copy the link manually.", "share_link": share_link, "email_status": "failed"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        return JSONResponse(content={"message": f"Share link sent to {email}", "email_status": "sent"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
    except Exception as e:
        print(f"Error sharing via email: {e}")
        db.rollback()
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

# -------------------- AGREEMENT PDF --------------------
@app.get("/agreements/{agreement_id}/pdf")
def download_agreement_pdf(agreement_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    cors_headers = {"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Methods": "GET, POST, OPTIONS", "Access-Control-Allow-Headers": "Authorization, Content-Type", "Access-Control-Allow-Credentials": "true"}
    try:
        query = db.query(models.Agreement).filter(models.Agreement.id == agreement_id)
        if current_user.role != "agent":
            query = query.filter(models.Agreement.owner_id == current_user.id)
        agreement = query.first()
        if not agreement:
            return JSONResponse(status_code=404, content={"detail": "Agreement not found"}, headers=cors_headers)

        branch = db.query(models.Branch).filter(models.Branch.branch_code == agreement.branch_code).first()
        branch_mileage = 0.67
        if branch and hasattr(branch, 'mileage') and branch.mileage:
            branch_mileage = float(branch.mileage)
            print(f"Using branch mileage: {branch_mileage} for {agreement.branch_code}")
        branch_data = {}
        if branch:
            branch_data = {"Mileage": branch_mileage, "branch_code": branch.branch_code, "office_name": getattr(branch, 'office_name', '')}

        if not branch:
            from branch_config import get_branch_address, BRANCH_DISPLAY_NAMES
            import re
            addr = get_branch_address(agreement.branch_code)
            branch_state = 'MD'
            office_name = addr['office_name']
            street = addr['address_line_1']
            city = addr['city']
            zipcode = addr['zip_code']
            branch_phone = addr['tel']
            branch_fax = addr['fax']
            display_name = BRANCH_DISPLAY_NAMES.get(agreement.branch_code, "")
            state_match = re.search(r'\(([A-Z]{2})\)', display_name)
            branch_state = state_match.group(1) if state_match else 'MD'
            print(f"Branch {agreement.branch_code} not found in database, using config defaults")
        else:
            branch_state = branch.branch_state or 'MD'
            office_name = branch.office_name or "Options For Senior America"
            street = branch.street or getattr(branch, 'address_line_1', '') or ""
            city = branch.city or ""
            zipcode = branch.zipcode or getattr(branch, 'zip_code', '') or ""
            branch_phone = branch.branch_phone or ""
            branch_fax = branch.branch_fax or getattr(branch, 'fax', '') or ""

        # ── Read branch_content from DB (Edit Content saves here) ─────────────
        branch_content_row = db.execute(
            text("SELECT content_data FROM branch_content WHERE branch_code = :code AND content_type = 'agreement'"),
            {"code": agreement.branch_code}
        ).first()
        branch_content = branch_content_row[0] if branch_content_row else {}
        if isinstance(branch_content, str):
            branch_content = json.loads(branch_content)
        print(f"[PDF] branch={agreement.branch_code} content_keys={list(branch_content.keys())}")
        # ─────────────────────────────────────────────────────────────────────

        logo_path = Config.get_logo_path()
        if not logo_path:
            logo_path = ""

        pdf_data = {
            "branch_code": agreement.branch_code,
            "branch_data": branch_data,
            "office_name": office_name,
            "address_line_1": street,
            "address_line_2": "",
            "city": city,
            "state_code": branch_state,
            "zip_code": zipcode,
            "tel": branch_phone,
            "fax": branch_fax,
            "clt_title": agreement.clt_title or "",
            "clt_first_name": agreement.clt_first_name,
            "clt_last_name": agreement.clt_last_name,
            "clt_address": agreement.clt_address,
            "clt_city": agreement.clt_city,
            "clt_state": agreement.clt_state,
            "clt_zip": agreement.clt_zip,
            "clt_relationship": agreement.clt_relationship,
            "responsible_party": agreement.responsible_party or f"{agreement.clt_first_name} {agreement.clt_last_name}",
            "care_title": agreement.care_title or "",
            "care_first_name": agreement.care_first_name,
            "care_last_name": agreement.care_last_name,
            "care_recipient_address": agreement.care_recipient_address or "",
            "care_city": agreement.care_city or "",
            "care_state": agreement.care_state,
            "care_zip": agreement.care_zip or "",
            "initial_inquiry_date": agreement.initial_inquiry_date.strftime("%m/%d/%Y") if agreement.initial_inquiry_date else "",
            "agreement_date": agreement.agreement_date.strftime("%m/%d/%Y") if agreement.agreement_date else "",
            "start_date": agreement.start_date.strftime("%m/%d/%Y") if agreement.start_date else "",
            "services_start_time": agreement.services_start_time or "",
            "instructions_given_by": agreement.instructions_given_by or "",
            "handled_by": agreement.handled_by or "",
            "frequency_duration": agreement.frequency_duration or "",
            "care_type": branch_content.get('care_type', agreement.care_type or "Home Care"),
            "is_live_in": str(agreement.is_live_in).lower(),
            "hourly_rate": f"{float(agreement.hourly_rate):.2f}",
            "mileage_rate": f"{branch_mileage:.2f}",
            "vehicle_authorized": str(agreement.vehicle_authorized).lower(),
            "vehicle_authorization_initials": agreement.vehicle_authorization_initials or "",
            # ✅ FIX: both key names for perc_charged
            "PercCharged": str(getattr(agreement, 'perc_charged', '100')),
            "perc_charged": str(getattr(agreement, 'perc_charged', '100')),
            "hazards":           getattr(agreement, 'hazards', None) or branch_content.get('hazards', 'None Reported'),
            "required_services": getattr(agreement, 'required_services', None) or branch_content.get('required_services', ''),
            "freq_of_visit":     getattr(agreement, 'freq_of_visit', None) or branch_content.get('freq_of_visit', ''),
            "inicontactdate": agreement.inicontactdate.strftime("%m/%d/%Y") if hasattr(agreement, 'inicontactdate') and agreement.inicontactdate else "",
            "date_of_order": agreement.date_of_order.strftime("%m/%d/%Y") if hasattr(agreement, 'date_of_order') and agreement.date_of_order else "",
            "page1_cont_signature": getattr(agreement, 'page1_cont_signature', ''),
            "page3_1_signature": getattr(agreement, 'page3_1_signature', ''),
            "bank_name": agreement.bank_name or "",
            "bank_city": agreement.bank_city or "",
            "bank_state": agreement.bank_state or "",
            "routing_number": agreement.routing_number or "",
            "account_number": agreement.account_number or "",
            "account_type": agreement.account_type or "Checking",
            "client_signature": agreement.client_signature or "",
            "logo_path": logo_path,
            # ── All Edit Content fields ───────────────────────────────────────
            "required_services_intro":      branch_content.get('required_services', ''),
            "notice_period_text":           branch_content.get('notice_period_text', ''),
            "needs_assessment_text":        branch_content.get('needs_assessment_text', ''),
            "valuables_text":               branch_content.get('valuables_text', ''),
            "medication_text":              branch_content.get('medication_text', ''),
            "cannot_hire_text":             branch_content.get('cannot_hire_text', ''),
            "record_keeping_text":          branch_content.get('record_keeping_text', ''),
            "mileage_reimbursement_text":   branch_content.get('mileage_reimbursement_text', ''),
            "vehicle_use_text":             branch_content.get('vehicle_use_text', ''),
            "payment_obligations_text":     branch_content.get('payment_obligations_text', ''),
            "patients_rights_text":         branch_content.get('patients_rights_text', ''),
            "complaint_procedures_text":    branch_content.get('complaint_procedures_text', ''),
            "billing_procedures_text":      branch_content.get('billing_procedures_text', ''),
            "eft_authorization_text":       branch_content.get('eft_authorization_text', ''),
            "consumer_notice_text":         branch_content.get('consumer_notice_text', ''),
            "holiday_count":                branch_content.get('holiday_count', 11),
            "has_initial_contact":          branch_content.get('has_initial_contact', False),
            "requires_consumer_notice":     branch_content.get('requires_consumer_notice', False),
            "notice_period":                branch_content.get('notice_period', '3 calendar days'),
            # ─────────────────────────────────────────────────────────────────
        }

        pdf_stream = json_to_pdf(pdf_data)
        filename = f"Agreement_{agreement.clt_last_name}.pdf"
        return StreamingResponse(pdf_stream, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={filename}", "Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Methods": "GET, POST, OPTIONS", "Access-Control-Allow-Headers": "Authorization, Content-Type", "Access-Control-Allow-Credentials": "true"})

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"PDF Generation Error: {e}")
        print(f"Full traceback: {error_trace}")
        return JSONResponse(status_code=500, content={"detail": f"Internal PDF Generation Error: {str(e)}"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Methods": "GET, POST, OPTIONS", "Access-Control-Allow-Headers": "Authorization, Content-Type", "Access-Control-Allow-Credentials": "true"})

# -------------------- BRANCHES API --------------------
@app.get("/branches")
def get_branches(db: Session = Depends(get_db)):
    try:
        branches = db.query(models.Branch).all()
        print(f"Found {len(branches)} branches in database")
        result = []
        for branch in branches:
            if not branch.branch_code:
                continue
            display_name = BRANCH_DISPLAY_NAMES.get(branch.branch_code)
            if not display_name:
                display_name = branch.branch_name or branch.branch_code
            branch_state = branch.branch_state or 'MD'
            office_name = branch.office_name or "Options For Senior America"
            street = branch.street or getattr(branch, 'address_line_1', '') or ""
            street_full = street
            if getattr(branch, 'address_line_2', None):
                street_full = f"{street}, {branch.address_line_2}" if street else branch.address_line_2
            city = branch.city or ""
            zipcode = branch.zipcode or getattr(branch, 'zip_code', '') or ""
            branch_phone = branch.branch_phone or ""
            branch_fax = branch.branch_fax or getattr(branch, 'fax', '') or ""
            result.append({"branch_code": branch.branch_code, "branch_name": display_name, "office_name": office_name, "street": street_full, "city": city, "branch_state": branch_state, "zipcode": zipcode, "tel": branch_phone, "fax": branch_fax, "mileage": branch.mileage or 0.67})
        result.sort(key=lambda x: x["branch_name"])
        print(f"Returning {len(result)} branches to frontend")
        return JSONResponse(content=result, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
    except Exception as e:
        print(f"Error fetching branches: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

# ===== BRANCH MANAGEMENT ENDPOINTS =====
@app.post("/branches")
def create_branch(branch: BranchCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        existing = db.query(models.Branch).filter(models.Branch.branch_code == branch.branch_code).first()
        if existing:
            return JSONResponse(status_code=400, content={"detail": f"Branch code '{branch.branch_code}' already exists"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})
        new_branch = models.Branch(branch_code=branch.branch_code, branch_name=branch.branch_name, office_name=branch.office_name, street=branch.street, city=branch.city, branch_state=branch.branch_state, zipcode=branch.zipcode, branch_phone=branch.branch_phone, branch_fax=branch.branch_fax, mileage=branch.mileage, admin_meds=branch.admin_meds, is_corporate=branch.is_corporate)
        db.add(new_branch)
        db.commit()
        db.refresh(new_branch)
        default_content = {"required_services": "In addition to the general services that our caregivers provide such as assistance with activities of daily living, meal preparation, light housekeeping, and laundry, the required services as stated by the responsible party/client are:", "freq_of_visit": "", "hourly_rate": 36.00, "perc_charged": "100", "hazards": "None Reported", "mileage_rate": branch.mileage or 0.67, "care_type": "Home Care", "has_initial_contact": False, "notice_period": "3 calendar days", "holiday_count": 11, "requires_consumer_notice": False, "special_instructions": ""}
        db.execute(text("INSERT INTO branch_content (branch_code, content_type, content_data, created_at, updated_at) VALUES (:code, 'agreement', :data, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"), {"code": branch.branch_code, "data": json.dumps(default_content)})
        db.commit()
        return JSONResponse(content={"message": "Branch created successfully", "branch": {"branch_code": new_branch.branch_code, "branch_name": new_branch.branch_name}}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})
    except Exception as e:
        db.rollback()
        print(f"Error creating branch: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})

@app.put("/branches/{branch_code}")
def update_branch(branch_code: str, branch: BranchCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        existing = db.query(models.Branch).filter(models.Branch.branch_code == branch_code).first()
        if not existing:
            return JSONResponse(status_code=404, content={"detail": f"Branch '{branch_code}' not found"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})
        for key, value in branch.dict().items():
            if hasattr(existing, key):
                setattr(existing, key, value)
        db.commit()
        return JSONResponse(content={"message": "Branch updated successfully"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})
    except Exception as e:
        db.rollback()
        print(f"Error updating branch: {e}")
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})

@app.delete("/branches/{branch_code}")
def delete_branch(branch_code: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        agreements_count = db.query(models.Agreement).filter(models.Agreement.branch_code == branch_code).count()
        if agreements_count > 0:
            return JSONResponse(status_code=400, content={"detail": f"Cannot delete branch with {agreements_count} agreement(s). Please reassign or delete the agreements first."}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})
        db.execute(text("DELETE FROM branch_content WHERE branch_code = :code"), {"code": branch_code})
        branch = db.query(models.Branch).filter(models.Branch.branch_code == branch_code).first()
        if not branch:
            return JSONResponse(status_code=404, content={"detail": f"Branch '{branch_code}' not found"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})
        db.delete(branch)
        db.commit()
        return JSONResponse(content={"message": "Branch deleted successfully"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})
    except Exception as e:
        db.rollback()
        print(f"Error deleting branch: {e}")
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})

# ===== BRANCH CONTENT ENDPOINTS =====
@app.get("/branches/{branch_code}/content")
def get_branch_content(branch_code: str, db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT content_data FROM branch_content WHERE branch_code = :code AND content_type = 'agreement'"), {"code": branch_code}).first()
        if result:
            return JSONResponse(content=result[0], headers={"Access-Control-Allow-Origin": "http://localhost:5173"})
        else:
            default_content = {"required_services": "In addition to the general services that our caregivers provide such as assistance with activities of daily living, meal preparation, light housekeeping, and laundry, the required services as stated by the responsible party/client are:", "freq_of_visit": "", "hourly_rate": 36.00, "perc_charged": "100", "hazards": "None Reported", "mileage_rate": 0.67, "care_type": "Home Care", "has_initial_contact": False, "notice_period": "3 calendar days", "holiday_count": 11, "requires_consumer_notice": False, "special_instructions": ""}
            return JSONResponse(content=default_content, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})
    except Exception as e:
        print(f"Error getting branch content: {e}")
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})

@app.put("/branches/{branch_code}/content")
def update_branch_content(branch_code: str, content: dict, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        existing = db.execute(text("SELECT id FROM branch_content WHERE branch_code = :code AND content_type = 'agreement'"), {"code": branch_code}).first()
        if existing:
            db.execute(text("UPDATE branch_content SET content_data = :data, updated_at = CURRENT_TIMESTAMP WHERE branch_code = :code AND content_type = 'agreement'"), {"code": branch_code, "data": json.dumps(content)})
        else:
            db.execute(text("INSERT INTO branch_content (branch_code, content_type, content_data, created_at, updated_at) VALUES (:code, 'agreement', :data, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"), {"code": branch_code, "data": json.dumps(content)})
        db.commit()
        return JSONResponse(content={"message": "Branch content updated successfully"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})
    except Exception as e:
        db.rollback()
        print(f"Error updating branch content: {e}")
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})

# ===== COPY CONTENT BETWEEN BRANCHES =====
@app.post("/branches/copy-content")
def copy_branch_content(request: CopyContentRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        results = {"agreements": 0, "rates": 0, "services": 0}
        source_content = db.execute(text("SELECT content_data FROM branch_content WHERE branch_code = :code AND content_type = 'agreement'"), {"code": request.source_branch}).first()
        if not source_content:
            return JSONResponse(status_code=404, content={"detail": f"Source branch '{request.source_branch}' has no content"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})
        source_data = source_content[0]
        source_branch = db.query(models.Branch).filter(models.Branch.branch_code == request.source_branch).first()
        for target_code in request.target_branches:
            target_branch = db.query(models.Branch).filter(models.Branch.branch_code == target_code).first()
            if not target_branch:
                continue
            existing = db.execute(text("SELECT content_data FROM branch_content WHERE branch_code = :code AND content_type = 'agreement'"), {"code": target_code}).first()
            target_data = existing[0] if existing else {}
            if request.content_types.get("agreements", False):
                text_fields = ["required_services", "freq_of_visit", "hazards", "perc_charged", "charges_text", "payment_obligations_text", "live_in_text", "needs_assessment_text", "valuables_text", "notice_period_text", "cannot_hire_text", "record_keeping_text", "mileage_reimbursement_text", "vehicle_use_text", "general_provisions", "patients_rights_text", "complaint_procedures_text", "billing_procedures_text", "eft_authorization_text", "consumer_notice_text", "holidays_list"]
                for field in text_fields:
                    if field in source_data:
                        target_data[field] = source_data[field]
                results["agreements"] += 1
            if request.content_types.get("rates", False):
                if source_branch:
                    target_branch.mileage = source_branch.mileage
                for field in ["mileage_rate", "hourly_rate"]:
                    if field in source_data:
                        target_data[field] = source_data[field]
                results["rates"] += 1
            if request.content_types.get("services", False):
                for field in ["has_initial_contact", "requires_consumer_notice", "holiday_count", "care_type", "notice_period", "special_instructions"]:
                    if field in source_data:
                        target_data[field] = source_data[field]
                results["services"] += 1
            if existing:
                db.execute(text("UPDATE branch_content SET content_data = :data, updated_at = CURRENT_TIMESTAMP WHERE branch_code = :code AND content_type = 'agreement'"), {"code": target_code, "data": json.dumps(target_data)})
            else:
                db.execute(text("INSERT INTO branch_content (branch_code, content_type, content_data, created_at, updated_at) VALUES (:code, 'agreement', :data, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"), {"code": target_code, "data": json.dumps(target_data)})
        db.commit()
        return JSONResponse(content={"message": "Content copied successfully", "results": results}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})
    except Exception as e:
        db.rollback()
        print(f"Error copying content: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})

# -------------------- BRANCH SYNC API --------------------
@app.post("/branches/sync")
def sync_branches(db: Session = Depends(get_db)):
    from branch_config import BRANCH_DISPLAY_NAMES, get_branch_address
    import re
    results = {"created": [], "updated": [], "total": 0}
    for code, display_name in BRANCH_DISPLAY_NAMES.items():
        branch = db.query(models.Branch).filter(models.Branch.branch_code == code).first()
        addr = get_branch_address(code)
        state_match = re.search(r'\(([A-Z]{2})\)', display_name)
        state_code = state_match.group(1) if state_match else 'MD'
        if branch:
            branch.office_name = addr['office_name']; branch.street = addr['address_line_1']; branch.city = addr['city']
            branch.branch_state = state_code; branch.zipcode = addr['zip_code']; branch.branch_phone = addr['tel']; branch.branch_fax = addr['fax']
            results["updated"].append(code)
        else:
            new_branch = models.Branch(branch_code=code, branch_name=display_name, office_name=addr['office_name'], street=addr['address_line_1'], city=addr['city'], branch_state=state_code, zipcode=addr['zip_code'], branch_phone=addr['tel'], branch_fax=addr['fax'], responsible_title=None, care_coordinator_name=None, mileage=None, admin_meds=False, corp_state_long=None, office_phone_corp=None, fein=None, is_corporate=False)
            db.add(new_branch)
            results["created"].append(code)
    db.commit()
    results["total"] = len(results["created"]) + len(results["updated"])
    return JSONResponse(content={"message": "Branches synced successfully", "results": results}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

# ===== DEBUG: Check what's in branch_content DB =====
@app.get("/debug/branch-content/{branch_code}")
def debug_branch_content(branch_code: str, db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT content_data FROM branch_content WHERE branch_code = :code AND content_type = 'agreement'"), {"code": branch_code}).first()
        if not result:
            return JSONResponse(content={"error": f"No branch_content found for branch_code='{branch_code}'", "hint": "Go to Edit Content and Save Template for this branch first"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})
        raw = result[0]
        data = json.loads(raw) if isinstance(raw, str) else raw
        return JSONResponse(content={"branch_code": branch_code, "type": str(type(raw).__name__), "keys_saved": list(data.keys()), "data": data}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173"})

@app.get("/branch-config/{branch_code}")
def get_branch_config_api(branch_code: str, state_code: str = "MD"):
    try:
        config = get_branch_config(branch_code, state_code)
        return JSONResponse(content=config, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
    except Exception as e:
        return JSONResponse(status_code=404, content={"detail": f"Branch config not found: {str(e)}"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

@app.get("/shared-agreement/{token}")
def get_shared_agreement(token: str, db: Session = Depends(get_db)):
    try:
        shared = db.query(models.SharedAgreement).filter(models.SharedAgreement.token == token, models.SharedAgreement.is_active == True).first()
        if not shared:
            return JSONResponse(status_code=404, content={"detail": "Invalid or expired share link"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        if shared.expires_at < datetime.now():
            shared.is_active = False
            db.commit()
            return JSONResponse(status_code=404, content={"detail": "Share link has expired"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        shared.views += 1
        db.commit()
        agreement = db.query(models.Agreement).filter(models.Agreement.id == shared.agreement_id).first()
        if not agreement:
            return JSONResponse(status_code=404, content={"detail": "Agreement not found"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        return JSONResponse(content={"id": agreement.id, "clt_first_name": agreement.clt_first_name, "clt_last_name": agreement.clt_last_name, "branch_code": agreement.branch_code, "hourly_rate": agreement.hourly_rate, "care_type": agreement.care_type, "start_date": agreement.start_date.isoformat() if agreement.start_date else None}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
    except Exception as e:
        print(f"Error getting shared agreement: {e}")
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

# ================================================================================
# ✅ FIXED: get_shared_agreement_pdf — now fetches branch_content and passes all
#    Edit Content fields into pdf_data (was missing before)
# ================================================================================
@app.get("/shared-agreement/{token}/pdf")
def get_shared_agreement_pdf(token: str, db: Session = Depends(get_db)):
    try:
        shared = db.query(models.SharedAgreement).filter(models.SharedAgreement.token == token, models.SharedAgreement.is_active == True).first()
        if not shared:
            return JSONResponse(status_code=404, content={"detail": "Invalid or expired share link"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        if shared.expires_at < datetime.now():
            shared.is_active = False
            db.commit()
            return JSONResponse(status_code=404, content={"detail": "Share link has expired"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})
        agreement = db.query(models.Agreement).filter(models.Agreement.id == shared.agreement_id).first()
        if not agreement:
            return JSONResponse(status_code=404, content={"detail": "Agreement not found"}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

        branch = db.query(models.Branch).filter(models.Branch.branch_code == agreement.branch_code).first()
        branch_mileage = 0.67
        if branch and branch.mileage:
            branch_mileage = float(branch.mileage)
        branch_data = {}
        if branch:
            branch_data = {"Mileage": branch_mileage, "branch_code": branch.branch_code, "office_name": getattr(branch, 'office_name', '')}

        # ✅ FIX: Fetch branch_content so Edit Content fields appear in shared PDF
        branch_content_row = db.execute(
            text("SELECT content_data FROM branch_content WHERE branch_code = :code AND content_type = 'agreement'"),
            {"code": agreement.branch_code}
        ).first()
        branch_content = branch_content_row[0] if branch_content_row else {}
        if isinstance(branch_content, str):
            branch_content = json.loads(branch_content)
        print(f"[SharedPDF] branch={agreement.branch_code} content_keys={list(branch_content.keys())}")
        # ─────────────────────────────────────────────────────────────────────

        logo_path = Config.get_logo_path()

        pdf_data = {
            "branch_code": agreement.branch_code,
            "branch_data": branch_data,
            "office_name": getattr(branch, 'office_name', "Options For Senior America"),
            "address_line_1": getattr(branch, 'street', ''),
            "address_line_2": "",
            "city": getattr(branch, 'city', ''),
            "state_code": getattr(branch, 'branch_state', 'MD'),
            "zip_code": getattr(branch, 'zipcode', ''),
            "tel": getattr(branch, 'branch_phone', ''),
            "fax": getattr(branch, 'branch_fax', ''),
            "clt_title": agreement.clt_title or "",
            "clt_first_name": agreement.clt_first_name,
            "clt_last_name": agreement.clt_last_name,
            "clt_address": agreement.clt_address or "",
            "clt_city": agreement.clt_city or "",
            "clt_state": agreement.clt_state or "",
            "clt_zip": agreement.clt_zip or "",
            "clt_relationship": agreement.clt_relationship or "Self",
            "responsible_party": f"{agreement.clt_first_name} {agreement.clt_last_name}".strip(),
            "care_title": agreement.care_title or "",
            "care_first_name": agreement.care_first_name,
            "care_last_name": agreement.care_last_name,
            "care_recipient_address": agreement.care_recipient_address or "",
            "care_city": agreement.care_city or "",
            "care_state": agreement.care_state or "",
            "care_zip": agreement.care_zip or "",
            "initial_inquiry_date": agreement.initial_inquiry_date.strftime("%m/%d/%Y") if agreement.initial_inquiry_date else "",
            "agreement_date": agreement.agreement_date.strftime("%m/%d/%Y") if agreement.agreement_date else "",
            "start_date": agreement.start_date.strftime("%m/%d/%Y") if agreement.start_date else "",
            "services_start_time": agreement.services_start_time or "",
            "instructions_given_by": agreement.instructions_given_by or "",
            "handled_by": agreement.handled_by or "",
            "frequency_duration": agreement.frequency_duration or "",
            "care_type": branch_content.get('care_type', agreement.care_type or "Home Care"),
            "is_live_in": str(agreement.is_live_in).lower(),
            "hourly_rate": f"{float(agreement.hourly_rate):.2f}",
            "mileage_rate": f"{branch_mileage:.2f}",
            "vehicle_authorized": str(agreement.vehicle_authorized).lower(),
            "vehicle_authorization_initials": agreement.vehicle_authorization_initials or "",
            # ✅ FIX: both key names for perc_charged
            "PercCharged": str(getattr(agreement, 'perc_charged', '100')),
            "perc_charged": str(getattr(agreement, 'perc_charged', '100')),
            # Agreement-level fields, fall back to branch template
            "hazards":           getattr(agreement, 'hazards', None) or branch_content.get('hazards', 'None Reported'),
            "required_services": getattr(agreement, 'required_services', None) or branch_content.get('required_services', ''),
            "freq_of_visit":     getattr(agreement, 'freq_of_visit', None) or branch_content.get('freq_of_visit', ''),
            "inicontactdate": agreement.inicontactdate.strftime("%m/%d/%Y") if hasattr(agreement, 'inicontactdate') and agreement.inicontactdate else "",
            "date_of_order": agreement.date_of_order.strftime("%m/%d/%Y") if hasattr(agreement, 'date_of_order') and agreement.date_of_order else "",
            "page1_cont_signature": getattr(agreement, 'page1_cont_signature', ''),
            "page3_1_signature": getattr(agreement, 'page3_1_signature', ''),
            "bank_name": agreement.bank_name or "",
            "bank_city": agreement.bank_city or "",
            "bank_state": agreement.bank_state or "",
            "routing_number": agreement.routing_number or "",
            "account_number": agreement.account_number or "",
            "account_type": agreement.account_type or "Checking",
            "client_signature": agreement.client_signature or "",
            "logo_path": logo_path,
            # ✅ ALL Edit Content fields — now included in shared PDF too
            "notice_period_text":           branch_content.get('notice_period_text', ''),
            "needs_assessment_text":        branch_content.get('needs_assessment_text', ''),
            "valuables_text":               branch_content.get('valuables_text', ''),
            "medication_text":              branch_content.get('medication_text', ''),
            "cannot_hire_text":             branch_content.get('cannot_hire_text', ''),
            "record_keeping_text":          branch_content.get('record_keeping_text', ''),
            "mileage_reimbursement_text":   branch_content.get('mileage_reimbursement_text', ''),
            "vehicle_use_text":             branch_content.get('vehicle_use_text', ''),
            "payment_obligations_text":     branch_content.get('payment_obligations_text', ''),
            "patients_rights_text":         branch_content.get('patients_rights_text', ''),
            "complaint_procedures_text":    branch_content.get('complaint_procedures_text', ''),
            "billing_procedures_text":      branch_content.get('billing_procedures_text', ''),
            "eft_authorization_text":       branch_content.get('eft_authorization_text', ''),
            "consumer_notice_text":         branch_content.get('consumer_notice_text', ''),
            "holiday_count":                branch_content.get('holiday_count', 11),
            "has_initial_contact":          branch_content.get('has_initial_contact', False),
            "requires_consumer_notice":     branch_content.get('requires_consumer_notice', False),
            "notice_period":                branch_content.get('notice_period', '3 calendar days'),
        }

        from pdf_generator import json_to_pdf
        pdf_stream = json_to_pdf(pdf_data)
        filename = f"Agreement_{agreement.clt_last_name}.pdf"
        return StreamingResponse(pdf_stream, media_type="application/pdf", headers={"Content-Disposition": f"inline; filename={filename}", "Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})

    except Exception as e:
        print(f"Error getting shared PDF: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"detail": str(e)}, headers={"Access-Control-Allow-Origin": "http://localhost:5173", "Access-Control-Allow-Credentials": "true"})