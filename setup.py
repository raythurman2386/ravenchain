from setuptools import setup, find_packages

setup(
    name="ravenchain",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ecdsa>=0.18.0",
        "base58>=2.1.1",
        "fastapi>=0.115.8",
        "uvicorn>=0.27.0",
        "sqlalchemy>=2.0.38",
        "alembic>=1.13.0",
        "psycopg2-binary>=2.9.10",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "slowapi>=0.1.9",
        "pydantic>=2.1.1",
        "pydantic-core>=2.7.0",
        "pydantic[email]>=2.1.1",
    ],
    extras_require={
        "test": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.23.0",
            "httpx>=0.26.0",  # For testing FastAPI endpoints
            "python-dotenv>=1.0.0",  # For loading environment variables
        ],
        "dev": [
            "black>=25.0.0",
            "isort>=5.13.0",
            "flake8>=7.0.0",
        ],
    },
)
