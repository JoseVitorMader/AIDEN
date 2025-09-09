import speech_recognition as sr
import json
import datetime
from typing import Dict, Any, Optional

def recognize_speech_from_mic(recognizer, microphone, user_id="default", collect_voice_data=True):
    """Transcreve fala de um microfone para texto e coleta dados de voz para aprendizado."""
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` deve ser uma instância de `Recognizer`")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` deve ser uma instância de `Microphone`")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Increased duration for better adaptation
        print("🎤 Ouvindo... (Melhorando captação de voz)")
        
        try:
            # Enhanced listening with longer timeout and better settings
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            
            # Collect voice characteristics for learning
            if collect_voice_data:
                voice_characteristics = _analyze_voice_characteristics(audio, recognizer)
            else:
                voice_characteristics = {}
                
        except sr.WaitTimeoutError:
            return {
                "success": False,
                "error": "Timeout - nenhuma fala detectada",
                "transcription": None,
                "voice_data": {}
            }

    response = {
        "success": True,
        "error": None,
        "transcription": None,
        "voice_data": voice_characteristics,
        "confidence": None
    }

    try:
        # Try multiple recognition methods for better accuracy
        transcription = None
        confidence = 0.0
        
        # Primary method: Google Speech Recognition
        try:
            transcription = recognizer.recognize_google(audio, language='pt-BR', show_all=True)
            if isinstance(transcription, dict) and 'alternative' in transcription:
                alternatives = transcription['alternative']
                if alternatives:
                    best_alternative = alternatives[0]
                    transcription = best_alternative.get('transcript', '')
                    confidence = best_alternative.get('confidence', 0.0)
            elif isinstance(transcription, str):
                confidence = 0.8  # Default confidence for simple string response
            
        except sr.UnknownValueError:
            # Fallback: try with different settings
            try:
                transcription = recognizer.recognize_google(audio, language='pt-BR')
                confidence = 0.6  # Lower confidence for fallback
            except:
                transcription = None
        
        if transcription:
            response["transcription"] = transcription
            response["confidence"] = confidence
            
            # Save voice learning data
            if collect_voice_data:
                _save_voice_learning_data(user_id, audio, transcription, voice_characteristics, confidence)
        else:
            response["success"] = False
            response["error"] = "Fala não reconhecida com clareza"
            
    except sr.RequestError as e:
        response["success"] = False
        response["error"] = f"Erro no serviço de reconhecimento: {e}"
    except Exception as e:
        response["success"] = False
        response["error"] = f"Erro inesperado: {e}"

    return response

def _analyze_voice_characteristics(audio, recognizer) -> Dict[str, Any]:
    """Analisa características da voz para aprendizado e adaptação"""
    try:
        # Basic audio analysis - in a full implementation, this would use more sophisticated audio processing
        characteristics = {
            'timestamp': datetime.datetime.now().isoformat(),
            'sample_rate': getattr(audio, 'sample_rate', 16000),
            'sample_width': getattr(audio, 'sample_width', 2),
            'frame_count': len(audio.frame_data) if hasattr(audio, 'frame_data') else 0,
            'audio_length_seconds': len(audio.frame_data) / (16000 * 2) if hasattr(audio, 'frame_data') else 0,
        }
        
        # Additional voice characteristics could be added here:
        # - Pitch analysis
        # - Speaking rate
        # - Voice timbre
        # - Accent detection
        
        return characteristics
        
    except Exception as e:
        print(f"[Voice Analysis Error]: {e}")
        return {
            'timestamp': datetime.datetime.now().isoformat(),
            'error': str(e)
        }

def _save_voice_learning_data(user_id: str, audio, transcription: str, characteristics: Dict[str, Any], confidence: float):
    """Salva dados de voz para aprendizado no Firebase"""
    try:
        # Try to use Firebase integration
        try:
            from firebase_integration import get_firebase_manager
            firebase_manager = get_firebase_manager()
            
            voice_learning_data = {
                'transcription': transcription,
                'confidence': confidence,
                'characteristics': characteristics,
                'audio_metadata': {
                    'duration': characteristics.get('audio_length_seconds', 0),
                    'sample_rate': characteristics.get('sample_rate', 16000),
                    'frame_count': characteristics.get('frame_count', 0)
                },
                'learning_context': 'voice_recognition'
            }
            
            firebase_manager.save_voice_sample(user_id, voice_learning_data)
            print(f"[Voice Learning] Dados salvos no Firebase para usuário: {user_id}")
            
        except ImportError:
            # Fallback to local storage
            _save_voice_data_locally(user_id, transcription, characteristics, confidence)
            
    except Exception as e:
        print(f"[Voice Learning Error]: {e}")

def _save_voice_data_locally(user_id: str, transcription: str, characteristics: Dict[str, Any], confidence: float):
    """Salva dados de voz localmente como fallback"""
    try:
        filename = f"aiden_voice_learning_{user_id}.json"
        
        data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'transcription': transcription,
            'confidence': confidence,
            'characteristics': characteristics
        }
        
        # Read existing data
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []
        
        # Append new data
        existing_data.append(data)
        
        # Keep only last 200 entries to avoid large files
        if len(existing_data) > 200:
            existing_data = existing_data[-200:]
        
        # Write back
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
        print(f"[Voice Learning] Dados salvos localmente: {filename}")
        
    except Exception as e:
        print(f"[Local Voice Save Error]: {e}")

def get_voice_learning_stats(user_id: str) -> Dict[str, Any]:
    """Obtem estatísticas de aprendizado de voz do usuário"""
    try:
        # Try Firebase first
        try:
            from firebase_integration import get_firebase_manager
            firebase_manager = get_firebase_manager()
            # This would need implementation in firebase_integration.py
            # For now, use local fallback
            raise ImportError("Using local fallback for stats")
            
        except ImportError:
            return _get_local_voice_stats(user_id)
            
    except Exception as e:
        print(f"[Voice Stats Error]: {e}")
        return {}

def _get_local_voice_stats(user_id: str) -> Dict[str, Any]:
    """Obtem estatísticas locais de aprendizado de voz"""
    try:
        filename = f"aiden_voice_learning_{user_id}.json"
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data:
            return {}
        
        # Calculate basic stats
        total_samples = len(data)
        avg_confidence = sum(d.get('confidence', 0) for d in data) / total_samples
        recent_samples = [d for d in data if 
                         (datetime.datetime.now() - datetime.datetime.fromisoformat(d['timestamp'])).days < 7]
        
        return {
            'total_voice_samples': total_samples,
            'average_confidence': avg_confidence,
            'recent_samples_week': len(recent_samples),
            'last_sample': data[-1]['timestamp'] if data else None,
            'voice_quality_trend': 'improving' if avg_confidence > 0.7 else 'needs_improvement'
        }
        
    except FileNotFoundError:
        return {'message': 'No voice learning data found'}
    except Exception as e:
        print(f"[Local Stats Error]: {e}")
        return {'error': str(e)}

if __name__ == "__main__":
    r = sr.Recognizer()
    mic = sr.Microphone()
    print("🎙️ Teste de captura de voz melhorada - Diga algo!")
    result = recognize_speech_from_mic(r, mic, user_id="test_user")

    if result["success"]:
        print(f"✅ Você disse: {result['transcription']}")
        print(f"📊 Confiança: {result.get('confidence', 'N/A')}")
        print(f"🎵 Dados de voz coletados: {bool(result.get('voice_data'))}")
        
        # Show voice learning stats
        stats = get_voice_learning_stats("test_user")
        if stats:
            print(f"📈 Estatísticas de aprendizado: {stats}")
    else:
        print(f"❌ Erro: {result['error']}")


