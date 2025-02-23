#!/usr/bin/env python3
"""
Backup script for RavenChain data and wallets.
Creates compressed backups with timestamps.
"""
import os
import shutil
import logging
from datetime import datetime
from pathlib import Path
from config.logging import setup_logging

logger = setup_logging("ravenchain.backup")


def create_backup(data_dir: str = "data", backup_dir: str = "backups"):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = Path(backup_dir) / f"ravenchain_backup_{timestamp}"

        # Create backup directory if it doesn't exist
        Path(backup_dir).mkdir(parents=True, exist_ok=True)

        # Create backup
        shutil.make_archive(
            str(backup_path),
            "gztar",
            data_dir,
        )

        logger.info(
            "Backup created successfully", backup_file=f"{backup_path}.tar.gz", timestamp=timestamp
        )

        # Clean old backups (keep last 5)
        cleanup_old_backups(backup_dir)

    except Exception as e:
        logger.error("Backup failed", error=str(e), exc_info=True)
        raise


def cleanup_old_backups(backup_dir: str, keep_last: int = 5):
    """Remove old backups, keeping only the specified number of recent ones."""
    try:
        backups = sorted(Path(backup_dir).glob("ravenchain_backup_*.tar.gz"), key=os.path.getmtime)

        # Remove old backups
        for backup in backups[:-keep_last]:
            backup.unlink()
            logger.info("Removed old backup", file=str(backup))

    except Exception as e:
        logger.error("Cleanup failed", error=str(e), exc_info=True)


if __name__ == "__main__":
    create_backup()
