"""
rejection_log.py

Purpose:
- Track and persist information about rejected or suspicious records
- Maintain transparency in the data cleaning process
- Support reporting and auditability

This module does NOT clean data.
It ONLY logs metadata about rejected rows.
"""

import os
import csv
from datetime import datetime


# -----------------------------
# Log file location
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "..", "data", "logs")
LOG_FILE = os.path.join(LOG_DIR, "rejection_log.csv")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)


# -----------------------------
# Initialize log file
# -----------------------------
def _initialize_log():
    """
    Creates the rejection log file with headers if it does not exist.
    """
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "reason",
                "rejected_count"
            ])


_initialize_log()


# -----------------------------
# Log rejection event
# -----------------------------
def log_rejections(reason: str, count: int):
    """
    Appends a rejection event to the log file.

    Parameters:
    - reason (str): Why records were rejected
    - count (int): Number of rows rejected
    """
    if count <= 0:
        return

    timestamp = datetime.utcnow().isoformat()

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            reason,
            count
        ])

    print(f"Logged rejection → {reason}: {count}")
