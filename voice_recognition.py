import speech_recognition as sr
import tempfile
import json
import datetime
from typing import Dict, Any, Optional

def analyze_voice_characteristics(audio_data) -> Dict[str, Any]:
    """
    Analyze voice characteristics from audio data for learning purposes
    
    Args:
        audio_data: Raw audio data from speech recognition
    
    Returns:
        Dict containing voice analysis data
    """
    try:
        # Basic analysis - in a real implementation, you might use librosa or similar
        analysis = {
            'sample_rate': getattr(audio_data, 'sample_rate', 'unknown'),
            'duration': getattr(audio_data, 'duration', 'unknown'),
            'frame_data_length': len(audio_data.frame_data) if hasattr(audio_data, 'frame_data') else 0,
            'analysis_timestamp': datetime.datetime.now().isoformat(),
        }
        
        # Add more sophisticated analysis here if needed
        # For now, we'll capture basic metadata
        
        return analysis
    except Exception as e:
        print(f"[Voice Analysis] Error analyzing voice: {e}")
        return {'error': str(e), 'analysis_timestamp': datetime.datetime.now().isoformat()}

def save_voice_sample_file(audio_data, user_id: str = "default") -> Optional[str]:
    """
    Save voice audio data to a temporary file for Firebase upload
    
    Args:
        audio_data: Raw audio data from speech recognition
        user_id: User identifier
    
    Returns:
        Path to saved file or None if failed
    """
    try:
        # Create temporary file for the audio
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'_voice_{user_id}.wav')
        filename = temp_file.name
        
        # Save audio data to file
        with open(filename, 'wb') as f:
            f.write(audio_data.get_wav_data())
        
        print(f"[Voice Sample] Saved to: {filename}")
        return filename
        
    except Exception as e:
        print(f"[Voice Sample] Error saving file: {e}")
        return None

def recognize_speech_from_mic(recognizer, microphone, user_id: str = "default", save_sample: bool = True):
    """Transcreve fala de um microfone para texto com análise e aprendizado de voz."""
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` deve ser uma instância de `Recognizer`")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` deve ser uma instância de `Microphone`")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)  # Ajusta para ruído ambiente
        print("Ouvindo...")
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None,
        "voice_analysis": None,
        "voice_file": None
    }

    try:
        # Recognize speech
        response["transcription"] = recognizer.recognize_google(audio, language='pt-BR')
        
        # Analyze voice characteristics if enabled
        if save_sample:
            analysis = analyze_voice_characteristics(audio)
            response["voice_analysis"] = analysis
            
            # Save voice sample file
            voice_file = save_voice_sample_file(audio, user_id)
            response["voice_file"] = voice_file
            
            # Upload to Firebase if available
            try:
                from firebase_integration import get_firebase_manager
                firebase_manager = get_firebase_manager()
                
                # Save analysis data
                firebase_manager.save_voice_analysis(user_id, analysis)
                
                # Upload voice file if we have one
                if voice_file:
                    metadata = {
                        'transcription': response["transcription"],
                        'analysis': analysis,
                        'recognition_engine': 'google',
                        'language': 'pt-BR'
                    }
                    download_url = firebase_manager.upload_voice_file(user_id, voice_file, metadata)
                    if download_url:
                        response["firebase_url"] = download_url
                    
                    # Clean up local file after upload
                    try:
                        import os
                        os.remove(voice_file)
                    except:
                        pass
                        
            except ImportError:
                print("[Voice Learning] Firebase not available - voice data saved locally only")
            except Exception as e:
                print(f"[Voice Learning] Error saving to Firebase: {e}")
        
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API indisponível"
    except sr.UnknownValueError:
        response["success"] = False
        response["error"] = "Fala não reconhecida"

    return response

if __name__ == "__main__":
    r = sr.Recognizer()
    mic = sr.Microphone()
    print("Diga algo!")
    result = recognize_speech_from_mic(r, mic)

    if result["success"]:
        print("Você disse: " + result["transcription"])
    else:
        print("Erro: {}".format(result["error"]))


