"""
Unit Tests for BankSight
Test suite for fraud detection, analytics, and utilities
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.analytics.fraud_detection import FraudDetectionEngine, BehaviorAnalyzer, AnomalyDetector
from src.analytics.analytics import TransactionAnalytics, CustomerAnalytics, RiskScoring
from src.utils.helpers import ValidationUtils, SecurityUtils, NumberFormatting


class TestFraudDetectionEngine:
    """Test Fraud Detection Engine"""
    
    @pytest.fixture
    def engine(self):
        return FraudDetectionEngine()
    
    @pytest.fixture
    def sample_transaction(self):
        return {
            'amount': 100.0,
            'transaction_date': datetime.now(),
            'merchant_name': 'Walmart',
            'merchant_category': 'RETAIL',
            'device_id': 'DEV_001',
            'merchant_country': 'USA',
        }
    
    @pytest.fixture
    def customer_profile(self):
        return {
            'avg_transaction_amount': 50.0,
            'std_transaction_amount': 25.0,
            'max_typical': 200.0,
            'preferred_merchants': ['Walmart', 'Target', 'Costco'],
            'preferred_categories': ['RETAIL'],
            'trusted_devices': ['DEV_001', 'DEV_002'],
            'typical_countries': ['USA'],
            'avg_daily_transactions': 2,
        }
    
    def test_engine_initialization(self, engine):
        assert engine is not None
        assert engine.isolation_forest is not None
    
    def test_feature_extraction(self, engine, sample_transaction, customer_profile):
        features = engine.extract_features(
            sample_transaction,
            customer_profile
        )
        assert 'amount' in features
        assert 'combined_risk_score' in features


class TestTransactionAnalytics:
    """Test Transaction Analytics"""
    
    @pytest.fixture
    def sample_transactions(self):
        n = 100
        return pd.DataFrame({
            'amount': np.random.exponential(100, n),
            'transaction_type': np.random.choice(['DEBIT', 'CREDIT'], n),
            'status': np.random.choice(['COMPLETED', 'FAILED'], n),
            'merchant_name': np.random.choice(['Walmart', 'Target', 'Amazon'], n),
            'merchant_category': np.random.choice(['RETAIL', 'FOOD'], n),
            'merchant_country': np.random.choice(['USA', 'UK'], n),
            'transaction_date': [datetime.now() - timedelta(days=i) for i in range(n)],
        })
    
    def test_transaction_summary(self, sample_transactions):
        summary = TransactionAnalytics.get_transaction_summary(sample_transactions)
        assert 'total_transactions' in summary
        assert 'total_volume' in summary
        assert 'avg_transaction' in summary
    
    def test_daily_metrics(self, sample_transactions):
        metrics = TransactionAnalytics.get_daily_metrics(sample_transactions)
        assert not metrics.empty
        assert 'total_amount' in metrics.columns


class TestValidationUtils:
    """Test Validation Utilities"""
    
    def test_validate_email(self):
        assert ValidationUtils.validate_email('test@example.com') == True
        assert ValidationUtils.validate_email('invalid-email') == False
    
    def test_validate_phone(self):
        assert ValidationUtils.validate_phone('1234567890') == True
        assert ValidationUtils.validate_phone('123') == False
    
    def test_validate_amount(self):
        assert ValidationUtils.validate_amount(100.0) == True
        assert ValidationUtils.validate_amount(-50.0) == False
    
    def test_validate_required_fields(self):
        data = {'name': 'John', 'email': 'john@example.com'}
        valid, missing = ValidationUtils.validate_required_fields(
            data, 
            ['name', 'email']
        )
        assert valid == True
        assert len(missing) == 0


class TestSecurityUtils:
    """Test Security Utilities"""
    
    def test_mask_card_number(self):
        masked = SecurityUtils.mask_card_number('1234567890123456')
        assert masked == '****3456'
    
    def test_mask_email(self):
        masked = SecurityUtils.mask_email('test@example.com')
        assert 'test' not in masked or masked.startswith('t')
        assert '@example.com' in masked
    
    def test_hash_sensitive_data(self):
        data = 'sensitive_information'
        hashed1 = SecurityUtils.hash_sensitive_data(data)
        hashed2 = SecurityUtils.hash_sensitive_data(data, hashed1[:32])
        assert hashed1 != data
        assert len(hashed1) > len(data)


class TestNumberFormatting:
    """Test Number Formatting"""
    
    def test_format_currency(self):
        formatted = NumberFormatting.format_currency(1000.50)
        assert '$' in formatted
        assert '1,000.50' in formatted
    
    def test_format_percentage(self):
        formatted = NumberFormatting.format_percentage(0.75)
        assert '%' in formatted
        assert '75' in formatted
    
    def test_format_large_number(self):
        assert 'M' in NumberFormatting.format_large_number(1000000)
        assert 'B' in NumberFormatting.format_large_number(1000000000)
        assert 'K' in NumberFormatting.format_large_number(1000)


class TestAnomalyDetector:
    """Test Anomaly Detector"""
    
    @pytest.fixture
    def sample_data(self):
        return pd.Series([1, 2, 3, 4, 5, 100])  # 100 is an outlier
    
    def test_zscore_outliers(self, sample_data):
        outliers = AnomalyDetector.detect_statistical_outliers(sample_data)
        assert outliers.any()  # Should detect 100 as outlier
    
    def test_iqr_outliers(self, sample_data):
        outliers = AnomalyDetector.detect_iqr_outliers(sample_data)
        assert outliers.any()


class TestBehaviorAnalyzer:
    """Test Customer Behavior Analyzer"""
    
    @pytest.fixture
    def sample_transactions(self):
        n = 50
        return pd.DataFrame({
            'amount': np.random.exponential(100, n),
            'merchant_name': np.random.choice(['Merchant1', 'Merchant2', 'Merchant3'], n),
            'merchant_category': np.random.choice(['FOOD', 'RETAIL'], n),
            'merchant_country': np.random.choice(['USA'], n),
            'transaction_date': [datetime.now() - timedelta(hours=i) for i in range(n)],
        })
    
    def test_customer_profile(self, sample_transactions):
        profile = BehaviorAnalyzer.calculate_customer_profile(sample_transactions)
        assert 'avg_transaction_amount' in profile
        assert 'preferred_merchants' in profile


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
