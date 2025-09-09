# 🔥 Firebase Setup for AIDEN

AIDEN is pre-configured to work with Firebase Realtime Database for persistent data storage. However, Firebase requires authentication to access the database.

## Current Status

✅ Firebase configuration is already set up
✅ Local storage fallback is working
❌ Firebase authentication needs to be configured

## Quick Fix Options

### Option 1: Use Local Storage (No Setup Required)
AIDEN automatically falls back to local JSON storage when Firebase is unavailable. All features work normally, but data is stored locally only.

**Files created:**
- `aiden_conversations_YYYYMMDD.json` - Chat conversations
- `aiden_searches_YYYYMMDD.json` - Search results  
- `aiden_voice_profiles_USER.json` - Voice learning data

### Option 2: Set Up Firebase (Recommended for Cloud Storage)

#### Step 1: Get Service Account Key
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select project: **aiden-dd627**
3. Go to Project Settings (⚙️) → Service accounts
4. Click "Generate new private key"
5. Download the JSON file
6. Rename it to `serviceAccountKey.json`
7. Place it in the AIDEN directory

#### Step 2: Test Connection
```bash
python3 -c "from firebase_integration import get_firebase_manager; fm = get_firebase_manager(); print('Connected:', fm.connected)"
```

#### Alternative: Environment Variable
Instead of placing the file in the directory, you can set an environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/serviceAccountKey.json"
```

## Firebase Configuration Details

The Firebase project is already configured with:
- **Project ID:** aiden-dd627
- **Database URL:** https://aiden-dd627-default-rtdb.firebaseio.com/
- **API Key:** AIzaSyDe1tIF0RDqotZVqzV1o77utir_nl2XMSc

## Testing Firebase

After setting up authentication, test all features:

```python
from firebase_integration import get_firebase_manager

# Create Firebase manager
fm = get_firebase_manager()
print("Connected:", fm.connected)

# Test conversation storage
fm.save_conversation("Hello", "Hi there!")

# Test search storage  
fm.save_search_result("test query", "test result")

# Test voice profile storage
fm.save_voice_sample("user1", {"speed": 0.9, "pitch": 0.8})
```

## Troubleshooting

### Error: "Your default credentials were not found"
This means Firebase authentication is not set up. Use Option 1 (local storage) or Option 2 (Firebase setup).

### Error: "Permission denied"
The Firebase database rules may restrict access. Contact the project owner or use local storage.

### Error: "Network issues"
Firebase may be blocked by network restrictions. Local storage will work offline.

## Get Help

Run the setup helper:
```bash
python3 setup_firebase_auth.py
```

This will guide you through the setup process and show current status.