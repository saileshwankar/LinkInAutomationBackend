import uuid
from flask import request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os 
import json




# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    firebase_credentials = json.loads(os.getenv("FIREBASE_CREDENTIALS"))
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def submit_linkin_contact_data():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({"error": "All fields are required"}), 400

    contact_data = {
        "name": name,
        "email": email,
        "message": message
    }

    # Use Firestore's collection/document pattern
    entry_id = str(uuid.uuid4())
    db.collection('linkin_contact_data_page').document(entry_id).set(contact_data)

    return jsonify({"status": "success", "id": entry_id}), 200
