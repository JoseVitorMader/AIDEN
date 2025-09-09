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

# Import AIDEN core for enhanced capabilities
try:
    from aiden_core import AidenCore
    AIDEN_CORE_AVAILABLE = True
except ImportError:
    AIDEN_CORE_AVAILABLE = False
    print("[INFO] AIDEN core not available - using basic mode")

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
    def __init__(self, gemini_api_key, enable_aiden_mode=True, user_name="User"):
        """
        Initialize ManusAI with optional AIDEN enhancement
        
        Args:
            gemini_api_key: API key for Gemini AI
            enable_aiden_mode: Enable AIDEN-like advanced features
            user_name: Name to address the user
        """
        self.enable_aiden_mode = enable_aiden_mode and AIDEN_CORE_AVAILABLE
        self.user_name = user_name
        
        # Initialize AIDEN core if available and enabled
        if self.enable_aiden_mode:
            self.aiden_core = AidenCore(user_name)
            print(f"[INFO] AIDEN mode enabled - Enhanced capabilities active")
        else:
            self.aiden_core = None
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
                prompt = f"\n{self.user_name}: " if self.enable_aiden_mode else "Digite: "
                return input(prompt)
            except EOFError:
                return ""

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("🎤 Ouvindo...")
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
        # Enhanced AIDEN-style output
        if self.enable_aiden_mode:
            print(f"🤖 AIDEN: {text}")
        else:
            print(f"IA: {text}")
            
        # Attempt text-to-speech if available
        if TEXT_TO_SPEECH_AVAILABLE:
            try:
                # Handle large texts by chunking them for better TTS processing
                self._speak_with_chunking(text, method)
            except Exception as e:
                print(f"[TTS Error]: {e}")
                
    def _speak_with_chunking(self, text, method='online', max_chunk_size=800):
        """
        Break large texts into smaller chunks for better TTS processing
        
        Args:
            text: Text to speak
            method: TTS method ('online' or 'offline')
            max_chunk_size: Maximum characters per chunk
        """
        try:
            from text_to_speech import speak_text
            
            # If text is short enough, speak directly
            if len(text) <= max_chunk_size:
                speak_text(text, method, user_id=self.user_name)
                return
            
            # Split text into sentences for more natural chunking
            import re
            # Split by sentence endings, keeping the punctuation
            sentences = re.split(r'(?<=[.!?])\s+', text)
            
            current_chunk = ""
            
            for sentence in sentences:
                # If adding this sentence would exceed chunk size, speak current chunk
                if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
                    speak_text(current_chunk.strip(), method, user_id=self.user_name)
                    current_chunk = sentence
                else:
                    current_chunk = current_chunk + " " + sentence if current_chunk else sentence
            
            # Speak any remaining text
            if current_chunk.strip():
                speak_text(current_chunk.strip(), method, user_id=self.user_name)
                
            # Save conversation data to Firebase for learning
            self._save_conversation_data(text)
                
        except Exception as e:
            print(f"[Chunking Error]: {e}")
            # Fallback to direct speaking attempt
            try:
                from text_to_speech import speak_text
                speak_text(text[:max_chunk_size], method, user_id=self.user_name)
            except Exception as fallback_error:
                print(f"[Fallback TTS Error]: {fallback_error}")
    
    def _save_conversation_data(self, ai_response):
        """Save conversation data to Firebase for voice learning"""
        try:
            from firebase_integration import get_firebase_manager
            firebase_manager = get_firebase_manager()
            
            # Get the last user input (this is a simple approach)
            user_input = getattr(self, '_last_user_input', 'Unknown')
            firebase_manager.save_conversation(user_input, ai_response)
            
        except Exception as e:
            # Graceful failure - don't interrupt the conversation
            print(f"[Firebase Warning]: Could not save conversation data: {e}")

    def process_command(self, command):
        # Store last user input for conversation logging
        self._last_user_input = command
        
        # Enhanced AIDEN processing
        if self.enable_aiden_mode and self.aiden_core:
            # Check if this is an AIDEN system command
            aiden_keywords = [
                "status", "diagnóstico", "diagnostics", "sistema", "system",
                "arquivo", "file", "diretório", "directory", "pasta", "folder",
                "tempo", "time", "data", "date", "processo", "process",
                "memória", "memory", "performance", "desempenho", "informação", "information"
            ]
            
            if any(keyword in command.lower() for keyword in aiden_keywords):
                response = self.aiden_core.process_command(command)
                self.speak(response)
                return
        
        # Web search logic (enhanced for AIDEN)
        if "pesquisar" in command.lower() or "procurar" in command.lower():
            query = command.lower().replace("pesquisar", "").replace("procurar", "").strip()
            
            if self.enable_aiden_mode:
                self.speak(f"Iniciando pesquisa para '{query}', {self.user_name}.")
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
                            if self.enable_aiden_mode:
                                self.speak(f"Pesquisa concluída, {self.user_name}. {snippet.get_text()}")
                            else:
                                self.speak(f"Encontrei isto: {snippet.get_text()}")
                        else:
                            self.speak("Pesquisa concluída, mas não encontrei resultados claros no formato atual.")
                    else:
                        self.speak("Encontrei dificuldades para acessar recursos web.")
                except Exception as e:
                    self.speak(f"Sistemas de pesquisa web estão enfrentando dificuldades técnicas: {str(e)}")
            else:
                self.speak("Capacidades de pesquisa web estão atualmente offline.")
            return

        # Conversational AI processing
        if self.conversational_ai:
            try:
                # Enhanced prompt for AIDEN mode
                if self.enable_aiden_mode:
                    enhanced_command = f"""Você é AIDEN (Advanced Interactive Digital Enhancement Network), um assistente de IA inteligente. 
Responda de forma útil, profissional e amigável. 
Dirija-se ao usuário como '{self.user_name}' e forneça respostas detalhadas quando apropriado.
Seja conversacional, mas informativo, como um assistente digital sofisticado.

Consulta do usuário: {command}"""
                    response = self.conversational_ai.send_message(enhanced_command)
                    
                    # Ensure AIDEN tone in response
                    if not any(term in response.lower() for term in [self.user_name.lower(), 'usuário']):
                        response = f"Certamente, {self.user_name}. " + response
                else:
                    response = self.conversational_ai.send_message(command)
                    
                self.speak(response)
            except Exception as e:
                if self.enable_aiden_mode:
                    self.speak(f"Peço desculpas, {self.user_name}, mas estou enfrentando dificuldades com meus sistemas de processamento avançado.")
                else:
                    self.speak("Desculpe, não consegui processar sua solicitação no momento.")
        else:
            # Fallback responses
            self._fallback_response(command)
    
    def _fallback_response(self, command):
        """Provide intelligent fallback responses when AI is unavailable"""
        command_lower = command.lower()
        
        if self.enable_aiden_mode:
            if any(word in command_lower for word in ["olá", "oi", "hello", "hi"]):
                self.speak(f"Olá, {self.user_name}. Estou operando com capacidades limitadas, mas permaneço ao seu serviço.")
            elif "?" in command or any(word in command_lower for word in ["como", "what", "why", "quando"]):
                self.speak(f"Essa é uma pergunta intrigante, {self.user_name}. Embora meus sistemas avançados estejam offline, posso ajudar com diagnósticos e operações do sistema.")
            else:
                self.speak(f"Reconheço sua solicitação, {self.user_name}. Minhas capacidades atuais incluem monitoramento do sistema e gerenciamento de arquivos. Como posso ajudá-lo?")
        else:
            self.speak("Desculpe, não consegui entender completamente sua solicitação. Tente comandos como 'status do sistema' ou 'ajuda'.")

    def run(self):
        # Enhanced greeting for AIDEN mode
        if self.enable_aiden_mode:
            greeting = f"Boa tarde, {self.user_name}. Sistemas AIDEN estão agora online."
            if not CONVERSATIONAL_AI_AVAILABLE:
                greeting += f"\n\nNota: Recursos avançados de IA requerem configuração adequada. Atualmente operando em modo de diagnóstico aprimorado."
            greeting += f"\n\nComo posso ajudá-lo hoje, {self.user_name}?"
        else:
            greeting = "Olá! Eu sou a Manus. Como posso ajudar?"
            
        self.speak(greeting)
        
        while True:
            command = self.listen()
            if command:
                if command.lower() in ["parar", "sair", "exit", "quit"]:
                    if self.enable_aiden_mode:
                        farewell = f"Sistemas AIDEN desligando. Até a próxima, {self.user_name}."
                    else:
                        farewell = "Até logo!"
                    self.speak(farewell)
                    break
                self.process_command(command)

if __name__ == "__main__":
    gemini_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    # Check for AIDEN mode preference
    aiden_mode = os.getenv("AIDEN_MODE", "true").lower() == "true"
    user_name = os.getenv("AIDEN_USER_NAME", "User")
    
    print("🤖 AIDEN - Advanced Interactive Digital Enhancement Network")
    print("   Enhanced with voice-first capabilities")
    print(f"   Mode: {'AIDEN Enhanced' if aiden_mode else 'Standard Manus'}")
    print(f"   User: {user_name}\n")
    
    if not gemini_api_key:
        print("Note: Para recursos avançados de IA, defina a variável GOOGLE_API_KEY ou GEMINI_API_KEY.")
        print("Operating in diagnostic and system management mode.\n")
    
    ai = ManusAI(gemini_api_key, enable_aiden_mode=aiden_mode, user_name=user_name)
    ai.run()


