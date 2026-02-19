from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    Boolean,
    Text,
    Numeric,
    TypeDecorator
)
from sqlalchemy.orm import relationship
from database import Base
import decimal


# Custom type for PostgreSQL numeric
class NumericFloat(TypeDecorator):
    """Convert Python float to PostgreSQL numeric and back"""
    impl = Numeric(10, 2)
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            return decimal.Decimal(str(value))
        return None
    
    def process_result_value(self, value, dialect):
        if value is not None:
            return float(value)
        return None


# -------------------- USER --------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="client")

    agreements = relationship(
        "Agreement",
        back_populates="owner",
        cascade="all, delete-orphan"
    )


# -------------------- BRANCH --------------------
class Branch(Base):
    __tablename__ = "tblbranch"

    id = Column(Integer, primary_key=True)
    branch_name = Column(String, nullable=True)
    branch_code = Column(String(50), unique=True, index=True, nullable=False)
    responsible_title = Column(String, nullable=True)
    care_coordinator_name = Column(String, nullable=True)
    branch_phone = Column(String(25), nullable=True)
    branch_state = Column(String(2), nullable=True)
    mileage = Column(Float, nullable=True)
    admin_meds = Column(Boolean, default=False)
    street = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    zipcode = Column(String(10), nullable=True)
    corp_state_long = Column(String(100), nullable=True)
    office_phone_corp = Column(String(25), nullable=True)
    fein = Column(String(20), nullable=True)
    branch_fax = Column(String(25), nullable=True)
    office_name = Column(Text, nullable=True)
    address_line_1 = Column(Text, nullable=True)
    state_code = Column(String(2), nullable=True)
    zip_code = Column(String(10), nullable=True)
    is_corporate = Column(Boolean, default=False)
    address_line_2 = Column(Text, nullable=True) 
    fax = Column(String(25), nullable=True)
    tel = Column(String)

    # Relationship
    agreements = relationship(
        "Agreement",
        primaryjoin="Branch.branch_code == Agreement.branch_code",
        back_populates="branch",
        overlaps="branch"
    )


# -------------------- AGREEMENT --------------------
class Agreement(Base):
    __tablename__ = "agreements"

    id = Column(Integer, primary_key=True, index=True)

    # SECTION 1: CLIENT
    clt_title = Column(String, nullable=True)
    clt_first_name = Column(String, nullable=False)
    clt_last_name = Column(String, nullable=False)
    clt_email = Column(String, nullable=True)
    clt_phone = Column(String, nullable=True)
    clt_address = Column(String, nullable=False)
    clt_city = Column(String, nullable=True)
    clt_state = Column(String(2), default="MD")
    clt_zip = Column(String(10), nullable=True)
    responsible_party = Column(String, nullable=True)
    clt_relationship = Column(String, nullable=True, default="Self")

    # SECTION 2: CARE RECIPIENT
    care_title = Column(String, nullable=True)
    care_first_name = Column(String, nullable=False)
    care_last_name = Column(String, nullable=False)
    care_dob = Column(Date, nullable=True)
    care_recipient_address = Column(String, nullable=True)
    care_city = Column(String, nullable=True)
    care_state = Column(String(2), default="MD")
    care_zip = Column(String(10), nullable=True)

    # SECTION 3: SERVICE
    branch_code = Column(
        String(50),
        ForeignKey("tblbranch.branch_code"),
        nullable=False
    )

    handled_by = Column(String, nullable=True)
    agreement_date = Column(Date, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    initial_inquiry_date = Column(Date, nullable=True)
    services_start_time = Column(String, nullable=True)
    instructions_given_by = Column(String, nullable=True)

    hours_requested = Column(String, nullable=True)
    frequency_duration = Column(String, nullable=True) 
    care_type = Column(String)
    is_live_in = Column(Boolean, default=False)
    
    # FIXED: Use custom NumericFloat type
    hourly_rate = Column(NumericFloat, default=36.0)
    mileage_rate = Column(NumericFloat, default=0.67)
    
    status = Column(String, default="Pending")
    
    # Additional service details
    vehicle_authorized = Column(Boolean, default=False)  
    vehicle_authorization_initials = Column(String(10), nullable=True)
    medication_administration = Column(Boolean, default=False)   

    # SECTION 4: PAYMENT
    bank_name = Column(String, nullable=True)
    bank_city = Column(String, nullable=True)
    bank_state = Column(String(2), nullable=True)
    routing_number = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    account_type = Column(String, default="Checking")
    payment_method = Column(String, default="Direct Debit")

    # SECTION 5: SIGNATURES
    client_initials = Column(String(5), nullable=True)
    client_sign_date = Column(Date, nullable=True)
    rep_sign_date = Column(Date, nullable=True)
    client_signature = Column(Text, nullable=True)
    rep_signature = Column(Text, default="Staff Signed")
    
    # Additional signature fields for multiple pages
    page1_signature = Column(Text, nullable=True)
    page2_signature = Column(Text, nullable=True)
    page3_signature = Column(Text, nullable=True)

    # OWNERSHIP
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="agreements")
    branch = relationship("Branch", back_populates="agreements")