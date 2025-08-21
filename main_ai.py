import os
import speech_recognition as sr
from conversational_ai import ConversationalAI
from text_to_speech import speak_text
from web_scraper import scrape_static_page, scrape_dynamic_page

# Importa dotenv de forma segura
try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()
else:
    if os.getenv("GOOGLE_API_KEY") is None and os.getenv("GEMINI_API_KEY") is None:
        print("[Aviso] python-dotenv não instalado. Use 'pip install python-dotenv' ou defina a variável de ambiente manualmente.")

class ManusAI:
    def __init__(self, gemini_api_key):
        self.recognizer = sr.Recognizer()
        # Tenta inicializar microfone; se PyAudio não instalado ou dispositivo ausente, faz fallback para modo texto
        try:
            self.microphone = sr.Microphone()
        except Exception as e:
            print("[Aviso] Não foi possível inicializar o microfone (PyAudio ausente ou dispositivo indisponível). Fallback para entrada por texto.")
            print(f"Detalhe: {e}")
            self.microphone = None
        self.conversational_ai = ConversationalAI(gemini_api_key)

    def listen(self):
        if not self.microphone:
            # modo texto
            try:
                return input("Digite: ")
            except EOFError:
                return ""

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Ouvindo...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio, language='pt-BR')
                print(f"Você disse: {text}")
                return text
            except sr.UnknownValueError:
                print("Não entendi o que você disse.")
                return ""
            except sr.RequestError as e:
                print(f"Erro no serviço de reconhecimento de fala: {e}")
                return ""
            except Exception as e:
                print(f"Erro ao ouvir: {e}")
                return ""

    def speak(self, text, method='online'):
        print(f"IA: {text}")
        speak_text(text, method)

    def process_command(self, command):
        # Lógica para processar comandos e integrar webscraping
        if "pesquisar" in command.lower() or "procurar" in command.lower():
            query = command.lower().replace("pesquisar", "").replace("procurar", "").strip()
            self.speak(f"Claro, vou pesquisar por {query} na web.")
            # Exemplo simples: tentar raspar uma página estática
            # Em um cenário real, você precisaria de uma lógica mais sofisticada para determinar a URL
            # e se a página é estática ou dinâmica.
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            soup = scrape_static_page(search_url)
            if soup:
                # Tenta extrair um snippet da pesquisa
                snippet = soup.find("div", class_="BNeawe s3v9rd AP7Wnd")
                if snippet:
                    self.speak(f"Encontrei isto: {snippet.get_text()}")
                else:
                    self.speak("Não consegui encontrar um snippet relevante para sua pesquisa.")
            else:
                self.speak("Não consegui realizar a pesquisa na web.")
            return

        response = self.conversational_ai.send_message(command)
        self.speak(response)

    def run(self):
        self.speak("Olá! Eu sou a Manus. Como posso ajudar?")
        while True:
            command = self.listen()
            if command:
                if command.lower() == "parar":
                    self.speak("Até logo!")
                    break
                self.process_command(command)

if __name__ == "__main__":
    gemini_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("Por favor, defina a variável de ambiente GOOGLE_API_KEY ou GEMINI_API_KEY.")
    else:
        ai = ManusAI(gemini_api_key)
        ai.run()


