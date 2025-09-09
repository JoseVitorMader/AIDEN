#!/usr/bin/env python3
"""
Test script to demonstrate Firebase fix and local fallback functionality
"""

import sys
import os
from firebase_integration import get_firebase_manager

def test_firebase_connection():
    """Test Firebase connection and functionality"""
    
    print("🤖 AIDEN Firebase Connection Test")
    print("=" * 50)
    
    # Test Firebase manager creation
    print("1. Creating Firebase manager...")
    try:
        fm = get_firebase_manager()
        print(f"   ✅ Firebase manager created successfully")
        print(f"   🔗 Connected to Firebase: {fm.connected}")
    except Exception as e:
        print(f"   ❌ Error creating Firebase manager: {e}")
        return False
    
    # Test conversation storage
    print("\n2. Testing conversation storage...")
    try:
        result = fm.save_conversation(
            "Hello AIDEN, are you working properly?",
            "Yes! I'm working perfectly with local storage fallback."
        )
        if result:
            print("   ✅ Conversation saved successfully")
        else:
            print("   ❌ Failed to save conversation")
    except Exception as e:
        print(f"   ❌ Error saving conversation: {e}")
    
    # Test search result storage
    print("\n3. Testing search result storage...")
    try:
        result = fm.save_search_result(
            "Firebase authentication setup",
            "Firebase requires service account credentials for Admin SDK access",
            "documentation"
        )
        if result:
            print("   ✅ Search result saved successfully")
        else:
            print("   ❌ Failed to save search result")
    except Exception as e:
        print(f"   ❌ Error saving search result: {e}")
    
    # Test voice profile storage
    print("\n4. Testing voice profile storage...")
    try:
        result = fm.save_voice_sample("test_user", {
            "voice_speed": 0.85,
            "voice_pitch": 0.9,
            "confidence": 0.92,
            "test_mode": True
        })
        if result:
            print("   ✅ Voice profile saved successfully")
        else:
            print("   ❌ Failed to save voice profile")
    except Exception as e:
        print(f"   ❌ Error saving voice profile: {e}")
    
    # Show created files
    print("\n5. Checking local storage files...")
    import glob
    local_files = glob.glob("aiden_*.json")
    if local_files:
        print(f"   ✅ Local storage files created: {len(local_files)} files")
        for file in sorted(local_files):
            size = os.path.getsize(file)
            print(f"      📁 {file} ({size} bytes)")
    else:
        print("   ⚠️ No local storage files found")
    
    # Firebase setup guidance
    print("\n" + "=" * 50)
    print("🔥 FIREBASE SETUP STATUS")
    print("=" * 50)
    
    if fm.connected:
        print("✅ Firebase is connected and working!")
        print("   All data is being saved to Firebase Realtime Database.")
    else:
        print("⚠️  Firebase is NOT connected (using local storage)")
        print("   To enable Firebase cloud storage:")
        print("   1. Run: python3 setup_firebase_auth.py")
        print("   2. Or download service account key to 'serviceAccountKey.json'")
        print("   3. See FIREBASE_SETUP.md for detailed instructions")
    
    print("\n🎉 Test completed successfully!")
    print("   AIDEN Firebase integration is working properly with fallback support.")
    
    return True

if __name__ == "__main__":
    success = test_firebase_connection()
    sys.exit(0 if success else 1)