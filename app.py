"""
BankSight: Transaction Intelligence Dashboard
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging
from config.settings import STREAMLIT_PAGE_CONFIG
from src.analytics.fraud_detection import FraudDetectionEngine, BehaviorAnalyzer
from src.analytics.analytics import (
    TransactionAnalytics, CustomerAnalytics, RiskScoring,
    TrendAnalysis, DataQualityMetrics
)
from src.utils.helpers import (
    Logger, NumberFormatting, DateTimeUtils, 
    SecurityUtils, CacheManager
)

# Configure logging
Logger.setup_logging()
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(**STREAMLIT_PAGE_CONFIG)

# Add custom CSS
def add_custom_css():
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77e6;
            margin-bottom: 1rem;
        }
        .metric-card {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77e6;
        }
        .alert-box {
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        .fraud-alert {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

add_custom_css()

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'transactions_df' not in st.session_state:
    st.session_state.transactions_df = None
if 'customers_df' not in st.session_state:
    st.session_state.customers_df = None


def load_sample_data():
    """Load or generate sample transaction data"""
    np.random.seed(42)
    
    # Generate sample customers
    n_customers = 100
    customers_data = {
        'id': range(1, n_customers + 1),
        'customer_id': [f'CUST_{i:05d}' for i in range(1, n_customers + 1)],
        'first_name': np.random.choice(['John', 'Jane', 'Bob', 'Alice', 'Charlie'], n_customers),
        'last_name': np.random.choice(['Smith', 'Johnson', 'Brown', 'Davis', 'Wilson'], n_customers),
        'email': [f'customer_{i}@bank.com' for i in range(1, n_customers + 1)],
        'risk_score': np.random.uniform(0, 1, n_customers),
        'kyc_verified': np.random.choice([True, False], n_customers, p=[0.8, 0.2]),
    }
    customers_df = pd.DataFrame(customers_data)
    
    # Generate sample transactions
    n_transactions = 2000
    transaction_types = ['DEBIT', 'CREDIT', 'TRANSFER', 'WITHDRAWAL']
    merchant_categories = ['RETAIL', 'FOOD', 'FUEL', 'ENTERTAINMENT', 'UTILITIES', 'HEALTHCARE', 'TRAVEL']
    merchants = ['Walmart', 'Target', 'McDonald\'s', 'Starbucks', 'Shell', 'Costco', 'Amazon', 'Netflix', 'hotel.com', 'United Airlines']
    countries = ['USA', 'UK', 'Canada', 'Mexico', 'Germany', 'France', 'Japan']
    
    transactions_data = {
        'transaction_id': [f'TXN_{i:08d}' for i in range(1, n_transactions + 1)],
        'customer_id': np.random.randint(1, n_customers + 1, n_transactions),
        'amount': np.random.exponential(100, n_transactions),
        'transaction_type': np.random.choice(transaction_types, n_transactions),
        'merchant_name': np.random.choice(merchants, n_transactions),
        'merchant_category': np.random.choice(merchant_categories, n_transactions),
        'merchant_country': np.random.choice(countries, n_transactions),
        'status': np.random.choice(['COMPLETED', 'PENDING', 'FAILED'], n_transactions, p=[0.9, 0.05, 0.05]),
        'fraud_score': np.random.uniform(0, 1, n_transactions),
        'is_flagged': np.random.choice([True, False], n_transactions, p=[0.05, 0.95]),
        'transaction_date': [datetime.now() - timedelta(days=np.random.randint(0, 90)) for _ in range(n_transactions)],
        'device_id': [f'DEV_{i % 50:04d}' for i in range(n_transactions)],
    }
    transactions_df = pd.DataFrame(transactions_data)
    
    st.session_state.customers_df = customers_df
    st.session_state.transactions_df = transactions_df
    st.session_state.data_loaded = True
    
    logger.info(f"Sample data loaded: {len(customers_df)} customers, {len(transactions_df)} transactions")


def main():
    """Main application"""
    
    # Header
    st.markdown("<div class='main-header'>💰 BankSight: Transaction Intelligence Dashboard</div>", unsafe_allow_html=True)
    st.markdown("Advanced Fraud Detection & Customer Analytics Platform")
    
    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Select View", [
            "Dashboard",
            "Fraud Detection",
            "Customer Analytics",
            "Risk Scoring",
            "Transaction Analysis",
            "Reports & Export",
            "Settings"
        ])
        
        st.divider()
        
        # Data loading
        st.subheader("Data Management")
        if st.button("Load Sample Data", use_container_width=True):
            load_sample_data()
            st.success("Sample data loaded!")
        
        if st.session_state.data_loaded:
            st.info(f"✓ {len(st.session_state.customers_df)} Customers\n✓ {len(st.session_state.transactions_df)} Transactions")
        
        st.divider()
        
        # Date range selector
        st.subheader("Filters")
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            key="date_range"
        )
    
    # Page routing
    if page == "Dashboard":
        show_dashboard()
    elif page == "Fraud Detection":
        show_fraud_detection()
    elif page == "Customer Analytics":
        show_customer_analytics()
    elif page == "Risk Scoring":
        show_risk_scoring()
    elif page == "Transaction Analysis":
        show_transaction_analysis()
    elif page == "Reports & Export":
        show_reports()
    elif page == "Settings":
        show_settings()


def show_dashboard():
    """Main Dashboard"""
    if not st.session_state.data_loaded:
        st.info("Please load sample data to get started.")
        return
    
    transactions_df = st.session_state.transactions_df
    customers_df = st.session_state.customers_df
    
    # KPI Metrics
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = TransactionAnalytics.get_transaction_summary(transactions_df)
    
    with col1:
        st.metric(
            "Total Transactions",
            f"{metrics.get('total_transactions', 0):,}"
        )
    
    with col2:
        st.metric(
            "Total Volume",
            NumberFormatting.format_currency(metrics.get('total_volume', 0))
        )
    
    with col3:
        st.metric(
            "Avg Transaction",
            NumberFormatting.format_currency(metrics.get('avg_transaction', 0))
        )
    
    with col4:
        flagged = len(transactions_df[transactions_df['is_flagged'] == True])
        st.metric(
            "Flagged Transactions",
            f"{flagged:,}",
            f"{(flagged / len(transactions_df) * 100):.2f}%"
        )
    
    with col5:
        unique_customers = transactions_df['customer_id'].nunique()
        st.metric(
            "Active Customers",
            f"{unique_customers:,}"
        )
    
    st.divider()
    
    # Daily Transaction Trend
    st.subheader("Daily Transaction Trend")
    daily_metrics = TransactionAnalytics.get_daily_metrics(transactions_df)
    
    if not daily_metrics.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_metrics.index,
            y=daily_metrics['total_amount'],
            mode='lines+markers',
            name='Total Amount'
        ))
        st.plotly_chart(fig, use_container_width=True)
    
    # Transaction Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Transaction Type Distribution")
        type_dist = transactions_df['transaction_type'].value_counts()
        fig = px.pie(values=type_dist.values, names=type_dist.index, title="By Type")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Transaction Status Distribution")
        status_dist = transactions_df['status'].value_counts()
        fig = px.pie(values=status_dist.values, names=status_dist.index, title="By Status")
        st.plotly_chart(fig, use_container_width=True)
    
    # Hourly Distribution
    st.subheader("Hourly Transaction Distribution")
    hourly_dist = TransactionAnalytics.get_hourly_distribution(transactions_df)
    
    if hourly_dist:
        transactions_df['hour'] = pd.to_datetime(transactions_df['transaction_date']).dt.hour
        hourly_count = transactions_df.groupby('hour').size()
        fig = px.bar(x=hourly_count.index, y=hourly_count.values, title="Transactions by Hour")
        fig.update_xaxes(title_text="Hour of Day")
        fig.update_yaxes(title_text="Transaction Count")
        st.plotly_chart(fig, use_container_width=True)


def show_fraud_detection():
    """Fraud Detection View"""
    if not st.session_state.data_loaded:
        st.info("Please load sample data to get started.")
        return
    
    st.subheader("Fraud Detection & Alerts")
    
    transactions_df = st.session_state.transactions_df
    fraud_engine = FraudDetectionEngine()
    
    # High-risk transactions
    high_risk = transactions_df[transactions_df['fraud_score'] > 0.7].sort_values('fraud_score', ascending=False)
    
    st.info(f"⚠️ {len(high_risk)} High-Risk Transactions Detected")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Flagged Transactions", len(transactions_df[transactions_df['is_flagged'] == True]))
    
    with col2:
        fraud_rate = (len(transactions_df[transactions_df['is_flagged'] == True]) / len(transactions_df) * 100)
        st.metric("Fraud Flag Rate", f"{fraud_rate:.2f}%")
    
    with col3:
        avg_fraud_score = transactions_df['fraud_score'].mean()
        st.metric("Avg Fraud Score", f"{avg_fraud_score:.3f}")
    
    st.divider()
    
    # Recent alerts
    st.subheader("High-Risk Transactions")
    if not high_risk.empty:
        display_cols = ['transaction_id', 'customer_id', 'amount', 'merchant_name', 'fraud_score', 'transaction_date']
        st.dataframe(
            high_risk[display_cols].head(20),
            use_container_width=True
        )
    
    st.divider()
    
    # Fraud Score Distribution
    st.subheader("Fraud Score Distribution")
    fig = px.histogram(transactions_df, x='fraud_score', nbins=50, title="Fraud Score Distribution")
    st.plotly_chart(fig, use_container_width=True)


def show_customer_analytics():
    """Customer Analytics View"""
    if not st.session_state.data_loaded:
        st.info("Please load sample data to get started.")
        return
    
    st.subheader("Customer Analytics & Segmentation")
    
    transactions_df = st.session_state.transactions_df
    customers_df = st.session_state.customers_df
    
    # Customer segmentation
    segments = CustomerAnalytics.segment_customers(customers_df, transactions_df)
    
    st.subheader("Customer Segments")
    col1, col2, col3, col4 = st.columns(4)
    
    for idx, (segment, count) in enumerate(segments.get('segment_summary', {}).items()):
        with [col1, col2, col3, col4][idx % 4]:
            st.metric(segment, count)
    
    st.divider()
    
    # Top customers by spending
    st.subheader("Top Customers by Spending")
    customer_spending = transactions_df.groupby('customer_id')['amount'].sum().sort_values(ascending=False).head(10)
    fig = px.bar(x=customer_spending.values, y=customer_spending.index, orientation='h', title="Top 10 Customers")
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Customer transaction frequency
    st.subheader("Customer Transaction Frequency")
    freq = transactions_df.groupby('customer_id').size().sort_values(ascending=False).head(10)
    fig = px.bar(x=freq.values, y=freq.index, orientation='h', title="Transaction Frequency - Top 10")
    st.plotly_chart(fig, use_container_width=True)


def show_risk_scoring():
    """Risk Scoring View"""
    if not st.session_state.data_loaded:
        st.info("Please load sample data to get started.")
        return
    
    st.subheader("Risk Scoring & Assessment")
    
    transactions_df = st.session_state.transactions_df
    customers_df = st.session_state.customers_df
    
    # Risk distribution
    st.subheader("Risk Score Distribution")
    fig = px.histogram(customers_df, x='risk_score', nbins=30, title="Customer Risk Scores")
    st.plotly_chart(fig, use_container_width=True)
    
    # High risk customers
    high_risk_customers = customers_df.nlargest(10, 'risk_score')
    
    st.subheader("High-Risk Customers")
    st.dataframe(
        high_risk_customers[['customer_id', 'first_name', 'last_name', 'risk_score', 'kyc_verified']],
        use_container_width=True
    )


def show_transaction_analysis():
    """Transaction Analysis View"""
    if not st.session_state.data_loaded:
        st.info("Please load sample data to get started.")
        return
    
    st.subheader("Transaction Analysis")
    
    transactions_df = st.session_state.transactions_df
    
    # Merchant analytics
    merchant_analytics = TransactionAnalytics.get_merchant_analytics(transactions_df)
    
    st.subheader("Top Merchants")
    if 'top_merchants' in merchant_analytics:
        top_merchants = pd.DataFrame(merchant_analytics['top_merchants']).T
        st.dataframe(top_merchants, use_container_width=True)
    
    st.divider()
    
    # Geographic distribution
    st.subheader("Geographic Distribution")
    geo_dist = TransactionAnalytics.get_geographic_distribution(transactions_df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("By Country")
        if geo_dist.get('countries'):
            fig = px.pie(values=list(geo_dist['countries'].values()), names=list(geo_dist['countries'].keys()))
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("By Category")
        category_dist = transactions_df['merchant_category'].value_counts()
        fig = px.bar(x=category_dist.values, y=category_dist.index, orientation='h')
        st.plotly_chart(fig, use_container_width=True)


def show_reports():
    """Reports & Export View"""
    st.subheader("Reports & Data Export")
    
    if not st.session_state.data_loaded:
        st.info("Please load sample data to get started.")
        return
    
    transactions_df = st.session_state.transactions_df
    customers_df = st.session_state.customers_df
    
    # Report selection
    report_type = st.selectbox(
        "Select Report Type",
        ["Transaction Summary", "Customer Summary", "Fraud Report", "Risk Assessment"]
    )
    
    # Export format
    export_format = st.selectbox("Export Format", ["CSV", "JSON", "Excel"])
    
    if st.button("Generate & Export Report"):
        if report_type == "Transaction Summary":
            st.dataframe(transactions_df, use_container_width=True)
        elif report_type == "Customer Summary":
            st.dataframe(customers_df, use_container_width=True)
        st.success("Report generated successfully!")


def show_settings():
    """Settings View"""
    st.subheader("Application Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Display Settings")
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        rows_per_page = st.slider("Rows per Page", 10, 100, 20)
    
    with col2:
        st.header("Alert Settings")
        fraud_threshold = st.slider("Fraud Score Threshold", 0.0, 1.0, 0.7)
        alert_volume = st.selectbox("Alert Volume", ["Low", "Medium", "High"])
    
    st.divider()
    
    st.header("Data Quality")
    if st.session_state.data_loaded:
        quality = DataQualityMetrics.assess_data_quality(st.session_state.transactions_df)
        st.metric("Overall Completeness", f"{quality.get('overall_completeness', 0):.2f}%")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("Field Completeness")
            completeness_data = quality.get('completeness_by_field', {})
            for field, pct in list(completeness_data.items())[:5]:
                st.write(f"{field}: {pct:.1f}%")


if __name__ == "__main__":
    main()
