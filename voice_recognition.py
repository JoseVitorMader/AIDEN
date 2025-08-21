import speech_recognition as sr

def recognize_speech_from_mic(recognizer, microphone):
    """Transcreve fala de um microfone para texto."""
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
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language='pt-BR')
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


