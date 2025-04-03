import os

def ensure_uploads_dir():
    """Ensure the uploads directory exists"""
    os.makedirs("uploads", exist_ok=True)
    return "uploads"