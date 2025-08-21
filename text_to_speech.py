import pyttsx3
from gtts import gTTS
import os
import pygame

def speak_offline(text):
    """Converte texto em fala usando pyttsx3 (offline)."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return True
    except Exception as e:
        print(f"Erro ao usar pyttsx3: {e}")
        return False

def speak_online(text, lang='pt', filename='output.mp3'):
    """Converte texto em fala usando gTTS (online) e salva em arquivo."""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filename)
        return True
    except Exception as e:
        print(f"Erro ao usar gTTS: {e}")
        return False

def play_audio_file(filename):
    """Reproduz um arquivo de áudio usando pygame."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        return True
    except Exception as e:
        print(f"Erro ao reproduzir áudio: {e}")
        return False

def speak_text(text, method='offline'):
    """Função principal para síntese de fala."""
    if method == 'offline':
        return speak_offline(text)
    elif method == 'online':
        filename = 'temp_audio.mp3'
        if speak_online(text, filename=filename):
            result = play_audio_file(filename)
            # Limpa o arquivo temporário
            if os.path.exists(filename):
                os.remove(filename)
            return result
        return False
    else:
        print("Método inválido. Use 'offline' ou 'online'.")
        return False

if __name__ == "__main__":
    text = "Olá! Este é um teste do sistema de síntese de fala."
    print("Testando síntese offline...")
    speak_text(text, method='offline')
    
    print("Testando síntese online...")
    speak_text(text, method='online')

