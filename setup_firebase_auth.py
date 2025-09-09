#!/usr/bin/env python3
"""
Firebase Authentication Setup Script for AIDEN
This script helps set up Firebase authentication using the provided web app configuration.
"""

import json
import os
from pathlib import Path

def create_service_account_instructions():
    """Create instructions for setting up Firebase service account"""
    
    instructions = """
🔥 FIREBASE AUTHENTICATION SETUP FOR AIDEN 🔥

The Firebase configuration is already set up in AIDEN, but you need to provide authentication credentials.

📋 OPTION 1: Service Account Key (Recommended)
============================================

1. Go to Firebase Console: https://console.firebase.google.com/
2. Select your project: aiden-dd627
3. Go to Project Settings (gear icon) → Service accounts
4. Click "Generate new private key"
5. Download the JSON file 
6. Rename it to 'serviceAccountKey.json'
7. Place it in the AIDEN directory: {}/serviceAccountKey.json

📋 OPTION 2: Environment Variable
================================

1. Download the service account key as above
2. Set environment variable:
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/serviceAccountKey.json"

📋 OPTION 3: Google Cloud SDK
=============================

1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
2. Run: gcloud auth application-default login
3. Follow the authentication flow

📋 OPTION 4: Demo Mode (Local Storage Only)
===========================================

If you can't set up Firebase authentication, AIDEN will automatically fall back to local storage.
All conversations and data will be saved as JSON files in the current directory.

🔧 CURRENT STATUS
================
""".format(os.getcwd())

    # Check current Firebase status
    try:
        from firebase_integration import get_firebase_manager
        fm = get_firebase_manager()
        if fm.connected:
            instructions += "✅ Firebase is connected and working!\n"
        else:
            instructions += "❌ Firebase authentication needed\n"
    except Exception as e:
        instructions += f"❌ Firebase test failed: {e}\n"

    # Check for existing credentials
    service_account_file = Path("serviceAccountKey.json")
    if service_account_file.exists():
        instructions += "✅ Service account key file found: serviceAccountKey.json\n"
    else:
        instructions += "❌ No service account key file found\n"

    google_creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if google_creds:
        instructions += f"✅ Environment variable set: {google_creds}\n"
    else:
        instructions += "❌ GOOGLE_APPLICATION_CREDENTIALS not set\n"

    instructions += """
🚀 QUICK TEST
=============

After setting up credentials, test Firebase with:
    python3 -c "from firebase_integration import get_firebase_manager; fm = get_firebase_manager(); print('Connected:', fm.connected)"

📚 MORE HELP
============

- Firebase Admin SDK setup: https://firebase.google.com/docs/admin/setup
- Service account key guide: https://firebase.google.com/docs/admin/setup#initialize_the_sdk
- Troubleshooting: https://firebase.google.com/docs/admin/setup#troubleshooting

"""
    
    print(instructions)

def create_demo_service_account():
    """Create a demo service account template"""
    
    template = {
        "type": "service_account",
        "project_id": "aiden-dd627",
        "private_key_id": "REPLACE_WITH_ACTUAL_KEY_ID",
        "private_key": "-----BEGIN PRIVATE KEY-----\\nREPLACE_WITH_ACTUAL_PRIVATE_KEY\\n-----END PRIVATE KEY-----\\n",
        "client_email": "firebase-adminsdk-XXXXX@aiden-dd627.iam.gserviceaccount.com",
        "client_id": "REPLACE_WITH_CLIENT_ID",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-XXXXX%40aiden-dd627.iam.gserviceaccount.com"
    }
    
    with open('serviceAccountKey.json.template', 'w') as f:
        json.dump(template, f, indent=2)
    
    print("📝 Created serviceAccountKey.json.template")
    print("   Replace the placeholder values with your actual Firebase service account data")

if __name__ == "__main__":
    print("🤖 AIDEN Firebase Authentication Setup")
    print("=" * 50)
    
    create_service_account_instructions()
    
    # Ask if user wants to create template
    try:
        response = input("\nCreate service account template file? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            create_demo_service_account()
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled")
    
    print("\n🎉 Setup complete! Follow the instructions above to enable Firebase.")