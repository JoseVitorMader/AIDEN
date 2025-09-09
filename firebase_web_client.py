"""
Firebase Web Client Module for AIDEN
Alternative to Firebase Admin SDK using REST API and web credentials
"""

import json
import requests
import datetime
from typing import Dict, List, Optional, Any

class FirebaseWebClient:
    """Firebase client using web API credentials instead of Admin SDK"""
    
    def __init__(self, config: Dict[str, str]):
        """
        Initialize Firebase Web Client with web app config
        
        Args:
            config: Firebase web app configuration dictionary
        """
        self.config = config
        self.api_key = config.get('apiKey')
        self.database_url = config.get('databaseURL')
        self.project_id = config.get('projectId')
        self.connected = False
        
        if self.api_key and self.database_url:
            self._test_connection()
        else:
            print("[ERROR] Firebase web config missing required fields")
    
    def _test_connection(self):
        """Test Firebase connection using REST API"""
        try:
            # Test connection by trying to read from the database
            test_url = f"{self.database_url}/test.json"
            response = requests.get(test_url, timeout=10)
            
            if response.status_code in [200, 404]:  # 200 = data exists, 404 = path doesn't exist (both are OK)
                self.connected = True
                print(f"[SUCCESS] Connected to Firebase Realtime Database via REST API: {self.project_id}")
            else:
                print(f"[ERROR] Firebase connection test failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"[ERROR] Firebase web client connection failed: {e}")
            self.connected = False
    
    def save_data(self, path: str, data: Dict[str, Any]) -> bool:
        """
        Save data to Firebase using REST API
        
        Args:
            path: Firebase path (e.g., 'conversations', 'searches')
            data: Data to save
            
        Returns:
            bool: True if successful
        """
        if not self.connected:
            return False
            
        try:
            # Add timestamp
            data['timestamp'] = datetime.datetime.now().isoformat()
            
            # Use POST to create new entry with auto-generated key
            url = f"{self.database_url}/{path}.json"
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"[Firebase Web] Data saved to {path} with key: {result.get('name', 'unknown')}")
                return True
            else:
                print(f"[ERROR] Failed to save to Firebase: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Firebase web save failed: {e}")
            return False
    
    def get_data(self, path: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get data from Firebase using REST API
        
        Args:
            path: Firebase path
            limit: Maximum number of items to return
            
        Returns:
            List of data items
        """
        if not self.connected:
            return []
            
        try:
            # Get data with limit using Firebase REST API query parameters
            url = f"{self.database_url}/{path}.json"
            params = {
                'orderBy': '"timestamp"',
                'limitToLast': limit
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    # Convert to list format
                    if isinstance(data, dict):
                        return [{'key': k, **v} for k, v in data.items()]
                    else:
                        return [data] if not isinstance(data, list) else data
                return []
            else:
                print(f"[ERROR] Failed to get Firebase data: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            print(f"[ERROR] Firebase web get failed: {e}")
            return []

    def save_conversation(self, user_input: str, ai_response: str) -> bool:
        """Save conversation to Firebase"""
        data = {
            'user_input': user_input,
            'ai_response': ai_response,
            'session_id': self._get_session_id()
        }
        return self.save_data('conversations', data)
    
    def save_search_result(self, query: str, result: str, source: str = "web") -> bool:
        """Save search result to Firebase"""
        data = {
            'query': query,
            'result': result,
            'source': source,
            'session_id': self._get_session_id()
        }
        return self.save_data('searches', data)
    
    def _get_session_id(self) -> str:
        """Generate session ID"""
        return f"aiden_session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"


def test_firebase_web_client():
    """Test the Firebase web client"""
    from firebase_integration import FIREBASE_CONFIG
    
    client = FirebaseWebClient(FIREBASE_CONFIG)
    
    if client.connected:
        print("✅ Firebase Web Client connected successfully")
        
        # Test saving data
        if client.save_conversation("Test input", "Test response"):
            print("✅ Conversation save test passed")
        
        if client.save_search_result("test query", "test result"):
            print("✅ Search result save test passed")
            
        # Test getting data
        conversations = client.get_data('conversations', 5)
        print(f"✅ Retrieved {len(conversations)} conversations")
        
    else:
        print("❌ Firebase Web Client connection failed")


if __name__ == "__main__":
    test_firebase_web_client()