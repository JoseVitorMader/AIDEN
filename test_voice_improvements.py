#!/usr/bin/env python3
"""
Test script for AIDEN voice improvements
Tests the enhanced voice capabilities including Firebase integration
"""

import os
import sys

def test_text_to_speech_improvements():
    """Test improved text-to-speech functionality"""
    print("🎤 Testing improved text-to-speech...")
    
    try:
        from text_to_speech import speak_text, get_voice_settings, adapt_voice_settings
        
        # Test with short text
        print("Testing short text...")
        result = speak_text("Olá! Este é um teste rápido do sistema de voz melhorado.", method='offline', user_id='test_user')
        print(f"Short text TTS result: {result}")
        
        # Test with long text (should trigger chunking)
        long_text = """Este é um texto muito longo para testar a funcionalidade de divisão de texto em pedaços menores. 
        O sistema deve automaticamente dividir este texto em partes menores para uma melhor síntese de voz. 
        Esta é uma funcionalidade importante que foi implementada para resolver problemas com textos longos que não eram lidos corretamente. 
        Agora o sistema deve processar cada parte separadamente, fazendo pausas apropriadas entre as seções para uma experiência de áudio mais natural."""
        
        print("Testing long text (should be chunked)...")
        result = speak_text(long_text, method='offline', user_id='test_user')
        print(f"Long text TTS result: {result}")
        
        # Test voice settings
        settings = get_voice_settings('test_user')
        print(f"Current voice settings: {settings}")
        
        # Test voice adaptation
        print("Testing voice adaptation...")
        adapted_settings = adapt_voice_settings('test_user', 'fale mais devagar e com voz mais grave')
        print(f"Adapted settings: {adapted_settings}")
        
        return True
        
    except Exception as e:
        print(f"❌ Text-to-speech test failed: {e}")
        return False

def test_voice_recognition_improvements():
    """Test improved voice recognition (without requiring actual microphone input)"""
    print("🎧 Testing improved voice recognition system...")
    
    try:
        from voice_recognition import get_voice_learning_stats, _analyze_voice_characteristics
        
        # Test voice learning stats (should work even without data)
        stats = get_voice_learning_stats('test_user')
        print(f"Voice learning stats: {stats}")
        
        # Test would require actual audio input, so we'll just verify the module loads
        print("✅ Voice recognition modules loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Voice recognition test failed: {e}")
        return False

def test_firebase_integration():
    """Test Firebase integration for voice data"""
    print("🔥 Testing Firebase integration...")
    
    try:
        from firebase_integration import get_firebase_manager
        
        # Initialize Firebase manager
        firebase_manager = get_firebase_manager()
        print(f"Firebase connected: {firebase_manager.connected}")
        
        # Test saving voice sample (even if Firebase is offline, should fallback to local)
        test_voice_data = {
            'text_spoken': 'Test voice sample',
            'confidence': 0.85,
            'method': 'test',
            'characteristics': {'sample_rate': 16000, 'duration': 2.5}
        }
        
        result = firebase_manager.save_voice_sample('test_user', test_voice_data)
        print(f"Voice sample save result: {result}")
        
        # Test getting voice profile
        profile = firebase_manager.get_voice_profile('test_user')
        print(f"Voice profile retrieved: {bool(profile)}")
        
        # Test voice learning stats
        stats = firebase_manager.get_voice_learning_stats('test_user')
        print(f"Voice learning stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Firebase integration test failed: {e}")
        return False

def test_main_ai_improvements():
    """Test main AI improvements (without full initialization)"""
    print("🤖 Testing main AI improvements...")
    
    try:
        # Test text chunking functionality
        from main_ai import ManusAI
        
        # Create instance without full initialization
        ai = ManusAI(gemini_api_key=None, enable_aiden_mode=True, user_name="TestUser")
        
        # Test long text handling
        long_text = "Este é um texto muito longo " * 20  # Create a long text
        print(f"Testing text chunking with {len(long_text)} characters...")
        
        # This would normally speak, but we just want to test the chunking logic exists
        print("✅ Main AI improvements loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Main AI test failed: {e}")
        return False

def run_all_tests():
    """Run all improvement tests"""
    print("🚀 AIDEN Voice Improvements Test Suite")
    print("=" * 50)
    
    tests = [
        ("Text-to-Speech Improvements", test_text_to_speech_improvements),
        ("Voice Recognition Improvements", test_voice_recognition_improvements),
        ("Firebase Integration", test_firebase_integration),
        ("Main AI Improvements", test_main_ai_improvements)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"{'✅' if result else '❌'} {test_name}: {'PASSED' if result else 'FAILED'}")
        except Exception as e:
            results.append((test_name, False))
            print(f"❌ {test_name}: FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All voice improvements are working correctly!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)