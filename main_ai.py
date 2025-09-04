import os
import sys

# Safe imports with fallbacks for enhanced JARVIS mode
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    sr = None
    print("[INFO] Speech recognition not available - using text mode")

try:
    from conversational_ai import ConversationalAI
    CONVERSATIONAL_AI_AVAILABLE = True
except ImportError:
    CONVERSATIONAL_AI_AVAILABLE = False
    print("[INFO] Conversational AI not available - using basic responses")

try:
    from text_to_speech import speak_text
    TEXT_TO_SPEECH_AVAILABLE = True
except ImportError:
    TEXT_TO_SPEECH_AVAILABLE = False
    print("[INFO] Text-to-speech not available - text only mode")

try:
    from web_scraper import scrape_static_page, scrape_dynamic_page
    WEB_SCRAPER_AVAILABLE = True
except ImportError:
    WEB_SCRAPER_AVAILABLE = False
    print("[INFO] Web scraper not available")

# Import JARVIS core for enhanced capabilities
try:
    from jarvis_core import JarvisCore
    JARVIS_CORE_AVAILABLE = True
except ImportError:
    JARVIS_CORE_AVAILABLE = False
    print("[INFO] JARVIS core not available - using basic mode")

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
    def __init__(self, gemini_api_key, enable_jarvis_mode=True, user_name="Sir"):
        """
        Initialize ManusAI with optional JARVIS enhancement
        
        Args:
            gemini_api_key: API key for Gemini AI
            enable_jarvis_mode: Enable JARVIS-like advanced features
            user_name: Name to address the user (JARVIS style)
        """
        self.enable_jarvis_mode = enable_jarvis_mode and JARVIS_CORE_AVAILABLE
        self.user_name = user_name
        
        # Initialize JARVIS core if available and enabled
        if self.enable_jarvis_mode:
            self.jarvis_core = JarvisCore(user_name)
            print(f"[INFO] JARVIS mode enabled - Enhanced capabilities active")
        else:
            self.jarvis_core = None
            print(f"[INFO] Standard mode - Basic capabilities only")
        
        # Initialize speech recognition with fallback
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            # Tenta inicializar microfone; se PyAudio não instalado ou dispositivo ausente, faz fallback para modo texto
            try:
                self.microphone = sr.Microphone()
            except Exception as e:
                print("[Aviso] Não foi possível inicializar o microfone (PyAudio ausente ou dispositivo indisponível). Fallback para entrada por texto.")
                print(f"Detalhe: {e}")
                self.microphone = None
        else:
            self.recognizer = None
            self.microphone = None
            
        # Initialize conversational AI with fallback
        if CONVERSATIONAL_AI_AVAILABLE and gemini_api_key:
            try:
                self.conversational_ai = ConversationalAI(gemini_api_key)
            except Exception as e:
                print(f"[ERROR] Failed to initialize Gemini AI: {e}")
                self.conversational_ai = None
        else:
            self.conversational_ai = None

    def listen(self):
        if not self.recognizer or not self.microphone:
            # modo texto
            try:
                prompt = f"\n{self.user_name}: " if self.enable_jarvis_mode else "Digite: "
                return input(prompt)
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
        # Enhanced JARVIS-style output
        if self.enable_jarvis_mode:
            print(f"🤖 JARVIS: {text}")
        else:
            print(f"IA: {text}")
            
        # Attempt text-to-speech if available
        if TEXT_TO_SPEECH_AVAILABLE:
            try:
                speak_text(text, method)
            except Exception as e:
                print(f"[TTS Error]: {e}")

    def process_command(self, command):
        # Enhanced JARVIS processing
        if self.enable_jarvis_mode and self.jarvis_core:
            # Check if this is a JARVIS system command
            jarvis_keywords = [
                "status", "diagnóstico", "diagnostics", "sistema", "system",
                "arquivo", "file", "diretório", "directory", "pasta", "folder",
                "tempo", "time", "data", "date", "processo", "process",
                "memória", "memory", "performance", "desempenho", "informação", "information"
            ]
            
            if any(keyword in command.lower() for keyword in jarvis_keywords):
                response = self.jarvis_core.process_command(command)
                self.speak(response)
                return
        
        # Web search logic (enhanced for JARVIS)
        if "pesquisar" in command.lower() or "procurar" in command.lower():
            query = command.lower().replace("pesquisar", "").replace("procurar", "").strip()
            
            if self.enable_jarvis_mode:
                self.speak(f"Initiating web research for '{query}', {self.user_name}.")
            else:
                self.speak(f"Claro, vou pesquisar por {query} na web.")
            
            # Web scraping if available
            if WEB_SCRAPER_AVAILABLE:
                try:
                    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                    soup = scrape_static_page(search_url)
                    if soup:
                        snippet = soup.find("div", class_="BNeawe s3v9rd AP7Wnd")
                        if snippet:
                            if self.enable_jarvis_mode:
                                self.speak(f"Research complete, {self.user_name}. {snippet.get_text()}")
                            else:
                                self.speak(f"Encontrei isto: {snippet.get_text()}")
                        else:
                            self.speak("Research completed, but no clear results were found in the current format.")
                    else:
                        self.speak("I encountered difficulties accessing web resources.")
                except Exception as e:
                    self.speak(f"Web research systems are experiencing technical difficulties: {str(e)}")
            else:
                self.speak("Web research capabilities are currently offline.")
            return

        # Conversational AI processing
        if self.conversational_ai:
            try:
                # Enhanced prompt for JARVIS mode
                if self.enable_jarvis_mode:
                    enhanced_command = f"""You are JARVIS (Just A Rather Very Intelligent System), Tony Stark's AI assistant. 
Respond in JARVIS's characteristic style: professional, intelligent, respectful, and helpful. 
Address the user as '{self.user_name}' and provide detailed responses when appropriate.
Be formal but friendly, like a sophisticated British butler with advanced AI capabilities.

User query: {command}"""
                    response = self.conversational_ai.send_message(enhanced_command)
                    
                    # Ensure JARVIS tone in response
                    if not any(term in response.lower() for term in [self.user_name.lower(), 'sir', 'mr.']):
                        response = f"Certainly, {self.user_name}. " + response
                else:
                    response = self.conversational_ai.send_message(command)
                    
                self.speak(response)
            except Exception as e:
                if self.enable_jarvis_mode:
                    self.speak(f"I apologize, {self.user_name}, but I'm experiencing difficulties with my advanced processing systems.")
                else:
                    self.speak("Desculpe, não consegui processar sua solicitação no momento.")
        else:
            # Fallback responses
            self._fallback_response(command)
    
    def _fallback_response(self, command):
        """Provide intelligent fallback responses when AI is unavailable"""
        command_lower = command.lower()
        
        if self.enable_jarvis_mode:
            if any(word in command_lower for word in ["olá", "oi", "hello", "hi"]):
                self.speak(f"Hello, {self.user_name}. I am operating with limited capabilities, but I remain at your service.")
            elif "?" in command or any(word in command_lower for word in ["como", "what", "why", "quando"]):
                self.speak(f"That's an intriguing question, {self.user_name}. While my advanced systems are offline, I can assist with diagnostics and system operations.")
            else:
                self.speak(f"I acknowledge your request, {self.user_name}. My current capabilities include system monitoring and file management. How may I assist you?")
        else:
            self.speak("Desculpe, não consegui entender completamente sua solicitação. Tente comandos como 'status do sistema' ou 'ajuda'.")

    def run(self):
        # Enhanced greeting for JARVIS mode
        if self.enable_jarvis_mode:
            greeting = f"Good afternoon, {self.user_name}. JARVIS systems are now online."
            if not CONVERSATIONAL_AI_AVAILABLE:
                greeting += f"\n\nNote: Advanced AI capabilities require proper configuration. Currently operating in enhanced diagnostic mode."
            greeting += f"\n\nHow may I assist you today, {self.user_name}?"
        else:
            greeting = "Olá! Eu sou a Manus. Como posso ajudar?"
            
        self.speak(greeting)
        
        while True:
            command = self.listen()
            if command:
                if command.lower() in ["parar", "sair", "exit", "quit"]:
                    if self.enable_jarvis_mode:
                        farewell = f"JARVIS systems going offline. Until next time, {self.user_name}."
                    else:
                        farewell = "Até logo!"
                    self.speak(farewell)
                    break
                self.process_command(command)

if __name__ == "__main__":
    gemini_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    # Check for JARVIS mode preference
    jarvis_mode = os.getenv("JARVIS_MODE", "true").lower() == "true"
    user_name = os.getenv("JARVIS_USER_NAME", "Sir")
    
    print("🤖 AIDEN/JARVIS - AI Assistant System")
    print("   Enhanced with JARVIS capabilities")
    print(f"   Mode: {'JARVIS Enhanced' if jarvis_mode else 'Standard Manus'}")
    print(f"   User: {user_name}\n")
    
    if not gemini_api_key:
        print("Note: Para recursos avançados de IA, defina a variável GOOGLE_API_KEY ou GEMINI_API_KEY.")
        print("Operating in diagnostic and system management mode.\n")
    
    ai = ManusAI(gemini_api_key, enable_jarvis_mode=jarvis_mode, user_name=user_name)
    ai.run()


