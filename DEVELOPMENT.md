# Development Guide for BankSight

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Environment](#development-environment)
3. [Code Structure](#code-structure)
4. [Development Workflow](#development-workflow)
5. [Testing](#testing)
6. [Code Quality](#code-quality)
7. [Git Workflow](#git-workflow)
8. [Debugging](#debugging)

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Git
- Virtual Environment tools

### Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd BankSight

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install

# Initialize application
make init

# Copy environment variables
cp .env.example .env
# Edit .env with your configuration
```

## Development Environment

### Using Make Commands

```bash
# Install dependencies
make install

# Run application
make run

# Run tests
make test

# Format code
make format

# Lint code
make lint

# Clean generated files
make clean

# Initialize database
make init
```

### Docker Development

```bash
# Build and start containers
make docker

# View logs
make docker-logs

# Stop containers
make docker-down
```

## Code Structure

### Directory Organization

```
BankSight/
├── src/
│   ├── database/          # Database models and ORM
│   │   ├── __init__.py
│   │   ├── models.py      # SQLAlchemy models
│   │   └── connection.py  # Database connection
│   ├── analytics/         # Analytics engines
│   │   ├── __init__.py
│   │   ├── fraud_detection.py   # Fraud detection
│   │   └── analytics.py         # Analytics functions
│   └── utils/             # Utility functions
│       ├── __init__.py
│       └── helpers.py     # Helper functions
├── config/                # Configuration
│   ├── __init__.py
│   └── settings.py       # Application settings
├── tests/                 # Test suite
│   ├── __init__.py
│   └── test_main.py      # Main tests
├── app.py                # Streamlit main app
├── init.py               # Initialization script
└── requirements.txt      # Dependencies
```

## Development Workflow

### 1. Creating a New Feature

```bash
# Create feature branch
git checkout -b feature/fraud-detection-v2

# Make changes to code
# Add tests
# Format code
make format
make lint

# Run tests
make test

# Commit changes
git add .
git commit -m "Add improved fraud detection v2"

# Push branch
git push origin feature/fraud-detection-v2
```

### 2. Key Development Areas

#### Adding a New Fraud Detection Rule

```python
# In src/analytics/fraud_detection.py

class FraudDetectionEngine:
    def detect_new_pattern(self, transaction, customer_profile):
        """
        Detect a new fraud pattern
        
        Args:
            transaction: Transaction data
            customer_profile: Customer profile
            
        Returns:
            float: Fraud score [0, 1]
        """
        # Implementation here
        pass
```

#### Adding a New Analytics Function

```python
# In src/analytics/analytics.py

class TransactionAnalytics:
    @staticmethod
    def analyze_merchant_velocity(transactions_df, customer_id):
        """
        Analyze merchant transaction velocity
        """
        # Implementation here
        pass
```

#### Adding Database Models

```python
# In src/database/models.py

class NewModel(Base):
    __tablename__ = "new_models"
    
    id = Column(Integer, primary_key=True)
    # Add your columns
```

### 3. API Development

```python
# Creating new API endpoints (if using Flask)

from flask import Flask, jsonify
from src.analytics.analytics import TransactionAnalytics

app = Flask(__name__)

@app.route('/api/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """Get analytics summary"""
    # Implementation
    return jsonify(summary)
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_main.py

# Run with coverage
pytest --cov=src tests/

# Run specific test class
pytest tests/test_main.py::TestFraudDetectionEngine

# Run with verbose output
pytest -v
```

### Writing Tests

```python
import pytest
from src.analytics.fraud_detection import FraudDetectionEngine

class TestFraudDetectionEngine:
    
    @pytest.fixture
    def engine(self):
        """Setup fixture"""
        return FraudDetectionEngine()
    
    def test_feature_extraction(self, engine):
        """Test feature extraction"""
        # Arrange
        transaction = {'amount': 100.0}
        profile = {'avg_transaction_amount': 50.0}
        
        # Act
        features = engine.extract_features(transaction, profile)
        
        # Assert
        assert 'amount' in features
```

### Test Coverage

```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# View report
open htmlcov/index.html
```

## Code Quality

### Linting

```bash
# Run flake8
flake8 src/

# Run pylint
pylint src/

# Show all issues
flake8 src/ --count --show-source
```

### Code Formatting

```bash
# Format with black
black src/ tests/ --line-length=120

# Check formatting
black --check src/

# Sort imports
isort src/
```

### Type Checking

```bash
# Run mypy
mypy src/ --ignore-missing-imports
```

## Git Workflow

### Branch Naming Convention

```
feature/describe-feature    # New feature
bugfix/describe-bug         # Bug fix
hotfix/describe-hotfix      # Production hotfix
refactor/describe-change    # Code refactoring
docs/describe-docs          # Documentation
```

### Commit Message Convention

```
[TYPE] Brief description

Detailed explanation if needed.

Fixes: #123
Related to: #456
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `perf`

```bash
# Good commit messages
git commit -m "[feat] Add new fraud detection model"
git commit -m "[fix] Fix transaction parsing bug"
git commit -m "[docs] Update API documentation"
git commit -m "[refactor] Simplify CustomerAnalytics class"
```

## Debugging

### Using Print Debugging

```python
import logging

logger = logging.getLogger(__name__)

def my_function():
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
```

### Using Python Debugger

```python
import pdb

def my_function():
    x = 10
    pdb.set_trace()  # Execution stops here
    # Commands: n (next), s (step), c (continue), l (list), p (print)
```

### Database Debugging

```python
from src.database.connection import DatabaseManager

with DatabaseManager.session_scope() as session:
    result = session.query(Transaction).filter(...).all()
    print(result)
```

### Streamlit Debugging

```python
import streamlit as st

st.write("Debug output:", my_variable)
st.json(json_data)
st.dataframe(df)
```

## Performance Optimization

### Profiling

```python
from src.utils.helpers import PerformanceUtils

@PerformanceUtils.timing_decorator
def slow_function():
    # This will log execution time
    pass

@PerformanceUtils.memory_profiler
def memory_intensive_function():
    # This will profile memory usage
    pass
```

### Database Query Optimization

```python
# Use indexes
# Use lazy loading
# Batch operations
# Cache results

from src.utils.helpers import CacheManager

# Cache results
CacheManager.set('key', value, ttl=3600)
cached = CacheManager.get('key')
```

## Documentation

### Docstring Format

```python
def extract_features(transaction: Dict, customer_profile: Dict) -> Dict:
    """
    Extract features for fraud detection.
    
    Args:
        transaction: Transaction data dictionary
        customer_profile: Customer profile data
        
    Returns:
        Dictionary of extracted features
        
    Raises:
        ValueError: If transaction data is invalid
        
    Examples:
        >>> features = extract_features(txn, profile)
        >>> print(features['fraud_score'])
    """
    pass
```

## Deployment Checklist

- [ ] All tests pass
- [ ] Code is formatted with black
- [ ] No linting errors
- [ ] Type checking passes
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version bumped
- [ ] Database migrations created (if needed)
- [ ] Environment variables documented
- [ ] Security review completed

## Useful Resources

- [Python Documentation](https://docs.python.org/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pytest Documentation](https://pytest.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [scikit-learn Documentation](https://scikit-learn.org/)

## Support

For questions or issues:
1. Check existing documentation
2. Search GitHub issues
3. Create a new issue with details
4. Contact the development team

---

**Last Updated**: 2024
**Maintained By**: Banking Analytics Team
