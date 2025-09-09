import pyttsx3
from gtts import gTTS
import os
import pygame
import tempfile
from typing import Optional, Dict, Any
import json

def get_voice_settings(user_id: str = "default") -> Dict[str, Any]:
    """Get voice settings for a specific user"""
    try:
        filename = f"aiden_voice_profiles_{user_id}.json"
        with open(filename, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
            if profiles:
                # Get the most recent profile
                return profiles[-1]
    except FileNotFoundError:
        pass
    
    # Default voice settings - male voice, faster and more natural
    return {
        'rate': 200,  # Increased speaking rate (words per minute)
        'volume': 0.9,  # Volume level (0.0 to 1.0)
        'voice_id': 'male',  # Prefer male voice
        'pitch': 0.8,  # Lower pitch for more natural sound
        'language': 'pt-br'  # Portuguese Brazil
    }

def configure_voice_engine(engine, settings: Dict[str, Any]) -> bool:
    """Configure the voice engine with specific settings"""
    try:
        # Set speaking rate
        engine.setProperty('rate', settings.get('rate', 180))
        
        # Set volume
        engine.setProperty('volume', settings.get('volume', 0.9))
        
        # Try to set a male voice
        voices = engine.getProperty('voices')
        if voices:
            male_voice = None
            for voice in voices:
                # Look for male voices (common identifiers)
                voice_name = voice.name.lower() if voice.name else ""
                voice_id = voice.id.lower() if voice.id else ""
                
                if any(term in voice_name or term in voice_id for term in 
                       ['male', 'masculino', 'man', 'homem', 'david', 'alex', 'joão']):
                    male_voice = voice
                    break
                # Also look for Brazilian Portuguese voices
                elif any(term in voice_name or term in voice_id for term in 
                         ['brazil', 'pt-br', 'portuguese', 'brasil']):
                    male_voice = voice
                    break
            
            if male_voice:
                engine.setProperty('voice', male_voice.id)
                print(f"[TTS] Using male voice: {male_voice.name}")
            else:
                # Fallback to first available voice
                if len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)  # Often the second voice is different
                print("[TTS] Male voice not found, using available voice")
        
        return True
    except Exception as e:
        print(f"[TTS] Error configuring voice: {e}")
        return False

def speak_offline(text: str, user_id: str = "default") -> bool:
    """Convert text to speech using pyttsx3 (offline) with improved male voice."""
    try:
        engine = pyttsx3.init()
        settings = get_voice_settings(user_id)
        
        # Configure the voice with user preferences
        configure_voice_engine(engine, settings)
        
        # Speak the text
        engine.say(text)
        engine.runAndWait()
        
        # Save voice usage data for learning
        save_voice_usage(user_id, text, 'offline', settings)
        
        return True
    except Exception as e:
        print(f"Erro ao usar pyttsx3: {e}")
        return False

def speak_online(text: str, user_id: str = "default", lang: str = 'pt-br', filename: Optional[str] = None) -> bool:
    """Convert text to speech using gTTS (online) with male voice preference."""
    try:
        if filename is None:
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            filename = temp_file.name
            temp_file.close()
        
        settings = get_voice_settings(user_id)
        lang = settings.get('language', 'pt-br')
        
        # Use gTTS with slower speed for more natural sound
        tts = gTTS(text=text, lang=lang, slow=False, tld='com.br')
        tts.save(filename)
        
        # Save voice usage data for learning
        save_voice_usage(user_id, text, 'online', settings)
        
        return True
    except Exception as e:
        print(f"Erro ao usar gTTS: {e}")
        return False

def play_audio_file(filename: str, volume: float = 0.9) -> bool:
    """Play an audio file using pygame with adjustable volume."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        return True
    except Exception as e:
        print(f"Erro ao reproduzir áudio: {e}")
        return False

def speak_text(text: str, method: str = 'offline', user_id: str = "default") -> bool:
    """Main function for speech synthesis with voice learning capabilities."""
    try:
        # Enhanced error handling and voice adaptation
        if not text or not text.strip():
            print("[TTS] Empty text provided, skipping speech synthesis")
            return False
        
        # Clean and prepare text for better synthesis
        text = _clean_text_for_tts(text)
        
        if method == 'offline':
            result = speak_offline(text, user_id)
        elif method == 'online':
            # Create temporary file for online TTS
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            filename = temp_file.name
            temp_file.close()
            
            if speak_online(text, user_id, filename=filename):
                settings = get_voice_settings(user_id)
                volume = settings.get('volume', 0.9)
                result = play_audio_file(filename, volume)
                # Clean up temporary file
                try:
                    os.remove(filename)
                except:
                    pass
                return result
            return False
        else:
            print(f"[TTS] Invalid method '{method}'. Use 'offline' or 'online'.")
            return False
        
        # Log successful speech for learning
        if result:
            _log_successful_speech(user_id, text, method)
        
        return result
        
    except Exception as e:
        print(f"[TTS Critical Error]: {e}")
        # Try fallback method
        try:
            print("[TTS] Attempting fallback speech synthesis...")
            return _fallback_speak(text, user_id)
        except:
            print("[TTS] All speech synthesis methods failed")
            return False

def _clean_text_for_tts(text: str) -> str:
    """Clean and prepare text for better text-to-speech synthesis"""
    import re
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    # Replace common abbreviations with full words for better pronunciation
    replacements = {
        'Dr.': 'Doutor',
        'Sra.': 'Senhora',
        'Sr.': 'Senhor',
        'etc.': 'etcetera',
        'ex.': 'exemplo',
        'p.ex.': 'por exemplo',
        'vs.': 'versus',
        'n°': 'número',
        'nº': 'número',
        '%': 'porcento',
        '&': 'e',
        '@': 'arroba',
        'R$': 'reais',
        'US$': 'dólares',
    }
    
    for abbrev, full_word in replacements.items():
        text = text.replace(abbrev, full_word)
    
    # Handle numbers better
    text = re.sub(r'\b(\d+)\b', lambda m: _number_to_words(int(m.group(1))), text)
    
    return text

def _number_to_words(num: int) -> str:
    """Convert numbers to words for better TTS pronunciation (basic implementation)"""
    if num == 0:
        return "zero"
    
    # Basic number conversion (simplified)
    ones = ["", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove"]
    teens = ["dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"]
    tens = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"]
    
    if 0 <= num <= 9:
        return ones[num]
    elif 10 <= num <= 19:
        return teens[num - 10]
    elif 20 <= num <= 99:
        return tens[num // 10] + ("" if num % 10 == 0 else " e " + ones[num % 10])
    else:
        return str(num)  # Fallback for larger numbers

def _fallback_speak(text: str, user_id: str) -> bool:
    """Fallback speech method when primary methods fail"""
    try:
        # Try the simplest pyttsx3 setup
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text[:200])  # Limit text length for fallback
        engine.runAndWait()
        
        print("[TTS] Fallback speech synthesis completed")
        return True
        
    except Exception as e:
        print(f"[TTS] Fallback also failed: {e}")
        return False

def _log_successful_speech(user_id: str, text: str, method: str):
    """Log successful speech synthesis for learning and adaptation"""
    try:
        # Try to save to Firebase
        try:
            from firebase_integration import get_firebase_manager
            firebase_manager = get_firebase_manager()
            
            speech_data = {
                'text_spoken': text,
                'method_used': method,
                'speech_length': len(text),
                'word_count': len(text.split()),
                'synthesis_success': True,
                'context': 'successful_speech'
            }
            
            firebase_manager.save_voice_sample(user_id, speech_data)
            
        except ImportError:
            # Local logging as fallback
            filename = f"aiden_speech_log_{user_id}.json"
            
            import datetime
            log_entry = {
                'timestamp': datetime.datetime.now().isoformat(),
                'text': text[:100] + '...' if len(text) > 100 else text,  # Truncate for logging
                'method': method,
                'success': True
            }
            
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except FileNotFoundError:
                logs = []
            
            logs.append(log_entry)
            
            # Keep only last 50 entries
            if len(logs) > 50:
                logs = logs[-50:]
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
                
    except Exception as e:
        print(f"[TTS] Failed to log speech data: {e}")

def save_voice_usage(user_id: str, text: str, method: str, settings: Dict[str, Any]) -> None:
    """Save voice usage data for learning and adaptation."""
    try:
        # Try to import Firebase manager for cloud storage
        try:
            from firebase_integration import get_firebase_manager
            firebase_manager = get_firebase_manager()
            
            voice_data = {
                'text_spoken': text,
                'method_used': method,
                'settings': settings,
                'text_length': len(text),
                'word_count': len(text.split())
            }
            
            firebase_manager.save_voice_sample(user_id, voice_data)
            
        except ImportError:
            # Fallback to local storage
            _save_voice_usage_locally(user_id, text, method, settings)
            
    except Exception as e:
        print(f"[WARNING] Failed to save voice usage data: {e}")

def _save_voice_usage_locally(user_id: str, text: str, method: str, settings: Dict[str, Any]) -> None:
    """Save voice usage data locally."""
    try:
        import datetime
        filename = f"aiden_voice_usage_{user_id}.json"
        
        data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'text_spoken': text,
            'method_used': method,
            'settings': settings,
            'text_length': len(text),
            'word_count': len(text.split())
        }
        
        # Read existing data
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []
        
        # Append new data
        existing_data.append(data)
        
        # Keep only last 100 entries to avoid large files
        if len(existing_data) > 100:
            existing_data = existing_data[-100:]
        
        # Write back
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"[ERROR] Failed to save voice usage locally: {e}")

def adapt_voice_settings(user_id: str, feedback: str) -> Dict[str, Any]:
    """Adapt voice settings based on user feedback."""
    settings = get_voice_settings(user_id)
    
    feedback_lower = feedback.lower()
    
    # Adjust settings based on feedback
    if 'mais devagar' in feedback_lower or 'slower' in feedback_lower:
        settings['rate'] = max(120, settings.get('rate', 180) - 20)
    elif 'mais rápido' in feedback_lower or 'faster' in feedback_lower:
        settings['rate'] = min(250, settings.get('rate', 180) + 20)
    
    if 'mais baixo' in feedback_lower or 'quieter' in feedback_lower:
        settings['volume'] = max(0.1, settings.get('volume', 0.9) - 0.1)
    elif 'mais alto' in feedback_lower or 'louder' in feedback_lower:
        settings['volume'] = min(1.0, settings.get('volume', 0.9) + 0.1)
    
    if 'grave' in feedback_lower or 'deeper' in feedback_lower:
        settings['pitch'] = max(0.5, settings.get('pitch', 0.8) - 0.1)
    elif 'agudo' in feedback_lower or 'higher' in feedback_lower:
        settings['pitch'] = min(1.2, settings.get('pitch', 0.8) + 0.1)
    
    # Save adapted settings
    try:
        from firebase_integration import get_firebase_manager
        firebase_manager = get_firebase_manager()
        firebase_manager.save_voice_sample(user_id, settings)
    except:
        # Save locally
        filename = f"aiden_voice_profiles_{user_id}.json"
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                profiles = json.load(f)
        except FileNotFoundError:
            profiles = []
        
        profiles.append(settings)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)
    
    return settings

if __name__ == "__main__":
    # Test voice system with improved settings
    text = "Olá! Este é um teste do sistema de síntese de fala com voz masculina aprimorada."
    
    print("🎙️  Testando síntese offline com voz masculina...")
    speak_text(text, method='offline', user_id='test_user')
    
    print("🌐 Testando síntese online com voz masculina...")
    speak_text(text, method='online', user_id='test_user')
    
    print("🔧 Testando adaptação de configurações de voz...")
    settings = adapt_voice_settings('test_user', 'fale mais devagar e com voz mais grave')
    print(f"Configurações adaptadas: {settings}")
    
    # Test with adapted settings
    print("🎯 Testando com configurações adaptadas...")
    speak_text("Agora estou falando com as configurações adaptadas às suas preferências.", method='offline', user_id='test_user')

