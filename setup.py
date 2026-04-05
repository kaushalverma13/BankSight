"""
Setup configuration for BankSight
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="BankSight",
    version="1.0.0",
    author="Banking Analytics Team",
    author_email="dev@banksight.ai",
    description="Transaction Intelligence Dashboard - Advanced Fraud Detection & Customer Analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/banksight/banksight",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Proprietary License",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "Intended Audience :: System Administrators",
    ],
    python_requires=">=3.11",
    install_requires=[
        "streamlit>=1.28.1",
        "pandas>=2.1.1",
        "numpy>=1.24.3",
        "sqlalchemy>=2.0.21",
        "psycopg2-binary>=2.9.9",
        "scikit-learn>=1.3.1",
        "plotly>=5.17.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.2",
            "pytest-cov>=4.1.0",
            "black>=23.9.1",
            "flake8>=6.1.0",
        ],
        "prod": [
            "gunicorn>=21.2.0",
            "uvicorn>=0.23.2",
        ],
    },
    entry_points={
        "console_scripts": [
            "banksight-init=init:main",
        ],
    },
)
