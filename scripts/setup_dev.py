#!/usr/bin/env python3
"""
Development environment setup script for RavenChain.
Creates necessary directories, generates test certificates, and sets up initial configuration.
"""
import os
import sys
from pathlib import Path
from config.logging import setup_logging

logger = setup_logging("ravenchain.setup")


def setup_development_environment():
    """Set up the development environment."""
    try:
        if not Path("venv").exists():
            logger.info("Creating virtual environment and installing dependencies")
            os.system("python -m venv venv")
            os.system("venv/Scripts/activate && pip install -r requirements.txt")
            logger.info("Created virtual environment and installed dependencies")
        # Create necessary directories
        directories = ["data", "logs", "backups", "certs", "config"]

        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")

        # Create development environment file if it doesn't exist
        env_file = Path(".env.development")
        if not env_file.exists():
            env_content = """# Development Environment Configuration
ENVIRONMENT=development
DEBUG=1
RAVENCHAIN_DATA_DIR=data
RAVENCHAIN_LOGS_DIR=logs
MINING_DIFFICULTY=2
LOG_LEVEL=DEBUG
LOG_JSON=1

# Database Configuration (for future use)
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=ravenchain
# DB_USER=ravenchain
# DB_PASSWORD=ravenchain

# API Configuration (for future use)
# API_HOST=0.0.0.0
# API_PORT=8000
# API_WORKERS=4
# CORS_ORIGINS=http://localhost:3000
"""
            env_file.write_text(env_content)
            logger.info("Created development environment file")

        # Create test SSL certificates for development
        if not Path("certs/dev.key").exists():
            os.system(
                "openssl req -x509 -newkey rsa:4096 -keyout certs/dev.key "
                "-out certs/dev.crt -days 365 -nodes "
                "-subj /CN=localhost/O=Development/OU=Engineering/C=US"
            )
            logger.info("Generated development SSL certificates")

        # Initialize git hooks if in a git repository
        git_dir = Path(".git")
        if git_dir.exists():
            hooks_dir = git_dir / "hooks"

            # Create pre-commit hook
            pre_commit = hooks_dir / "pre-commit"
            pre_commit_content = """#!/bin/sh
# Activate virtual environment
. "./venv/Scripts/activate"

echo "Running Black formatter..."
python -m black .

# Run tests if formatting passes
if [ $? -eq 0 ]; then
    echo "Running tests..."
    python -m pytest tests/
else
    echo "Black formatting failed. Please fix the formatting issues."
    exit 1
fi
"""
            pre_commit.write_text(pre_commit_content)
            pre_commit.chmod(0o755)
            logger.info("Set up git pre-commit hook")

        logger.info("Development environment setup complete")

    except Exception as e:
        logger.error("Setup failed", error=str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    setup_development_environment()
