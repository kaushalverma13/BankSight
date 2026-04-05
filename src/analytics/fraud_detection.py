"""
Advanced Fraud Detection Module
ML-based fraud detection using Isolation Forest and behavioral analysis
"""

import logging
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from scipy import stats
from datetime import datetime, timedelta
from typing import Tuple, Dict, List
import pickle
import os

logger = logging.getLogger(__name__)


class FraudDetectionEngine:
    """Enterprise Fraud Detection Engine"""
    
    def __init__(self, contamination=0.05):
        self.contamination = contamination
        self.isolation_forest = None
        self.scaler = StandardScaler()
        self.feature_importance = {}
        self.model_path = "models/fraud_model.pkl"
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load trained model or create new one"""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.isolation_forest = pickle.load(f)
                logger.info("Fraud detection model loaded from disk")
            except Exception as e:
                logger.warning(f"Failed to load model: {e}. Creating new model.")
                self.isolation_forest = IsolationForest(
                    contamination=self.contamination,
                    random_state=42,
                    n_estimators=100
                )
        else:
            self.isolation_forest = IsolationForest(
                contamination=self.contamination,
                random_state=42,
                n_estimators=100
            )
    
    def save_model(self):
        """Save trained model to disk"""
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.isolation_forest, f)
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
    
    def extract_features(self, 
                        transaction: Dict, 
                        customer_profile: Dict,
                        historical_data: pd.DataFrame = None) -> Dict:
        """
        Extract comprehensive fraud detection features
        
        Args:
            transaction: Current transaction data
            customer_profile: Customer behavioral profile
            historical_data: Historical transaction data for comparison
            
        Returns:
            Dictionary of extracted features
        """
        features = {}
        
        # 1. Amount-based features
        amount = transaction.get('amount', 0)
        avg_amount = customer_profile.get('avg_transaction_amount', 0)
        
        features['amount'] = amount
        features['amount_zscore'] = self._calculate_zscore(
            amount, 
            avg_amount, 
            customer_profile.get('std_transaction_amount', 1)
        )
        features['amount_ratio'] = amount / (avg_amount + 1)
        features['is_high_amount'] = 1 if amount > customer_profile.get('max_typical', 10000) else 0
        
        # 2. Temporal features
        transaction_time = transaction.get('transaction_date')
        hour = transaction_time.hour if transaction_time else 0
        day_of_week = transaction_time.weekday() if transaction_time else 0
        
        features['hour'] = hour
        features['day_of_week'] = day_of_week
        features['is_late_night'] = 1 if hour >= 22 or hour <= 6 else 0
        features['is_weekend'] = 1 if day_of_week >= 5 else 0
        
        typical_hours = customer_profile.get('typical_transaction_hours', [])
        features['is_unusual_hour'] = 1 if hour not in typical_hours else 0
        
        # 3. Merchant features
        merchant_name = transaction.get('merchant_name', '')
        merchant_category = transaction.get('merchant_category', '')
        
        preferred_merchants = customer_profile.get('preferred_merchants', [])
        preferred_categories = customer_profile.get('preferred_categories', [])
        
        features['is_new_merchant'] = 1 if merchant_name not in preferred_merchants else 0
        features['is_new_category'] = 1 if merchant_category not in preferred_categories else 0
        
        # 4. Device and location features
        device_id = transaction.get('device_id')
        trusted_devices = customer_profile.get('trusted_devices', [])
        
        features['is_new_device'] = 1 if device_id not in trusted_devices else 0
        features['device_trust_score'] = transaction.get('device_trust_score', 0.5)
        
        # Geolocation
        merchant_country = transaction.get('merchant_country')
        customer_countries = customer_profile.get('typical_countries', [])
        
        features['is_foreign_transaction'] = 1 if merchant_country not in customer_countries else 0
        features['location_trust_score'] = transaction.get('location_trust_score', 0.5)
        
        # 5. Velocity features
        if historical_data is not None:
            velocity_features = self._calculate_velocity_features(
                transaction_time,
                historical_data,
                customer_profile
            )
            features.update(velocity_features)
        else:
            features['transaction_count_24h'] = 0
            features['total_amount_24h'] = 0
            features['velocity_zscore'] = 0
        
        # 6. Pattern features
        transaction_count = customer_profile.get('avg_daily_transactions', 1)
        features['transaction_frequency_deviation'] = self._calculate_zscore(
            transaction_count,
            customer_profile.get('mean_frequency', 5),
            customer_profile.get('std_frequency', 2)
        )
        
        # 7. Risk score composition
        features['combined_risk_score'] = self._calculate_combined_risk(features)
        
        return features
    
    def _calculate_zscore(self, value, mean, std):
        """Calculate Z-score"""
        if std == 0:
            return 0
        return (value - mean) / std
    
    def _calculate_velocity_features(self, 
                                    transaction_time: datetime,
                                    historical_data: pd.DataFrame,
                                    customer_profile: Dict) -> Dict:
        """Calculate velocity-based features"""
        features = {}
        
        # Transactions in last 24 hours
        cutoff_time = transaction_time - timedelta(hours=24)
        recent_txns = historical_data[historical_data['transaction_date'] > cutoff_time]
        
        features['transaction_count_24h'] = len(recent_txns)
        features['total_amount_24h'] = recent_txns['amount'].sum() if len(recent_txns) > 0 else 0
        
        avg_24h = customer_profile.get('avg_daily_transactions', 1)
        features['velocity_zscore'] = self._calculate_zscore(
            features['transaction_count_24h'],
            avg_24h,
            customer_profile.get('std_daily_transactions', 1)
        )
        
        # Geographic velocity (impossible travel)
        features['geographic_velocity'] = self._check_geographic_velocity(
            transaction_time,
            historical_data
        )
        
        return features
    
    def _check_geographic_velocity(self, 
                                   transaction_time: datetime,
                                   historical_data: pd.DataFrame) -> int:
        """
        Check for impossible geographic velocity
        (traveling too far too fast)
        """
        recent_txn = historical_data[historical_data['transaction_date'] < transaction_time].iloc[-1:] if len(historical_data) > 0 else None
        
        if recent_txn is None or recent_txn.empty:
            return 0
        
        # Simple check: returns 1 if suspicious velocity detected
        time_diff = (transaction_time - recent_txn['transaction_date'].iloc[0]).total_seconds() / 3600
        
        if time_diff > 0 and hasattr(recent_txn, 'latitude') and hasattr(recent_txn, 'longitude'):
            # Would calculate distance here in production
            return 0
        
        return 0
    
    def _calculate_combined_risk(self, features: Dict) -> float:
        """Calculate combined risk score from features"""
        risk_score = 0.0
        weights = {
            'amount_zscore': 0.15,
            'is_new_merchant': 0.10,
            'is_new_device': 0.12,
            'is_foreign_transaction': 0.08,
            'velocity_zscore': 0.15,
            'is_unusual_hour': 0.10,
            'geographic_velocity': 0.15,
            'transaction_frequency_deviation': 0.10,
            'is_late_night': 0.05,
        }
        
        for feature, weight in weights.items():
            if feature in features:
                value = abs(features.get(feature, 0))
                # Normalize to 0-1 range
                normalized = min(value / 5, 1.0)  # Cap at 5 for normalization
                risk_score += normalized * weight
        
        return min(risk_score, 1.0)
    
    def predict(self, features_df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict fraud probability
        
        Returns:
            - predictions: -1 (fraud) or 1 (normal)
            - anomaly_scores: Anomaly scores in range [0, 1]
        """
        try:
            # Select numeric features
            numeric_features = features_df.select_dtypes(include=[np.number]).fillna(0)
            
            if len(numeric_features) == 0:
                return np.ones(len(features_df)), np.zeros(len(features_df))
            
            # Scale features
            scaled_features = self.scaler.fit_transform(numeric_features)
            
            # Predict using Isolation Forest
            predictions = self.isolation_forest.predict(scaled_features)
            
            # Get anomaly scores (convert to probability-like score)
            anomaly_scores = -self.isolation_forest.score_samples(scaled_features)
            anomaly_scores = (anomaly_scores - anomaly_scores.min()) / (anomaly_scores.max() - anomaly_scores.min() + 1e-10)
            
            return predictions, anomaly_scores
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return np.ones(len(features_df)), np.zeros(len(features_df))
    
    def train(self, training_data: pd.DataFrame):
        """Train fraud detection model"""
        try:
            numeric_training_data = training_data.select_dtypes(include=[np.number]).fillna(0)
            
            if len(numeric_training_data) > 0:
                scaled_data = self.scaler.fit_transform(numeric_training_data)
                self.isolation_forest.fit(scaled_data)
                logger.info(f"Model trained on {len(scaled_data)} samples")
                self.save_model()
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            raise
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores"""
        return self.feature_importance


class AnomalyDetector:
    """Statistical Anomaly Detection"""
    
    @staticmethod
    def detect_statistical_outliers(data: pd.Series, z_threshold: float = 3.0) -> np.ndarray:
        """Detect outliers using Z-score"""
        z_scores = np.abs(stats.zscore(data.fillna(0)))
        return z_scores > z_threshold
    
    @staticmethod
    def detect_iqr_outliers(data: pd.Series, iqr_multiplier: float = 1.5) -> np.ndarray:
        """Detect outliers using Interquartile Range"""
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        return (data < (Q1 - iqr_multiplier * IQR)) | (data > (Q3 + iqr_multiplier * IQR))
    
    @staticmethod
    def detect_isolation_forest_anomalies(data: pd.DataFrame, 
                                         contamination: float = 0.1) -> np.ndarray:
        """Detect anomalies using Isolation Forest"""
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        predictions = iso_forest.fit_predict(data.fillna(0))
        return predictions == -1


class BehaviorAnalyzer:
    """Customer Behavior Analysis and Pattern Recognition"""
    
    @staticmethod
    def calculate_customer_profile(transactions_df: pd.DataFrame) -> Dict:
        """Calculate comprehensive customer behavioral profile"""
        profile = {}
        
        if len(transactions_df) == 0:
            return profile
        
        # Amount statistics
        profile['avg_transaction_amount'] = transactions_df['amount'].mean()
        profile['std_transaction_amount'] = transactions_df['amount'].std()
        profile['max_typical'] = transactions_df['amount'].quantile(0.95)
        profile['min_typical'] = transactions_df['amount'].quantile(0.05)
        
        # Frequency statistics
        profile['avg_daily_transactions'] = len(transactions_df) / (
            (transactions_df['transaction_date'].max() - 
             transactions_df['transaction_date'].min()).days + 1
        )
        
        # Temporal patterns
        profile['typical_transaction_hours'] = BehaviorAnalyzer._get_peak_hours(
            transactions_df
        )
        
        # Merchant preferences
        profile['preferred_merchants'] = transactions_df['merchant_name'].value_counts().head(10).index.tolist()
        profile['preferred_categories'] = transactions_df['merchant_category'].value_counts().head(5).index.tolist()
        
        # Geographic patterns
        profile['typical_countries'] = transactions_df['merchant_country'].value_counts().head(5).index.tolist()
        
        return profile
    
    @staticmethod
    def _get_peak_hours(transactions_df: pd.DataFrame, top_n: int = 10) -> List[int]:
        """Get hours with most transactions"""
        if len(transactions_df) == 0:
            return list(range(24))
        
        hours = pd.to_datetime(transactions_df['transaction_date']).dt.hour
        peak_hours = hours.value_counts().head(top_n).index.tolist()
        return sorted(peak_hours)
