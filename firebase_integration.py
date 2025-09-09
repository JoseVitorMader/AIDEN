"""
Firebase Integration Module for AIDEN
Handles saving and retrieving conversation data and search results from Firebase Realtime Database
"""

import json
import datetime
from typing import Dict, List, Optional, Any

# Safe import for Firebase (will be gracefully handled if not available)
try:
    import firebase_admin
    from firebase_admin import credentials, db
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
        """Initialize Firebase app and Realtime Database"""
        try:
            # Try to initialize Firebase app if not already done
            if not firebase_admin._apps:
                # For production, you would use a service account JSON file:
                # cred = credentials.Certificate('path/to/serviceAccountKey.json')
                # For development/demo, we'll use application default or anonymous
                try:
                    cred = credentials.ApplicationDefault()
                    self.app = firebase_admin.initialize_app(cred, {
                        'projectId': self.config.get('projectId', 'aiden-dd627'),
                        'databaseURL': f"https://{self.config.get('projectId', 'aiden-dd627')}-default-rtdb.firebaseio.com/"
                    })
                except Exception:
                    # Fallback: try to initialize with minimal config
                    print("[INFO] Using default Firebase credentials for Realtime Database")
                    self.app = firebase_admin.initialize_app(options={
                        'databaseURL': f"https://{self.config.get('projectId', 'aiden-dd627')}-default-rtdb.firebaseio.com/"
                    })
            else:
                self.app = firebase_admin.get_app()
            
            # Initialize Realtime Database
            self.db = db.reference()
            self.connected = True
            print(f"[SUCCESS] Connected to Firebase Realtime Database: {self.config.get('projectId', 'unknown')}")
            
        except Exception as e:
            print(f"[ERROR] Firebase Realtime Database initialization failed: {e}")
            print("[INFO] Continuing without Firebase - data will be stored locally only")
            self.connected = False
    
    def save_search_result(self, query: str, result: str, source: str = "web") -> bool:
        """
        Save a search query and result to Firebase Realtime Database
        
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
                'timestamp': datetime.datetime.now().isoformat(),
                'session_id': self._get_session_id()
            }
            
            # Save to 'searches' node in Realtime Database
            searches_ref = self.db.child('searches')
            new_search_ref = searches_ref.push(doc_data)
            print(f"[Firebase] Search saved with key: {new_search_ref.key}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to save to Firebase Realtime Database: {e}")
            return self._save_locally(query, result, source)
    
    def search_previous_results(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for previous results related to the query in Realtime Database
        
        Args:
            query: Search query to match against
            limit: Maximum number of results to return
        
        Returns:
            List of matching search results
        """
        if not self.connected:
            return self._search_locally(query, limit)
        
        try:
            # Search in Realtime Database for similar queries
            query_lower = query.lower()
            
            # Get recent searches from Realtime Database
            searches_ref = self.db.child('searches')
            all_searches = searches_ref.order_by_child('timestamp').limit_to_last(50).get()
            
            if not all_searches:
                return []
            
            matches = []
            
            # Convert the data and search for matches
            for key, data in all_searches.items():
                if not isinstance(data, dict):
                    continue
                    
                stored_query = data.get('query', '').lower()
                stored_result = data.get('result', '').lower()
                
                # Simple keyword matching - can be enhanced with better search algorithms
                query_words = set(query_lower.split())
                stored_words = set(stored_query.split())
                
                # Check if there's overlap in keywords
                if query_words.intersection(stored_words) or any(word in stored_result for word in query_words):
                    matches.append({
                        'id': key,
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
            print(f"[ERROR] Failed to search Firebase Realtime Database: {e}")
            return self._search_locally(query, limit)
    
    def save_conversation(self, user_input: str, ai_response: str) -> bool:
        """
        Save a conversation exchange to Firebase Realtime Database
        
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
                'timestamp': datetime.datetime.now().isoformat(),
                'session_id': self._get_session_id()
            }
            
            # Save to 'conversations' node in Realtime Database
            conversations_ref = self.db.child('conversations')
            new_conversation_ref = conversations_ref.push(doc_data)
            print(f"[Firebase] Conversation saved with key: {new_conversation_ref.key}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to save conversation to Firebase Realtime Database: {e}")
            return self._save_conversation_locally(user_input, ai_response)
    
    def save_voice_sample(self, user_id: str, voice_data: Dict[str, Any]) -> bool:
        """
        Save voice learning data to Firebase Realtime Database
        
        Args:
            user_id: User identifier
            voice_data: Voice characteristics and preferences
        
        Returns:
            bool: True if saved successfully
        """
        if not self.connected:
            return self._save_voice_sample_locally(user_id, voice_data)
        
        try:
            voice_data['timestamp'] = datetime.datetime.now().isoformat()
            voice_data['session_id'] = self._get_session_id()
            
            # Save to 'voice_profiles' node in Realtime Database
            voice_ref = self.db.child('voice_profiles').child(user_id)
            voice_ref.push(voice_data)
            print(f"[Firebase] Voice sample saved for user: {user_id}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to save voice sample to Firebase: {e}")
            return self._save_voice_sample_locally(user_id, voice_data)
    
    def get_voice_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Get voice profile for a user from Firebase Realtime Database
        
        Args:
            user_id: User identifier
        
        Returns:
            Voice profile data
        """
        if not self.connected:
            return self._get_voice_profile_locally(user_id)
        
        try:
            voice_ref = self.db.child('voice_profiles').child(user_id)
            voice_data = voice_ref.get()
            
            if voice_data:
                # Get the most recent voice profile
                if isinstance(voice_data, dict):
                    latest_key = max(voice_data.keys())
                    return voice_data[latest_key]
                    
            return {}
            
        except Exception as e:
            print(f"[ERROR] Failed to get voice profile from Firebase: {e}")
            return self._get_voice_profile_locally(user_id)
    
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

    def _save_voice_sample_locally(self, user_id: str, voice_data: Dict[str, Any]) -> bool:
        """Fallback method to save voice samples locally"""
        try:
            filename = f"aiden_voice_profiles_{user_id}.json"
            voice_data['timestamp'] = datetime.datetime.now().isoformat()
            
            # Read existing data
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except FileNotFoundError:
                existing_data = []
            
            # Append new data
            existing_data.append(voice_data)
            
            # Write back
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"[Local] Voice sample saved to {filename}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to save voice sample locally: {e}")
            return False
    
    def get_voice_learning_stats(self, user_id: str) -> Dict[str, Any]:
        """
        Get voice learning statistics for a user from Firebase Realtime Database
        
        Args:
            user_id: User identifier
        
        Returns:
            Dictionary with voice learning statistics
        """
        if not self.connected:
            return self._get_voice_stats_locally(user_id)
        
        try:
            voice_ref = self.db.child('voice_profiles').child(user_id)
            voice_data = voice_ref.get()
            
            if not voice_data:
                return {'message': 'No voice data found for user'}
            
            # Process voice learning data
            total_samples = len(voice_data)
            confidence_scores = []
            recent_samples = []
            
            import datetime
            week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
            
            for key, sample in voice_data.items():
                if isinstance(sample, dict):
                    # Collect confidence scores
                    if 'confidence' in sample:
                        confidence_scores.append(sample['confidence'])
                    
                    # Check for recent samples
                    timestamp_str = sample.get('timestamp')
                    if timestamp_str:
                        try:
                            sample_time = datetime.datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                            if sample_time > week_ago:
                                recent_samples.append(sample)
                        except:
                            pass
            
            # Calculate statistics
            avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
            
            stats = {
                'total_voice_samples': total_samples,
                'average_confidence': avg_confidence,
                'recent_samples_week': len(recent_samples),
                'voice_quality_trend': 'improving' if avg_confidence > 0.7 else 'needs_improvement',
                'learning_active': len(recent_samples) > 0
            }
            
            return stats
            
        except Exception as e:
            print(f"[ERROR] Failed to get voice learning stats from Firebase: {e}")
            return self._get_voice_stats_locally(user_id)
    
    def update_voice_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """
        Update user voice preferences in Firebase Realtime Database
        
        Args:
            user_id: User identifier
            preferences: Voice preference settings
        
        Returns:
            True if updated successfully
        """
        if not self.connected:
            return self._update_voice_preferences_locally(user_id, preferences)
        
        try:
            preferences['timestamp'] = datetime.datetime.now().isoformat()
            preferences['type'] = 'voice_preferences'
            
            # Save to user preferences node
            prefs_ref = self.db.child('user_preferences').child(user_id).child('voice')
            prefs_ref.set(preferences)
            
            print(f"[Firebase] Voice preferences updated for user: {user_id}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to update voice preferences in Firebase: {e}")
            return self._update_voice_preferences_locally(user_id, preferences)
    
    def get_user_voice_preferences(self, user_id: str) -> Dict[str, Any]:
        """
        Get user voice preferences from Firebase Realtime Database
        
        Args:
            user_id: User identifier
        
        Returns:
            Voice preferences dictionary
        """
        if not self.connected:
            return self._get_voice_preferences_locally(user_id)
        
        try:
            prefs_ref = self.db.child('user_preferences').child(user_id).child('voice')
            preferences = prefs_ref.get()
            
            return preferences if preferences else {}
            
        except Exception as e:
            print(f"[ERROR] Failed to get voice preferences from Firebase: {e}")
            return self._get_voice_preferences_locally(user_id)
    
    def _get_voice_profile_locally(self, user_id: str) -> Dict[str, Any]:
        """Fallback method to get voice profile locally"""
        try:
            filename = f"aiden_voice_profiles_{user_id}.json"
            
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Return the most recent profile
                    return data[-1] if data else {}
            except FileNotFoundError:
                return {}
            
        except Exception as e:
            print(f"[ERROR] Failed to get voice profile locally: {e}")
            return {}
    
    def _get_voice_stats_locally(self, user_id: str) -> Dict[str, Any]:
        """Fallback method to get voice learning stats locally"""
        try:
            filename = f"aiden_voice_profiles_{user_id}.json"
            
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except FileNotFoundError:
                return {'message': 'No voice learning data found locally'}
            
            if not data:
                return {'message': 'No voice samples available'}
            
            # Calculate basic stats
            total_samples = len(data)
            confidence_scores = [d.get('confidence', 0) for d in data if 'confidence' in d]
            avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
            
            # Recent samples (last week)
            import datetime
            week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
            recent_samples = []
            
            for sample in data:
                timestamp_str = sample.get('timestamp')
                if timestamp_str:
                    try:
                        sample_time = datetime.datetime.fromisoformat(timestamp_str)
                        if sample_time > week_ago:
                            recent_samples.append(sample)
                    except:
                        pass
            
            return {
                'total_voice_samples': total_samples,
                'average_confidence': avg_confidence,
                'recent_samples_week': len(recent_samples),
                'voice_quality_trend': 'improving' if avg_confidence > 0.7 else 'needs_improvement',
                'learning_active': len(recent_samples) > 0,
                'source': 'local_storage'
            }
            
        except Exception as e:
            return {'error': str(e), 'source': 'local_storage'}
    
    def _update_voice_preferences_locally(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Fallback method to update voice preferences locally"""
        try:
            filename = f"aiden_voice_preferences_{user_id}.json"
            preferences['timestamp'] = datetime.datetime.now().isoformat()
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(preferences, f, indent=2, ensure_ascii=False)
            
            print(f"[Local] Voice preferences saved to {filename}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to save voice preferences locally: {e}")
            return False
    
    def _get_voice_preferences_locally(self, user_id: str) -> Dict[str, Any]:
        """Fallback method to get voice preferences locally"""
        try:
            filename = f"aiden_voice_preferences_{user_id}.json"
            
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except FileNotFoundError:
                return {}
            
        except Exception as e:
            print(f"[ERROR] Failed to get voice preferences locally: {e}")
            return {}


# Firebase configuration for Realtime Database
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyDe1tIF0RDqotZVqzV1o77utir_nl2XMSc",
    "authDomain": "aiden-dd627.firebaseapp.com",
    "projectId": "aiden-dd627",
    "databaseURL": "https://aiden-dd627-default-rtdb.firebaseio.com/",
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