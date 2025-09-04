"""
Firebase Integration Module for AIDEN
Handles saving and retrieving conversation data and search results from Firebase
"""

import json
import datetime
from typing import Dict, List, Optional, Any

# Safe import for Firebase (will be gracefully handled if not available)
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("[INFO] Firebase Admin SDK not available - install with 'pip install firebase-admin'")

class FirebaseManager:
    def __init__(self, config: Dict[str, str]):
        """
        Initialize Firebase connection with provided config
        
        Args:
            config: Firebase configuration dictionary with apiKey, projectId, etc.
        """
        self.config = config
        self.db = None
        self.app = None
        self.connected = False
        
        if FIREBASE_AVAILABLE:
            try:
                self._initialize_firebase()
            except Exception as e:
                print(f"[ERROR] Failed to initialize Firebase: {e}")
                self.connected = False
        else:
            print("[WARNING] Firebase SDK not available - data will not be saved to Firebase")
    
    def _initialize_firebase(self):
        """Initialize Firebase app and Firestore database"""
        try:
            # For server-side SDK, we need a service account key
            # Since we only have web config, we'll create a minimal credential
            # This would normally require a service account JSON file
            
            # Try to initialize Firebase app if not already done
            if not firebase_admin._apps:
                # In production, you would use:
                # cred = credentials.Certificate('path/to/serviceAccountKey.json')
                # For now, we'll use application default credentials or skip if not available
                try:
                    cred = credentials.ApplicationDefault()
                    self.app = firebase_admin.initialize_app(cred, {
                        'projectId': self.config.get('projectId', 'aiden-dd627')
                    })
                except Exception:
                    # Fallback: try to initialize without credentials (for development)
                    print("[INFO] Using default Firebase credentials")
                    self.app = firebase_admin.initialize_app()
            else:
                self.app = firebase_admin.get_app()
            
            # Initialize Firestore
            self.db = firestore.client()
            self.connected = True
            print(f"[SUCCESS] Connected to Firebase project: {self.config.get('projectId', 'unknown')}")
            
        except Exception as e:
            print(f"[ERROR] Firebase initialization failed: {e}")
            print("[INFO] Continuing without Firebase - data will be stored locally only")
            self.connected = False
    
    def save_search_result(self, query: str, result: str, source: str = "web") -> bool:
        """
        Save a search query and result to Firebase
        
        Args:
            query: The search query
            result: The search result or response
            source: Source of the result (web, ai, system, etc.)
        
        Returns:
            bool: True if saved successfully, False otherwise
        """
        if not self.connected:
            return self._save_locally(query, result, source)
        
        try:
            doc_data = {
                'query': query,
                'result': result,
                'source': source,
                'timestamp': datetime.datetime.now(),
                'session_id': self._get_session_id()
            }
            
            # Save to 'searches' collection
            doc_ref = self.db.collection('searches').add(doc_data)
            print(f"[Firebase] Search saved with ID: {doc_ref[1].id}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to save to Firebase: {e}")
            return self._save_locally(query, result, source)
    
    def search_previous_results(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for previous results related to the query
        
        Args:
            query: Search query to match against
            limit: Maximum number of results to return
        
        Returns:
            List of matching search results
        """
        if not self.connected:
            return self._search_locally(query, limit)
        
        try:
            # Search in Firestore for similar queries
            query_lower = query.lower()
            
            # Get recent searches that might contain relevant keywords
            searches_ref = self.db.collection('searches').order_by(
                'timestamp', direction=firestore.Query.DESCENDING
            ).limit(50)  # Get last 50 searches to search through
            
            docs = searches_ref.stream()
            matches = []
            
            for doc in docs:
                data = doc.to_dict()
                stored_query = data.get('query', '').lower()
                stored_result = data.get('result', '').lower()
                
                # Simple keyword matching - can be enhanced with better search algorithms
                query_words = set(query_lower.split())
                stored_words = set(stored_query.split())
                
                # Check if there's overlap in keywords
                if query_words.intersection(stored_words) or any(word in stored_result for word in query_words):
                    matches.append({
                        'id': doc.id,
                        'query': data.get('query'),
                        'result': data.get('result'),
                        'source': data.get('source'),
                        'timestamp': data.get('timestamp'),
                        'relevance_score': len(query_words.intersection(stored_words))
                    })
                
                if len(matches) >= limit:
                    break
            
            # Sort by relevance score
            matches.sort(key=lambda x: x['relevance_score'], reverse=True)
            return matches[:limit]
            
        except Exception as e:
            print(f"[ERROR] Failed to search Firebase: {e}")
            return self._search_locally(query, limit)
    
    def save_conversation(self, user_input: str, ai_response: str) -> bool:
        """
        Save a conversation exchange to Firebase
        
        Args:
            user_input: User's input
            ai_response: AI's response
        
        Returns:
            bool: True if saved successfully
        """
        if not self.connected:
            return self._save_conversation_locally(user_input, ai_response)
        
        try:
            doc_data = {
                'user_input': user_input,
                'ai_response': ai_response,
                'timestamp': datetime.datetime.now(),
                'session_id': self._get_session_id()
            }
            
            # Save to 'conversations' collection
            doc_ref = self.db.collection('conversations').add(doc_data)
            print(f"[Firebase] Conversation saved with ID: {doc_ref[1].id}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to save conversation to Firebase: {e}")
            return self._save_conversation_locally(user_input, ai_response)
    
    def _get_session_id(self) -> str:
        """Generate a session ID for grouping related interactions"""
        return f"aiden_session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _save_locally(self, query: str, result: str, source: str) -> bool:
        """Fallback method to save data locally when Firebase is unavailable"""
        try:
            filename = f"aiden_searches_{datetime.datetime.now().strftime('%Y%m%d')}.json"
            data = {
                'query': query,
                'result': result,
                'source': source,
                'timestamp': datetime.datetime.now().isoformat()
            }
            
            # Read existing data
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except FileNotFoundError:
                existing_data = []
            
            # Append new data
            existing_data.append(data)
            
            # Write back
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"[Local] Search saved to {filename}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to save locally: {e}")
            return False
    
    def _search_locally(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Fallback method to search local data when Firebase is unavailable"""
        try:
            filename = f"aiden_searches_{datetime.datetime.now().strftime('%Y%m%d')}.json"
            
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except FileNotFoundError:
                return []
            
            query_lower = query.lower()
            matches = []
            
            for item in data:
                stored_query = item.get('query', '').lower()
                stored_result = item.get('result', '').lower()
                
                # Simple keyword matching
                if query_lower in stored_query or query_lower in stored_result:
                    matches.append(item)
            
            return matches[-limit:] if matches else []
            
        except Exception as e:
            print(f"[ERROR] Failed to search locally: {e}")
            return []
    
    def _save_conversation_locally(self, user_input: str, ai_response: str) -> bool:
        """Fallback method to save conversations locally"""
        try:
            filename = f"aiden_conversations_{datetime.datetime.now().strftime('%Y%m%d')}.json"
            data = {
                'user_input': user_input,
                'ai_response': ai_response,
                'timestamp': datetime.datetime.now().isoformat()
            }
            
            # Read existing data
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except FileNotFoundError:
                existing_data = []
            
            # Append new data
            existing_data.append(data)
            
            # Write back
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False, default=str)
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to save conversation locally: {e}")
            return False


# Firebase configuration from the problem statement
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyDe1tIF0RDqotZVqzV1o77utir_nl2XMSc",
    "authDomain": "aiden-dd627.firebaseapp.com",
    "projectId": "aiden-dd627",
    "storageBucket": "aiden-dd627.firebasestorage.app",
    "messagingSenderId": "397399680835",
    "appId": "1:397399680835:web:fbfbdffbd3abe8dc7b71f6",
    "measurementId": "G-KCKSSZV884"
}


# Convenience function to get Firebase manager instance
def get_firebase_manager() -> FirebaseManager:
    """Get a Firebase manager instance with the default config"""
    return FirebaseManager(FIREBASE_CONFIG)


if __name__ == "__main__":
    # Test Firebase integration
    firebase_manager = get_firebase_manager()
    
    # Test saving a search result
    test_query = "What is artificial intelligence?"
    test_result = "Artificial intelligence (AI) refers to the simulation of human intelligence in machines..."
    
    if firebase_manager.save_search_result(test_query, test_result, "test"):
        print("✓ Search result saved successfully")
    
    # Test searching for previous results
    results = firebase_manager.search_previous_results("intelligence", 3)
    print(f"Found {len(results)} related previous searches")
    
    for result in results:
        print(f"- {result.get('query')}: {result.get('result')[:100]}...")