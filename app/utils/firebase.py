import os
import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    # Correctly construct the path to the JSON file
    cred_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'callverse2-firebase-sdk.json')
    cred_path = os.path.abspath(cred_path)  # Ensure it's an absolute path
    cred = credentials.Certificate(cred_path)
    d  = firebase_admin.initialize_app(cred)
    print(firebase_admin._apps)
    print(firebase_admin.auth)

def get_firestore_client():
    return firestore.client()
