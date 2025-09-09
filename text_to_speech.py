import pyttsx3
from gtts import gTTS
import os
import pygame
import tempfile
import time
from typing import Optional, Dict, Any, List
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
    
    # Default voice settings - male voice, less robotic, faster speed
    return {
        'rate': 200,  # Speaking rate (words per minute) - increased from 180
        'volume': 0.9,  # Volume level (0.0 to 1.0)
        'voice_id': 'male',  # Prefer male voice
        'pitch': 0.8,  # Lower pitch for more natural sound
        'language': 'pt-br',  # Portuguese Brazil
        'chunk_size': 200  # Maximum words per chunk for long texts
    }

def chunk_long_text(text: str, max_words: int = 200) -> List[str]:
    """
    Split long text into smaller chunks for better TTS processing.
    
    Args:
        text: The text to split
        max_words: Maximum number of words per chunk
    
    Returns:
        List of text chunks
    """
    # Split text into sentences first
    sentences = text.replace('.', '.|').replace('!', '!|').replace('?', '?|').split('|')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    chunks = []
    current_chunk = ""
    current_word_count = 0
    
    for sentence in sentences:
        sentence_words = len(sentence.split())
        
        # If adding this sentence would exceed the limit, start a new chunk
        if current_word_count + sentence_words > max_words and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
            current_word_count = sentence_words
        else:
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
            current_word_count += sentence_words
    
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

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
    """Convert text to speech using pyttsx3 (offline) with improved male voice and long text handling."""
    try:
        engine = pyttsx3.init()
        settings = get_voice_settings(user_id)
        
        # Configure the voice with user preferences
        configure_voice_engine(engine, settings)
        
        # Handle long texts by chunking them
        max_words = settings.get('chunk_size', 200)
        word_count = len(text.split())
        
        if word_count > max_words:
            print(f"[TTS] Long text detected ({word_count} words), chunking for better processing...")
            chunks = chunk_long_text(text, max_words)
            
            for i, chunk in enumerate(chunks):
                print(f"[TTS] Speaking chunk {i+1}/{len(chunks)}...")
                engine.say(chunk)
                engine.runAndWait()
                
                # Small pause between chunks for natural flow
                if i < len(chunks) - 1:
                    time.sleep(0.5)
        else:
            # Speak normally for shorter texts
            engine.say(text)
            engine.runAndWait()
        
        # Save voice usage data for learning
        save_voice_usage(user_id, text, 'offline', settings)
        
        return True
    except Exception as e:
        print(f"Erro ao usar pyttsx3: {e}")
        return False

def speak_online(text: str, user_id: str = "default", lang: str = 'pt-br', filename: Optional[str] = None) -> bool:
    """Convert text to speech using gTTS (online) with male voice preference and long text handling."""
    try:
        settings = get_voice_settings(user_id)
        lang = settings.get('language', 'pt-br')
        max_words = settings.get('chunk_size', 200)
        word_count = len(text.split())
        
        # Handle long texts by chunking them
        if word_count > max_words:
            print(f"[TTS Online] Long text detected ({word_count} words), chunking for better processing...")
            chunks = chunk_long_text(text, max_words)
            
            for i, chunk in enumerate(chunks):
                print(f"[TTS Online] Processing chunk {i+1}/{len(chunks)}...")
                
                # Create temporary file for this chunk
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'_chunk_{i}.mp3')
                chunk_filename = temp_file.name
                temp_file.close()
                
                # Use gTTS with slower speed for more natural sound
                tts = gTTS(text=chunk, lang=lang, slow=False, tld='com.br')
                tts.save(chunk_filename)
                
                # Play this chunk
                volume = settings.get('volume', 0.9)
                play_audio_file(chunk_filename, volume)
                
                # Clean up chunk file
                try:
                    os.remove(chunk_filename)
                except:
                    pass
                
                # Small pause between chunks for natural flow
                if i < len(chunks) - 1:
                    time.sleep(0.3)
        else:
            # Handle normal length texts
            if filename is None:
                # Create a temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                filename = temp_file.name
                temp_file.close()
            
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

