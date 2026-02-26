# backend/config.py
import os
from pathlib import Path

class Config:
    # Get the base directory (backend folder) - this creates an ABSOLUTE path
    BASE_DIR = Path(__file__).resolve().parent
    

    LOGO_PATH = os.path.abspath(os.path.join(BASE_DIR, "static", "images", "Image111.bmp"))
    
    @classmethod
    def get_logo_path(cls):
        """Safe method to get logo path with error checking"""
        if os.path.exists(cls.LOGO_PATH):
            print(f"Logo found at: {cls.LOGO_PATH}")
            return cls.LOGO_PATH
        else:
            print(f"Warning: Logo not found at {cls.LOGO_PATH}")
            # Return None if logo not found
            return None