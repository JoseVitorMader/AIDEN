import pyttsx3
from gtts import gTTS
import os
import pygame
import tempfile
from typing import Optional, Dict, Any
import json
import datetime

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
    
    # Default voice settings - male voice, less robotic, faster speech
    return {
        'rate': 200,  # Speaking rate (words per minute) - increased from 180
        'volume': 0.9,  # Volume level (0.0 to 1.0)
        'voice_id': 'male',  # Prefer male voice
        'pitch': 0.7,  # Lower pitch for more natural sound - slightly lower
        'language': 'pt-br'  # Portuguese Brazil
    }

def configure_voice_engine(engine, settings: Dict[str, Any]) -> bool:
    """Configure the voice engine with specific settings"""
    try:
        # Set speaking rate - with improved range handling
        rate = settings.get('rate', 200)
        engine.setProperty('rate', max(120, min(300, rate)))  # Clamp between reasonable values
        
        # Set volume
        volume = settings.get('volume', 0.9)
        engine.setProperty('volume', max(0.1, min(1.0, volume)))
        
        # Try to set a male voice with improved selection logic
        voices = engine.getProperty('voices')
        if voices:
            selected_voice = None
            male_voices = []
            brazilian_voices = []
            
            for voice in voices:
                # Look for male voices (common identifiers)
                voice_name = voice.name.lower() if voice.name else ""
                voice_id = voice.id.lower() if voice.id else ""
                
                # Prioritize Brazilian Portuguese voices
                if any(term in voice_name or term in voice_id for term in 
                       ['brazil', 'pt-br', 'portuguese', 'brasil', 'br']):
                    brazilian_voices.append(voice)
                    
                # Collect male voices
                if any(term in voice_name or term in voice_id for term in 
                       ['male', 'masculino', 'man', 'homem', 'david', 'alex', 'joão', 'marcos']):
                    male_voices.append(voice)
            
            # Selection priority: Brazilian Portuguese > Male > First available
            if brazilian_voices:
                # Prefer male Brazilian voice
                selected_voice = next((v for v in brazilian_voices if any(term in v.name.lower() for term in ['male', 'masculino', 'man', 'homem'])), brazilian_voices[0])
            elif male_voices:
                selected_voice = male_voices[0]
            else:
                # Fallback to second voice (often different from default)
                selected_voice = voices[1] if len(voices) > 1 else voices[0]
            
            if selected_voice:
                engine.setProperty('voice', selected_voice.id)
                print(f"[TTS] Using voice: {selected_voice.name} (ID: {selected_voice.id})")
            else:
                print("[TTS] Using default system voice")
        
        # Additional engine properties for better quality
        try:
            # Some engines support additional properties
            engine.setProperty('pitch', settings.get('pitch', 0.7))
        except Exception:
            pass  # Not all engines support pitch
        
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
    """Convert text to speech using gTTS (online) with improved voice quality."""
    try:
        if filename is None:
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            filename = temp_file.name
            temp_file.close()
        
        settings = get_voice_settings(user_id)
        lang = settings.get('language', 'pt-br')
        
        # Use gTTS with improved settings for more natural sound
        # Use slower speed for longer texts to improve clarity
        use_slow = len(text) > 200  # Use slower speech for longer texts
        
        # Improve TTS quality with better TLD selection for Brazilian Portuguese
        tld = 'com.br' if 'br' in lang else 'com'
        
        tts = gTTS(text=text, lang=lang, slow=use_slow, tld=tld)
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
    if method == 'offline':
        return speak_offline(text, user_id)
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
        print("Método inválido. Use 'offline' ou 'online'.")
        return False

def save_voice_usage(user_id: str, text: str, method: str, settings: Dict[str, Any]) -> None:
    """Save voice usage data for learning and adaptation with enhanced analytics."""
    try:
        import time
        
        # Calculate analytics
        text_length = len(text)
        word_count = len(text.split())
        estimated_duration = word_count / settings.get('rate', 200) * 60  # seconds
        
        # Try to import Firebase manager for cloud storage
        try:
            from firebase_integration import get_firebase_manager
            firebase_manager = get_firebase_manager()
            
            # Save detailed voice usage data
            voice_data = {
                'text_spoken': text,
                'method_used': method,
                'settings': settings,
                'text_length': text_length,
                'word_count': word_count,
                'estimated_duration': estimated_duration,
                'language': settings.get('language', 'pt-br'),
                'voice_quality_rating': None  # Can be filled by user feedback later
            }
            
            firebase_manager.save_voice_sample(user_id, voice_data)
            
            # Also save usage analytics
            analytics_data = {
                'method_used': method,
                'text_length': text_length,
                'word_count': word_count,
                'estimated_duration': estimated_duration,
                'settings_used': {
                    'rate': settings.get('rate'),
                    'volume': settings.get('volume'),
                    'pitch': settings.get('pitch')
                }
            }
            
            firebase_manager.save_voice_usage_analytics(user_id, analytics_data)
            
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
    """Adapt voice settings based on user feedback with improved learning."""
    settings = get_voice_settings(user_id)
    
    feedback_lower = feedback.lower()
    changes_made = []
    
    # Adjust settings based on feedback with more nuanced changes
    if any(term in feedback_lower for term in ['mais devagar', 'slower', 'muito rápido', 'too fast']):
        old_rate = settings.get('rate', 200)
        settings['rate'] = max(120, old_rate - 25)
        changes_made.append(f"velocidade reduzida de {old_rate} para {settings['rate']}")
        
    elif any(term in feedback_lower for term in ['mais rápido', 'faster', 'muito devagar', 'too slow']):
        old_rate = settings.get('rate', 200)
        settings['rate'] = min(280, old_rate + 25)
        changes_made.append(f"velocidade aumentada de {old_rate} para {settings['rate']}")
    
    if any(term in feedback_lower for term in ['mais baixo', 'quieter', 'muito alto', 'too loud']):
        old_volume = settings.get('volume', 0.9)
        settings['volume'] = max(0.2, old_volume - 0.15)
        changes_made.append(f"volume reduzido de {old_volume:.1f} para {settings['volume']:.1f}")
        
    elif any(term in feedback_lower for term in ['mais alto', 'louder', 'muito baixo', 'too quiet']):
        old_volume = settings.get('volume', 0.9)
        settings['volume'] = min(1.0, old_volume + 0.15)
        changes_made.append(f"volume aumentado de {old_volume:.1f} para {settings['volume']:.1f}")
    
    if any(term in feedback_lower for term in ['grave', 'deeper', 'voz mais grossa', 'lower pitch']):
        old_pitch = settings.get('pitch', 0.7)
        settings['pitch'] = max(0.4, old_pitch - 0.15)
        changes_made.append(f"tom reduzido de {old_pitch:.1f} para {settings['pitch']:.1f}")
        
    elif any(term in feedback_lower for term in ['agudo', 'higher', 'voz mais fina', 'higher pitch']):
        old_pitch = settings.get('pitch', 0.7)
        settings['pitch'] = min(1.2, old_pitch + 0.15)
        changes_made.append(f"tom aumentado de {old_pitch:.1f} para {settings['pitch']:.1f}")
    
    # New: Quality feedback handling
    if any(term in feedback_lower for term in ['mais natural', 'more natural', 'melhor qualidade', 'better quality']):
        # Adjust for more natural sound
        settings['rate'] = max(160, min(220, settings.get('rate', 200)))
        settings['pitch'] = max(0.6, min(0.9, settings.get('pitch', 0.7)))
        changes_made.append("ajustado para som mais natural")
    
    # Add timestamp and learning metadata
    settings['last_adapted'] = datetime.datetime.now().isoformat()
    settings['feedback_received'] = feedback
    settings['changes_made'] = changes_made
    
    # Save adapted settings with better error handling
    try:
        from firebase_integration import get_firebase_manager
        firebase_manager = get_firebase_manager()
        if firebase_manager.save_voice_sample(user_id, settings):
            print(f"[Voice Learning] Settings saved to Firebase: {', '.join(changes_made) if changes_made else 'no changes needed'}")
        else:
            raise Exception("Firebase save failed")
    except Exception as e:
        print(f"[Voice Learning] Saving to local storage (Firebase unavailable): {e}")
        # Save locally with improved structure
        _save_voice_profile_locally(user_id, settings)
    
    return settings

def _save_voice_profile_locally(user_id: str, settings: Dict[str, Any]) -> None:
    """Save voice profile locally with improved structure"""
    try:
        filename = f"aiden_voice_profiles_{user_id}.json"
        
        # Read existing profiles
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                profiles = json.load(f)
        except FileNotFoundError:
            profiles = []
        
        # Add new profile
        profiles.append(settings)
        
        # Keep only last 10 profiles to avoid large files
        if len(profiles) > 10:
            profiles = profiles[-10:]
        
        # Write back
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False, default=str)
            
        print(f"[Voice Learning] Profile saved locally to {filename}")
            
    except Exception as e:
        print(f"[ERROR] Failed to save voice profile locally: {e}")

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

