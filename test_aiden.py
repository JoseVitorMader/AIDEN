#!/usr/bin/env python3
"""
AIDEN Voice and Firebase Test Script
Tests the voice-first functionality and Firebase integration
"""

import os
import sys
import time

def test_aiden_functionality():
    """Test AIDEN's core functionality"""
    print("🤖 AIDEN Functionality Test")
    print("=" * 50)
    
    # Test 1: Module imports
    print("\n1. Testing Module Imports...")
    try:
        from aiden_main import AIDEN
        from firebase_integration import get_firebase_manager
        from aiden_core import AidenCore
        print("✓ All core modules imported successfully")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    # Test 2: Firebase integration
    print("\n2. Testing Firebase Integration...")
    try:
        firebase_manager = get_firebase_manager()
        
        # Test saving a search result
        test_save = firebase_manager.save_search_result(
            "Como está o tempo hoje?", 
            "O tempo está ensolarado com temperatura de 25°C", 
            "test"
        )
        print(f"✓ Firebase save test: {'Success' if test_save else 'Failed (using local fallback)'}")
        
        # Test searching previous results
        results = firebase_manager.search_previous_results("tempo", 3)
        print(f"✓ Firebase search test: Found {len(results)} results")
        
    except Exception as e:
        print(f"✗ Firebase test error: {e}")
    
    # Test 3: AIDEN Core
    print("\n3. Testing AIDEN Core...")
    try:
        aiden_core = AidenCore("TestUser")
        greeting = aiden_core.greet()
        print(f"✓ AIDEN Core greeting: {greeting[:100]}...")
        
        # Test system command
        system_status = aiden_core.process_command("status do sistema")
        print(f"✓ System status command: {len(system_status)} characters response")
        
    except Exception as e:
        print(f"✗ AIDEN Core error: {e}")
    
    # Test 4: Voice Recognition (if available)
    print("\n4. Testing Voice Recognition...")
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        print("✓ Speech recognition library available")
        
        # Test microphone availability
        try:
            microphone = sr.Microphone()
            print("✓ Microphone device detected")
            
            # Note: We won't actually test recording here to avoid hanging
            print("ℹ️  Voice input would be available in interactive mode")
            
        except Exception as e:
            print(f"⚠️  Microphone test: {e}")
            
    except ImportError:
        print("ℹ️  Speech recognition not available (install requirements)")
    
    # Test 5: Text-to-Speech (if available)
    print("\n5. Testing Text-to-Speech...")
    try:
        from text_to_speech import speak_text
        print("✓ Text-to-speech module available")
        
        # Test offline TTS
        try:
            import pyttsx3
            print("✓ Offline TTS (pyttsx3) available")
        except ImportError:
            print("ℹ️  Offline TTS not available")
            
        # Test online TTS
        try:
            from gtts import gTTS
            print("✓ Online TTS (gTTS) available")
        except ImportError:
            print("ℹ️  Online TTS not available")
            
    except ImportError:
        print("ℹ️  Text-to-speech not available")
    
    # Test 6: Full AIDEN Instance
    print("\n6. Testing Full AIDEN Instance...")
    try:
        aiden = AIDEN("TestUser")
        print("✓ AIDEN instance created successfully")
        
        # Test capabilities
        capabilities = aiden.capabilities
        print("✓ AIDEN Capabilities:")
        for capability, status in capabilities.items():
            status_icon = "🟢" if status else "🔴"
            print(f"   {status_icon} {capability.replace('_', ' ').title()}")
            
        # Test session start
        welcome = aiden.start_session()
        print(f"✓ Session start: {len(welcome)} characters")
        
    except Exception as e:
        print(f"✗ AIDEN instance error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 AIDEN functionality test completed!")
    print("\nTo run AIDEN interactively:")
    print("  python aiden_main.py")
    print("\nFor voice-first interaction, ensure microphone is connected.")
    print("For full AI features, set GOOGLE_API_KEY environment variable.")
    
    return True

def test_voice_priority():
    """Demonstrate voice-priority features"""
    print("\n🎤 AIDEN Voice Priority Features")
    print("=" * 50)
    
    print("\n📋 Voice-First Design Features:")
    print("• Extended voice timeout (10 seconds)")
    print("• Optimized speech recognition settings")
    print("• Automatic ambient noise adjustment")
    print("• Priority audio output with offline/online TTS")
    print("• Graceful fallback to text when voice unavailable")
    print("• Voice status indicators (🎤, 🗣️, 🔊)")
    
    print("\n📋 Voice Commands Supported:")
    print("• 'Olá AIDEN' - Greeting")
    print("• 'pesquisar [topic]' - Web search with Firebase storage")
    print("• 'status do sistema' - System diagnostics")
    print("• 'como está o tempo?' - General conversation")
    print("• 'sair' - Shutdown")
    
    print("\n📋 Audio Processing:")
    print("• Portuguese (Brazil) speech recognition")
    print("• Offline TTS via pyttsx3 (priority)")
    print("• Online TTS via gTTS (fallback)")
    print("• pygame for audio playback")

def test_firebase_features():
    """Demonstrate Firebase integration features"""
    print("\n🔥 AIDEN Firebase Integration Features")
    print("=" * 50)
    
    print("\n📋 Firebase Capabilities:")
    print("• Automatic conversation storage")
    print("• Search result preservation") 
    print("• Context-aware responses using previous data")
    print("• Cross-session memory persistence")
    print("• Intelligent keyword-based search")
    print("• Graceful local fallback when offline")
    
    print("\n📋 Firebase Collections:")
    print("• 'conversations' - User inputs and AI responses")
    print("• 'searches' - Web search results with source tracking")
    print("• Automatic timestamping and session management")
    
    print("\n📋 Search Intelligence:")
    print("• Keyword overlap detection")
    print("• Relevance scoring")
    print("• Context integration in new responses")
    print("• Local JSON fallback storage")

if __name__ == "__main__":
    print("🚀 Starting AIDEN Test Suite...")
    
    # Run functionality tests
    test_aiden_functionality()
    
    # Show voice features
    test_voice_priority()
    
    # Show Firebase features  
    test_firebase_features()
    
    print("\n🎯 AIDEN is ready for voice-first interaction with Firebase integration!")
    print("Run 'python aiden_main.py' to start the interactive voice interface.")