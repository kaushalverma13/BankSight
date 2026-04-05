"""
BankSight - Transaction Intelligence Dashboard
Version 1.0.0
"""

__version__ = "1.0.0"
__author__ = "BankSight Development Team"
__email__ = "dev@banksight.ai"

# Load configuration
try:
    from config.settings import *
except ImportError:
    pass
