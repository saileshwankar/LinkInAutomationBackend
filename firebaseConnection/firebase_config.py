import firebase_admin
from firebase_admin import credentials, db

firebase_initialized = False

def init_firebase():
    global firebase_initialized
    if not firebase_initialized:
        try:
            cred = credentials.Certificate("C:/Users/ADMIN/Desktop/LinkinAutomation/BackendLinkedAutomation/firebasecred.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://linkinautomationbackend-default-rtdb.firebaseio.com/'
            })
            firebase_initialized = True
            print("Firebase Initialized Successfully.")
        except Exception as e:
            print(f"Error initializing Firebase: {e}")

# Call this method before any database operations
