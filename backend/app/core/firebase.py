# firebase.py
import firebase_admin
from firebase_admin import credentials, auth
import json
import os

def init_firebase():
    """Initialize Firebase only once."""
    if not firebase_admin._apps:
        firebase_creds = os.getenv("FIREBASE_CREDENTIALS")
        
        if not firebase_creds:
            print("FIREBASE_CREDENTIALS not set. Firebase auth will not work.")
            return
        
        try:
            # Parse the JSON string from environment variable
            cred_dict = json.loads(firebase_creds)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized successfully")
        except json.JSONDecodeError as e:
            print(f" Error parsing FIREBASE_CREDENTIALS: {e}")
            raise
        except Exception as e:
            print(f"Firebase initialization error: {e}")
            raise

# Initialize Firebase when module is imported
init_firebase()