"""
Database Models for BankSight
Defines all data structures for transaction, customer, and fraud scoring
"""

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Text, Boolean, 
    ForeignKey, Index, Enum, JSON, Numeric, BigInteger
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class Customer(Base):
    """Customer Information Model"""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(String(50), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True)
    phone = Column(String(20))
    date_of_birth = Column(DateTime)
    registration_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_status = Column(String(20), default="ACTIVE")
    risk_score = Column(Float, default=0.0)
    risk_classification = Column(String(20), default="LOW")
    kyc_verified = Column(Boolean, default=False)
    country = Column(String(50))
    state_province = Column(String(100))
    city = Column(String(100))
    postal_code = Column(String(20))
    occupation = Column(String(100))
    income_range = Column(String(50))
    
    # Relationships
    transactions = relationship("Transaction", back_populates="customer", cascade="all, delete-orphan")
    fraud_alerts = relationship("FraudAlert", back_populates="customer")
    device_info = relationship("DeviceInfo", back_populates="customer")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_customer_id', 'customer_id'),
        Index('idx_registration_date', 'registration_date'),
        Index('idx_risk_score', 'risk_score'),
    )


class Transaction(Base):
    """Transaction Records Model"""
    __tablename__ = "transactions"
    
    id = Column(BigInteger, primary_key=True)
    transaction_id = Column(String(100), unique=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(3), default="USD")
    transaction_type = Column(String(50), nullable=False)  # DEBIT, CREDIT, TRANSFER, etc.
    merchant_name = Column(String(255))
    merchant_category = Column(String(100))
    merchant_country = Column(String(50))
    merchant_city = Column(String(100))
    status = Column(String(20), default="COMPLETED")  # COMPLETED, FAILED, PENDING
    description = Column(Text)
    
    # Fraud Detection Fields
    fraud_score = Column(Float, default=0.0)
    is_flagged = Column(Boolean, default=False)
    fraud_reason = Column(String(255))
    
    # Device and Location
    device_id = Column(String(100), index=True)
    ip_address = Column(String(45))
    latitude = Column(Float)
    longitude = Column(Float)
    mcc_code = Column(String(4))
    
    # Additional Features
    device_trust_score = Column(Float)
    location_trust_score = Column(Float)
    velocity_score = Column(Float)
    
    # Relationships
    customer = relationship("Customer", back_populates="transactions")
    fraud_data = relationship("TransactionFraudData", back_populates="transaction", uselist=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_customer_transaction', 'customer_id', 'transaction_date'),
        Index('idx_transaction_date', 'transaction_date'),
        Index('idx_is_flagged', 'is_flagged'),
        Index('idx_fraud_score', 'fraud_score'),
    )


class TransactionFraudData(Base):
    """Detailed Fraud Analysis Data"""
    __tablename__ = "transaction_fraud_data"
    
    id = Column(Integer, primary_key=True)
    transaction_id = Column(BigInteger, ForeignKey("transactions.id"), nullable=False, unique=True)
    
    # Feature Scores
    amount_anomaly_score = Column(Float)
    temporal_anomaly_score = Column(Float)
    location_anomaly_score = Column(Float)
    device_anomaly_score = Column(Float)
    merchant_anomaly_score = Column(Float)
    
    # Pattern Analysis
    deviation_from_avg = Column(Float)  # Standard deviations
    transaction_frequency_rank = Column(Integer)
    customer_typical_amount = Column(Numeric(15, 2))
    
    # Risk Indicators
    is_new_merchant = Column(Boolean)
    is_new_device = Column(Boolean)
    is_international = Column(Boolean)
    is_late_night = Column(Boolean)
    is_weekend = Column(Boolean)
    
    model_prediction = Column(JSON)
    feature_importance = Column(JSON)
    
    transaction = relationship("Transaction", back_populates="fraud_data")
    created_at = Column(DateTime, default=datetime.utcnow)


class FraudAlert(Base):
    """Fraud Alerts and Cases"""
    __tablename__ = "fraud_alerts"
    
    id = Column(Integer, primary_key=True)
    alert_id = Column(String(100), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    transaction_ids = Column(String(500))  # Comma-separated transaction IDs
    alert_type = Column(String(50), nullable=False)  # FRAUD, SUSPICIOUS, ANOMALY
    severity = Column(String(20), default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    description = Column(Text)
    status = Column(String(20), default="OPEN")  # OPEN, INVESTIGATING, CLOSED, CONFIRMED
    
    # Investigation Details
    investigator_notes = Column(Text)
    resolution_notes = Column(Text)
    resolution_status = Column(String(50))  # FRAUD_CONFIRMED, FALSE_POSITIVE, UNDER_REVIEW
    
    customer = relationship("Customer", back_populates="fraud_alerts")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime)
    
    __table_args__ = (
        Index('idx_customer_alerts', 'customer_id', 'status'),
        Index('idx_alert_severity', 'severity', 'status'),
    )


class DeviceInfo(Base):
    """Device Information and Trust Scores"""
    __tablename__ = "device_info"
    
    id = Column(Integer, primary_key=True)
    device_id = Column(String(100), unique=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    
    device_type = Column(String(50))  # MOBILE, WEB, ATM, POS
    operating_system = Column(String(100))
    browser_type = Column(String(100))
    device_fingerprint = Column(String(500))
    
    trust_score = Column(Float, default=0.5)
    last_used = Column(DateTime)
    first_seen = Column(DateTime, default=datetime.utcnow)
    
    is_trusted = Column(Boolean, default=False)
    failed_attempts = Column(Integer, default=0)
    successful_transactions = Column(Integer, default=0)
    
    ip_addresses = Column(JSON)  # List of associated IPs
    locations = Column(JSON)  # List of known locations
    
    customer = relationship("Customer", back_populates="device_info")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_customer_device', 'customer_id'),
    )


class BehavioralPattern(Base):
    """Customer Behavioral Patterns"""
    __tablename__ = "behavioral_patterns"
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, unique=True)
    
    avg_transaction_amount = Column(Numeric(15, 2))
    avg_daily_transactions = Column(Float)
    avg_transactions_per_week = Column(Float)
    
    preferred_merchants = Column(JSON)  # List of top merchants
    preferred_categories = Column(JSON)  # List of preferred MCC codes
    preferred_locations = Column(JSON)  # List of common locations
    
    typical_transaction_time_start = Column(String(5))  # HH:MM format
    typical_transaction_time_end = Column(String(5))
    peak_transaction_days = Column(JSON)  # Days of week with most transactions
    
    travel_patterns = Column(JSON)  # Historical location data
    device_patterns = Column(JSON)  # Devices typically used
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuditLog(Base):
    """Audit Trail for Compliance"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    event_type = Column(String(100), nullable=False)
    entity_type = Column(String(50))
    entity_id = Column(String(100))
    user_id = Column(String(100))
    action = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, REVIEW
    previous_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))
    details = Column(Text)
    
    __table_args__ = (
        Index('idx_timestamp', 'timestamp'),
        Index('idx_event_type', 'event_type'),
    )


class Dashboard(Base):
    """Dashboard and Report Metadata"""
    __tablename__ = "dashboards"
    
    id = Column(Integer, primary_key=True)
    dashboard_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    dashboard_type = Column(String(50))  # OVERVIEW, FRAUD, CUSTOMER, RISK
    config = Column(JSON)  # Dashboard configuration
    created_by = Column(String(100))
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
