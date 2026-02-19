from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class AgreementBase(BaseModel):
    # CLIENT
    clt_title: Optional[str] = None
    clt_first_name: str
    clt_last_name: str
    clt_email: Optional[str] = None
    clt_phone: Optional[str] = None
    clt_address: str
    clt_city: Optional[str] = None
    clt_state: Optional[str] = "MD"
    clt_zip: Optional[str] = None
    responsible_party: Optional[str] = None
    clt_relationship: str = "Self" 

    # CARE RECIPIENT
    care_title: Optional[str] = None
    care_first_name: str
    care_last_name: str
    care_dob: Optional[date] = None
    care_recipient_address: Optional[str] = None 
    care_city: Optional[str] = None
    care_state: Optional[str] = "MD"
    care_zip: Optional[str] = None

    # SERVICE
    branch_code: str = "mnhomecare" 
    handled_by: Optional[str] = None
    agreement_date: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    
    
    initial_inquiry_date: Optional[date] = None
    services_start_time: Optional[str] = None
    instructions_given_by: Optional[str] = None
  

    hours_requested: Optional[str] = None 
    frequency_duration: Optional[str] = None
    care_type: str = "Home Care"
    is_live_in: bool = False
    hourly_rate: float = 36.0
    mileage_rate: float = 0.67
    
    # Additional service details
    vehicle_authorized: bool = False
    vehicle_authorization_initials: Optional[str] = None
    medication_administration: bool = False

    # PAYMENT
    bank_name: Optional[str] = None
    bank_city: Optional[str] = None
    bank_state: Optional[str] = None
    routing_number: Optional[str] = None
    account_number: Optional[str] = None
    account_type: str = "Checking"
    payment_method: str = "Direct Debit"

    # SIGNATURES
    client_initials: Optional[str] = None
    client_sign_date: Optional[date] = None
    rep_sign_date: Optional[date] = None
    client_signature: Optional[str] = None
    rep_signature: Optional[str] = "Staff Signed"

class AgreementCreate(AgreementBase):
    status: Optional[str] = "Pending"

class Agreement(AgreementBase):
    id: int
    owner_id: int
    status: str

    model_config = ConfigDict(from_attributes=True)

class BranchBase(BaseModel):
    branch_code: str
    office_name: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state_code: Optional[str] = None
    zip_code: Optional[str] = None
    tel: Optional[str] = None
    fax: Optional[str] = None
    mobile: Optional[str] = None
    is_corporate: bool = False
   

    class Config:
        from_attributes = True