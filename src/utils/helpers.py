"""
Utility Functions and Helpers for BankSight
"""

import logging
import hashlib
import secrets
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import json
import csv
import io
from functools import wraps
import time

logger = logging.getLogger(__name__)


class Logger:
    """Centralized logging configuration"""
    
    @staticmethod
    def setup_logging(log_file: str = None, level: str = "INFO"):
        """Setup application logging"""
        logging.basicConfig(
            level=getattr(logging, level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_file) if log_file else logging.NullHandler()
            ]
        )


class SecurityUtils:
    """Security-related utilities"""
    
    @staticmethod
    def hash_sensitive_data(data: str, salt: str = None) -> str:
        """Hash sensitive data"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        hash_obj = hashlib.pbkdf2_hmac('sha256', data.encode(), salt.encode(), 100000)
        return salt + hash_obj.hex()
    
    @staticmethod
    def mask_card_number(card_number: str) -> str:
        """Mask credit card number"""
        if len(card_number) < 4:
            return "****"
        return "****" + card_number[-4:]
    
    @staticmethod
    def mask_email(email: str) -> str:
        """Mask email address"""
        parts = email.split('@')
        if len(parts[0]) > 2:
            masked = parts[0][0] + '*' * (len(parts[0]) - 2) + parts[0][-1]
        else:
            masked = '*' * len(parts[0])
        return masked + '@' + parts[1]
    
    @staticmethod
    def sanitize_input(user_input: str, max_length: int = 255) -> str:
        """Sanitize user input"""
        # Remove potentially harmful characters
        dangerous_chars = ['<', '>', '"', "'", ';', '(', ')', '{', '}']
        sanitized = user_input
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized[:max_length]


class DataExport:
    """Data export utilities"""
    
    @staticmethod
    def export_to_csv(data: List[Dict]) -> bytes:
        """Export data to CSV format"""
        if not data:
            return b""
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        
        return output.getvalue().encode()
    
    @staticmethod
    def export_to_json(data: Any) -> str:
        """Export data to JSON format"""
        return json.dumps(data, indent=2, default=str)
    
    @staticmethod
    def export_dataframe_to_excel(df, filename: str):
        """Export DataFrame to Excel"""
        try:
            import openpyxl
            df.to_excel(filename, index=False)
            logger.info(f"Data exported to {filename}")
        except ImportError:
            logger.error("openpyxl not installed")


class DateTimeUtils:
    """DateTime utilities"""
    
    @staticmethod
    def get_date_range(start: str, end: str, format: str = "%Y-%m-%d"):
        """Parse date range"""
        from datetime import datetime as dt
        start_date = dt.strptime(start, format)
        end_date = dt.strptime(end, format)
        return start_date, end_date
    
    @staticmethod
    def get_relative_date(days: int = 0, months: int = 0, years: int = 0):
        """Get date relative to today"""
        from datetime import datetime, timedelta
        from dateutil.relativedelta import relativedelta
        
        return datetime.now() - relativedelta(days=days, months=months, years=years)
    
    @staticmethod
    def format_datetime(dt_obj: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Format datetime object"""
        return dt_obj.strftime(format)


class ValidationUtils:
    """Data validation utilities"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number"""
        import re
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_amount(amount: float, min_val: float = 0, max_val: float = 1000000) -> bool:
        """Validate transaction amount"""
        try:
            amount = float(amount)
            return min_val <= amount <= max_val
        except (TypeError, ValueError):
            return False
    
    @staticmethod
    def validate_required_fields(data: Dict, required_fields: List[str]) -> Tuple[bool, List[str]]:
        """Validate required fields in dictionary"""
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        return len(missing_fields) == 0, missing_fields


class PerformanceUtils:
    """Performance monitoring utilities"""
    
    @staticmethod
    def timing_decorator(func):
        """Decorator to measure function execution time"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            logger.info(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
            return result
        return wrapper
    
    @staticmethod
    def memory_profiler(func):
        """Decorator to profile memory usage"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                import tracemalloc
                tracemalloc.start()
                result = func(*args, **kwargs)
                current, peak = tracemalloc.get_traced_memory()
                logger.info(f"{func.__name__} - Current memory: {current / 1e6:.2f}MB, Peak: {peak / 1e6:.2f}MB")
                tracemalloc.stop()
                return result
            except ImportError:
                logger.warning("tracemalloc not available")
                return func(*args, **kwargs)
        return wrapper


class NumberFormatting:
    """Number formatting utilities"""
    
    @staticmethod
    def format_currency(amount: float, currency: str = "USD", decimals: int = 2) -> str:
        """Format amount as currency"""
        symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
        }
        symbol = symbols.get(currency, '$')
        return f"{symbol}{amount:,.{decimals}f}"
    
    @staticmethod
    def format_percentage(value: float, decimals: int = 2) -> str:
        """Format as percentage"""
        return f"{value:.{decimals}f}%"
    
    @staticmethod
    def format_large_number(number: float) -> str:
        """Format large numbers (e.g., 1M, 1K)"""
        if abs(number) >= 1e9:
            return f"{number / 1e9:.2f}B"
        elif abs(number) >= 1e6:
            return f"{number / 1e6:.2f}M"
        elif abs(number) >= 1e3:
            return f"{number / 1e3:.2f}K"
        else:
            return f"{number:.2f}"


class CacheManager:
    """Simple in-memory cache manager"""
    
    _cache = {}
    
    @classmethod
    def set(cls, key: str, value: Any, ttl: int = 3600):
        """Set cache value with TTL"""
        cls._cache[key] = {
            'value': value,
            'expires_at': datetime.now() + datetime.timedelta(seconds=ttl)
        }
    
    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        """Get cache value if not expired"""
        if key in cls._cache:
            cache_entry = cls._cache[key]
            if datetime.now() < cache_entry['expires_at']:
                return cache_entry['value']
            else:
                del cls._cache[key]
        return None
    
    @classmethod
    def clear(cls):
        """Clear all cache"""
        cls._cache.clear()
    
    @classmethod
    def remove(cls, key: str):
        """Remove specific cache entry"""
        if key in cls._cache:
            del cls._cache[key]


from datetime import timedelta
ValidationUtils.validate_required_fields.__annotations__ = {
    'data': Dict,
    'required_fields': List[str],
    'return': Tuple[bool, List[str]]
}
