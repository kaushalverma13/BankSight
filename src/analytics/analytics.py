"""
Data Analytics and Statistical Analysis Module
Comprehensive financial analytics for BankSight Dashboard
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


class TransactionAnalytics:
    """Transaction-level Analytics"""
    
    @staticmethod
    def get_transaction_summary(transactions_df: pd.DataFrame) -> Dict:
        """Get comprehensive transaction summary"""
        if transactions_df.empty:
            return {}
        
        return {
            'total_transactions': len(transactions_df),
            'total_volume': transactions_df['amount'].sum(),
            'avg_transaction': transactions_df['amount'].mean(),
            'median_transaction': transactions_df['amount'].median(),
            'max_transaction': transactions_df['amount'].max(),
            'min_transaction': transactions_df['amount'].min(),
            'std_deviation': transactions_df['amount'].std(),
            'transaction_count_by_type': transactions_df['transaction_type'].value_counts().to_dict(),
            'transaction_count_by_status': transactions_df['status'].value_counts().to_dict(),
        }
    
    @staticmethod
    def get_daily_metrics(transactions_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate daily transaction metrics"""
        if transactions_df.empty:
            return pd.DataFrame()
        
        transactions_df['date'] = pd.to_datetime(transactions_df['transaction_date']).dt.date
        
        daily_metrics = transactions_df.groupby('date').agg({
            'amount': ['sum', 'mean', 'count', 'std'],
            'transaction_id': 'count',
        }).round(2)
        
        daily_metrics.columns = ['total_amount', 'avg_amount', 'count', 'std', 'transaction_count']
        return daily_metrics
    
    @staticmethod
    def get_hourly_distribution(transactions_df: pd.DataFrame) -> Dict:
        """Analyze transaction distribution by hour"""
        if transactions_df.empty:
            return {}
        
        transactions_df['hour'] = pd.to_datetime(transactions_df['transaction_date']).dt.hour
        
        hourly_dist = transactions_df.groupby('hour').agg({
            'amount': ['sum', 'count', 'mean']
        }).round(2)
        
        return {
            'by_hour': hourly_dist.to_dict(),
            'peak_hours': transactions_df['hour'].value_counts().head(5).index.tolist(),
            'quiet_hours': transactions_df['hour'].value_counts().tail(5).index.tolist(),
        }
    
    @staticmethod
    def get_merchant_analytics(transactions_df: pd.DataFrame, top_n: int = 20) -> Dict:
        """Analyze merchant-level metrics"""
        if transactions_df.empty:
            return {}
        
        merchant_stats = transactions_df.groupby('merchant_name').agg({
            'amount': ['sum', 'count', 'mean'],
            'merchant_category': 'first',
        }).round(2)
        
        merchant_stats.columns = ['total_volume', 'transaction_count', 'avg_amount', 'category']
        merchant_stats = merchant_stats.sort_values('total_volume', ascending=False).head(top_n)
        
        return {
            'top_merchants': merchant_stats.to_dict('index'),
            'total_unique_merchants': transactions_df['merchant_name'].nunique(),
            'merchant_categories': transactions_df.groupby('merchant_category').size().to_dict(),
        }
    
    @staticmethod
    def get_geographic_distribution(transactions_df: pd.DataFrame) -> Dict:
        """Analyze geographic transaction patterns"""
        if transactions_df.empty:
            return {}
        
        return {
            'countries': transactions_df['merchant_country'].value_counts().to_dict(),
            'cities': transactions_df['merchant_city'].value_counts().head(20).to_dict(),
            'total_countries': transactions_df['merchant_country'].nunique(),
            'total_cities': transactions_df['merchant_city'].nunique(),
        }


class CustomerAnalytics:
    """Customer-level Analytics and Segmentation"""
    
    @staticmethod
    def get_customer_metrics(customer_id: int, transactions_df: pd.DataFrame) -> Dict:
        """Get individual customer metrics"""
        customer_txns = transactions_df[transactions_df['customer_id'] == customer_id]
        
        if customer_txns.empty:
            return {}
        
        return {
            'customer_id': customer_id,
            'total_transactions': len(customer_txns),
            'total_spending': customer_txns['amount'].sum(),
            'avg_spending': customer_txns['amount'].mean(),
            'transaction_frequency': len(customer_txns) / (
                (customer_txns['transaction_date'].max() - 
                 customer_txns['transaction_date'].min()).days + 1
            ),
            'first_transaction': customer_txns['transaction_date'].min(),
            'last_transaction': customer_txns['transaction_date'].max(),
            'unique_merchants': customer_txns['merchant_name'].nunique(),
            'unique_categories': customer_txns['merchant_category'].nunique(),
            'unique_countries': customer_txns['merchant_country'].nunique(),
            'transaction_types': customer_txns['transaction_type'].value_counts().to_dict(),
        }
    
    @staticmethod
    def segment_customers(customers_df: pd.DataFrame, transactions_df: pd.DataFrame) -> Dict:
        """Segment customers based on transaction patterns"""
        segments = {}
        
        for customer_id in transactions_df['customer_id'].unique():
            metrics = CustomerAnalytics.get_customer_metrics(customer_id, transactions_df)
            
            if not metrics:
                continue
            
            spending = metrics['total_spending']
            frequency = metrics['transaction_frequency']
            
            # RFM-based segmentation
            if spending > transactions_df['amount'].quantile(0.75) and frequency > transactions_df.groupby('customer_id').size().quantile(0.75):
                segment = 'VIP'
            elif spending < transactions_df['amount'].quantile(0.25):
                segment = 'Low-Value'
            elif frequency < 0.5:
                segment = 'Dormant'
            else:
                segment = 'Regular'
            
            if segment not in segments:
                segments[segment] = []
            
            segments[segment].append(customer_id)
        
        return {
            'segments': segments,
            'segment_summary': {seg: len(customers) for seg, customers in segments.items()}
        }
    
    @staticmethod
    def identify_high_risk_customers(transactions_df: pd.DataFrame, 
                                     fraud_threshold: float = 0.7) -> List[int]:
        """Identify customers with highest fraud risk"""
        customer_fraud = transactions_df[transactions_df['fraud_score'] > fraud_threshold].groupby('customer_id').size()
        return customer_fraud.nlargest(20).index.tolist()
    
    @staticmethod
    def get_customer_lifetime_value(customer_id: int, 
                                   transactions_df: pd.DataFrame) -> Dict:
        """Calculate Customer Lifetime Value"""
        customer_txns = transactions_df[transactions_df['customer_id'] == customer_id]
        
        if customer_txns.empty:
            return {}
        
        total_value = customer_txns['amount'].sum()
        txn_count = len(customer_txns)
        days_active = (customer_txns['transaction_date'].max() - 
                       customer_txns['transaction_date'].min()).days + 1
        
        return {
            'customer_id': customer_id,
            'total_lifetime_value': total_value,
            'transaction_count': txn_count,
            'days_active': days_active,
            'daily_average': total_value / days_active,
            'estimated_annual_value': (total_value / days_active) * 365 if days_active > 0 else 0,
        }


class RiskScoring:
    """Risk Assessment and Scoring"""
    
    @staticmethod
    def calculate_risk_score(customer: Dict, transactions_df: pd.DataFrame) -> Dict:
        """Calculate comprehensive risk score"""
        risk_components = {}
        
        # Behavioral risk
        if 'avg_transaction_amount' in customer:
            risk_components['behavioral_risk'] = min(
                abs(customer['avg_transaction_amount']) / 10000 if customer['avg_transaction_amount'] > 0 else 0,
                1.0
            )
        
        # Geographic risk
        countries = transactions_df['merchant_country'].nunique()
        risk_components['geographic_risk'] = min(countries / 50, 1.0)  # Normalized to 50 countries
        
        # Temporal risk
        hours = pd.to_datetime(transactions_df['transaction_date']).dt.hour.nunique()
        risk_components['temporal_risk'] = hours / 24
        
        # Merchant diversity risk
        merchants = transactions_df['merchant_name'].nunique()
        risk_components['merchant_risk'] = min(merchants / 100, 1.0)
        
        # Frequency risk
        txn_per_day = len(transactions_df) / (
            (transactions_df['transaction_date'].max() - 
             transactions_df['transaction_date'].min()).days + 1
        )
        risk_components['frequency_risk'] = min(txn_per_day / 50, 1.0)
        
        # Overall risk score (weighted average)
        weights = {
            'behavioral_risk': 0.25,
            'geographic_risk': 0.20,
            'temporal_risk': 0.15,
            'merchant_risk': 0.20,
            'frequency_risk': 0.20,
        }
        
        overall_risk = sum(risk_components.get(k, 0) * v for k, v in weights.items())
        
        # Classify risk level
        if overall_risk < 0.33:
            risk_level = 'LOW'
        elif overall_risk < 0.66:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'HIGH'
        
        return {
            'components': risk_components,
            'overall_score': round(overall_risk, 3),
            'risk_level': risk_level,
        }
    
    @staticmethod
    def identify_high_risk_transactions(transactions_df: pd.DataFrame,
                                       risk_threshold: float = 0.7) -> pd.DataFrame:
        """Identify transactions with high risk scores"""
        return transactions_df[transactions_df['fraud_score'] > risk_threshold].sort_values(
            'fraud_score', ascending=False
        )


class TrendAnalysis:
    """Trend Analysis and Forecasting"""
    
    @staticmethod
    def get_transaction_trends(transactions_df: pd.DataFrame, 
                              days: int = 30) -> Dict:
        """Analyze transaction trends"""
        end_date = pd.to_datetime(transactions_df['transaction_date']).max()
        start_date = end_date - timedelta(days=days)
        
        trend_data = transactions_df[
            pd.to_datetime(transactions_df['transaction_date']) >= start_date
        ].copy()
        
        trend_data['date'] = pd.to_datetime(trend_data['transaction_date']).dt.date
        daily_trend = trend_data.groupby('date')['amount'].agg(['sum', 'count']).reset_index()
        
        return {
            'trend_data': daily_trend.to_dict('records'),
            'trend_direction': 'up' if daily_trend['sum'].iloc[-1] > daily_trend['sum'].iloc[0] else 'down',
            'growth_rate': (daily_trend['sum'].iloc[-1] - daily_trend['sum'].iloc[0]) / daily_trend['sum'].iloc[0] * 100,
            'average_daily_volume': daily_trend['sum'].mean(),
        }
    
    @staticmethod
    def get_fraud_trends(transactions_df: pd.DataFrame,
                        days: int = 30) -> Dict:
        """Analyze fraud trends"""
        end_date = pd.to_datetime(transactions_df['transaction_date']).max()
        start_date = end_date - timedelta(days=days)
        
        fraud_data = transactions_df[
            (pd.to_datetime(transactions_df['transaction_date']) >= start_date) &
            (transactions_df['is_flagged'] == True)
        ].copy()
        
        fraud_data['date'] = pd.to_datetime(fraud_data['transaction_date']).dt.date
        daily_fraud = fraud_data.groupby('date').size().reset_index(name='count')
        
        return {
            'fraud_trend': daily_fraud.to_dict('records'),
            'total_flagged': len(fraud_data),
            'fraud_rate': (len(fraud_data) / len(transactions_df) * 100) if len(transactions_df) > 0 else 0,
        }


class DataQualityMetrics:
    """Data Quality and Completeness Metrics"""
    
    @staticmethod
    def assess_data_quality(df: pd.DataFrame) -> Dict:
        """Assess data quality metrics"""
        total_records = len(df)
        total_fields = len(df.columns)
        
        quality_metrics = {
            'total_records': total_records,
            'total_fields': total_fields,
            'completeness_by_field': {},
            'null_percentage': {},
            'duplicate_records': df.duplicated().sum(),
            'overall_completeness': 0.0,
        }
        
        total_nulls = 0
        for column in df.columns:
            null_count = df[column].isnull().sum()
            completeness = ((total_records - null_count) / total_records * 100) if total_records > 0 else 0
            
            quality_metrics['completeness_by_field'][column] = round(completeness, 2)
            quality_metrics['null_percentage'][column] = round((null_count / total_records * 100) if total_records > 0 else 0, 2)
            
            total_nulls += null_count
        
        overall_completeness = ((total_records * total_fields - total_nulls) / (total_records * total_fields) * 100) if (total_records * total_fields) > 0 else 0
        quality_metrics['overall_completeness'] = round(overall_completeness, 2)
        
        return quality_metrics
