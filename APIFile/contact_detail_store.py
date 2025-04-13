import uuid
from flask import request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os 
import json




# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    firebase_credentials_str = os.getenv("FIREBASE_CREDENTIALS")
    firebase_credentials = json.loads(firebase_credentials_str)
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

def submit_automation_request():
    data = request.get_json()

    required_fields = [
        "li_at", "email", "password", "connection_degree", "keyword",
        "location", "sendconnectionrequest", "include_note", "letter"
    ]

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    entry_id = str(uuid.uuid4())
    db.collection('automatio_request_account').document(entry_id).set(data)

    return jsonify({"status": "success", "id": entry_id}), 200
