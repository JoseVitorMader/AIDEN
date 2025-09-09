import speech_recognition as sr
import json
import datetime
from typing import Dict, Any, Optional, List

def save_voice_characteristics(user_id: str, audio_data: Any, transcription: str) -> None:
    """Save voice characteristics for learning user's voice patterns."""
    try:
        from firebase_integration import get_firebase_manager
        firebase_manager = get_firebase_manager()
        
        voice_data = {
            'transcription': transcription,
            'text_length': len(transcription),
            'word_count': len(transcription.split()),
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        firebase_manager.save_voice_sample(user_id, voice_data)
        
    except Exception as e:
        print(f"[WARNING] Failed to save voice characteristics: {e}")

def get_optimized_recognition_settings(user_id: str = "default") -> Dict[str, Any]:
    """Get optimized speech recognition settings based on user's voice patterns."""
    try:
        from firebase_integration import get_firebase_manager
        firebase_manager = get_firebase_manager()
        profile = firebase_manager.get_voice_profile(user_id)
        
        if profile:
            # Use learned settings
            return {
                'energy_threshold': profile.get('energy_threshold', 300),
                'dynamic_energy_threshold': profile.get('dynamic_energy_threshold', True),
                'pause_threshold': profile.get('pause_threshold', 0.8),
                'phrase_threshold': profile.get('phrase_threshold', 0.3),
                'non_speaking_duration': profile.get('non_speaking_duration', 0.5)
            }
    except:
        pass
    
    # Default optimized settings for better voice capture
    return {
        'energy_threshold': 300,  # Adjust based on environment noise
        'dynamic_energy_threshold': True,  # Auto-adjust to ambient noise
        'pause_threshold': 0.8,  # Seconds of silence to consider end of phrase
        'phrase_threshold': 0.3,  # Minimum seconds of audio before phrase
        'non_speaking_duration': 0.5  # Seconds of non-speaking audio to keep
    }

def configure_recognizer(recognizer: sr.Recognizer, user_id: str = "default") -> sr.Recognizer:
    """Configure speech recognizer with optimized settings for better voice capture."""
    settings = get_optimized_recognition_settings(user_id)
    
    recognizer.energy_threshold = settings['energy_threshold']
    recognizer.dynamic_energy_threshold = settings['dynamic_energy_threshold']
    recognizer.pause_threshold = settings['pause_threshold']
    recognizer.phrase_threshold = settings['phrase_threshold']
    recognizer.non_speaking_duration = settings['non_speaking_duration']
    
    return recognizer

def recognize_speech_from_mic(recognizer, microphone, user_id: str = "default", timeout: int = 10, phrase_time_limit: int = 10):
    """Transcreve fala de um microfone para texto com configurações otimizadas."""
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` deve ser uma instância de `Recognizer`")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` deve ser uma instância de `Microphone`")

    # Configure recognizer with optimized settings
    recognizer = configure_recognizer(recognizer, user_id)

    with microphone as source:
        print("🔧 Ajustando para ruído ambiente...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎤 Ouvindo...")
        
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return {
                "success": False,
                "error": "Tempo limite de escuta excedido",
                "transcription": None
            }

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        # Try Google Speech Recognition with Portuguese (Brazil)
        transcription = recognizer.recognize_google(audio, language='pt-BR')
        response["transcription"] = transcription
        
        # Save voice characteristics for learning
        save_voice_characteristics(user_id, audio, transcription)
        
        print(f"✓ Reconhecido: {transcription}")
        
    except sr.RequestError as e:
        response["success"] = False
        response["error"] = f"API indisponível: {e}"
        print(f"❌ Erro de API: {e}")
        
    except sr.UnknownValueError:
        response["success"] = False  
        response["error"] = "Fala não reconhecida - tente falar mais claramente"
        print("❌ Não foi possível entender o áudio")

    return response

def improve_voice_recognition_settings(user_id: str, feedback: str, current_audio_quality: str = "good") -> Dict[str, Any]:
    """Improve voice recognition settings based on user feedback and audio quality."""
    settings = get_optimized_recognition_settings(user_id)
    feedback_lower = feedback.lower()
    
    # Adjust settings based on feedback
    if any(word in feedback_lower for word in ["não entendeu", "não reconheceu", "erro"]):
        # Increase sensitivity
        settings['energy_threshold'] = max(100, settings['energy_threshold'] - 50)
        settings['pause_threshold'] = min(1.2, settings['pause_threshold'] + 0.1)
        
    elif any(word in feedback_lower for word in ["muito sensível", "capturando ruído"]):
        # Decrease sensitivity
        settings['energy_threshold'] = min(1000, settings['energy_threshold'] + 50)
        settings['pause_threshold'] = max(0.5, settings['pause_threshold'] - 0.1)
        
    elif any(word in feedback_lower for word in ["cortando palavras", "muito rápido"]):
        # Increase patience
        settings['phrase_threshold'] = max(0.1, settings['phrase_threshold'] - 0.1)
        settings['non_speaking_duration'] = min(1.0, settings['non_speaking_duration'] + 0.1)
    
    # Save improved settings
    try:
        from firebase_integration import get_firebase_manager
        firebase_manager = get_firebase_manager()
        firebase_manager.save_voice_sample(user_id, settings)
    except:
        # Save locally as fallback
        filename = f"voice_recognition_settings_{user_id}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Failed to save recognition settings: {e}")
    
    return settings

if __name__ == "__main__":
    r = sr.Recognizer()
    
    try:
        mic = sr.Microphone()
        print("🎤 Sistema de reconhecimento de voz aprimorado")
        print("Diga algo (timeout: 10s)...")
        
        result = recognize_speech_from_mic(r, mic, user_id="test_user", timeout=10, phrase_time_limit=10)

        if result["success"]:
            print(f"✓ Você disse: {result['transcription']}")
            
            # Test feedback system
            feedback = input("Como foi o reconhecimento? (digite 'bom' ou descreva problemas): ")
            if feedback.lower() != 'bom':
                improved_settings = improve_voice_recognition_settings("test_user", feedback)
                print(f"✓ Configurações melhoradas: {improved_settings}")
        else:
            print(f"❌ Erro: {result['error']}")
            
    except Exception as e:
        print(f"❌ Erro ao inicializar microfone: {e}")
        print("💡 Certifique-se de que um microfone esteja conectado e funcionando.")


