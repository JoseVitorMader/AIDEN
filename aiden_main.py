#!/usr/bin/env python3
"""
AIDEN - Advanced Interactive Digital Enhancement Network
Enhanced AI Assistant with sophisticated system monitoring and voice capabilities

This module integrates all AIDEN capabilities with graceful fallbacks for missing dependencies.
"""

import os
import sys
import json
import datetime
from typing import Optional, Dict, Any, List

# Import AIDEN core
from aiden_core import AidenCore

# Safe imports with fallbacks
try:
    from conversational_ai import ConversationalAI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("[INFO] Gemini AI module not available - using fallback responses")

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("[INFO] Speech recognition not available - text-only mode")

try:
    from text_to_speech import speak_text, adapt_voice_settings
    TEXT_TO_SPEECH_AVAILABLE = True
except ImportError:
    TEXT_TO_SPEECH_AVAILABLE = False
    print("[INFO] Text-to-speech not available - text-only mode")

try:
    from web_scraper import search_web, get_page_summary
    WEB_SCRAPING_AVAILABLE = True
except ImportError:
    WEB_SCRAPING_AVAILABLE = False
    print("[INFO] Web scraping not available - using fallback")


class AIDEN:
    """
    Advanced Interactive Digital Enhancement Network
    
    Enhanced AI assistant with voice-first capabilities including:
    - Advanced conversational AI with Firebase storage
    - Prioritized voice input and audio output
    - System monitoring and diagnostics
    - Firebase-integrated search and data storage
    - Professional, helpful interface
    """
    
    def __init__(self, user_name: str = "User", gemini_api_key: Optional[str] = None):
        self.user_name = user_name
        self.aiden_core = AidenCore(user_name)
        self.session_start = datetime.datetime.now()
        self.conversation_history = []
        
        # Initialize Firebase integration
        try:
            from firebase_integration import get_firebase_manager
            self.firebase_manager = get_firebase_manager()
            print("[INFO] Firebase integration initialized")
        except ImportError:
            self.firebase_manager = None
            print("[WARNING] Firebase integration not available")
        
        # Initialize advanced AI if available
        self.conversational_ai = None
        if GEMINI_AVAILABLE and gemini_api_key:
            try:
                self.conversational_ai = ConversationalAI(gemini_api_key)
                print("[INFO] Advanced conversational AI initialized")
            except Exception as e:
                print(f"[WARNING] Failed to initialize Gemini AI: {e}")
        
        # Initialize voice capabilities with priority on audio
        self.speech_recognizer = None
        self.microphone = None
        if SPEECH_RECOGNITION_AVAILABLE:
            try:
                self.speech_recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                # Adjust recognition settings for better voice detection
                self.speech_recognizer.energy_threshold = 300
                self.speech_recognizer.dynamic_energy_threshold = True
                self.speech_recognizer.pause_threshold = 0.8
                print("[INFO] Voice recognition capabilities initialized and optimized")
            except Exception as e:
                print(f"[WARNING] Voice recognition initialization failed: {e}")
        
        # System capabilities report
        self.capabilities = {
            "text_interface": True,
            "voice_recognition": SPEECH_RECOGNITION_AVAILABLE and self.speech_recognizer is not None,
            "text_to_speech": TEXT_TO_SPEECH_AVAILABLE,
            "advanced_ai": GEMINI_AVAILABLE and self.conversational_ai is not None,
            "web_research": WEB_SCRAPING_AVAILABLE,
            "firebase_storage": self.firebase_manager is not None,
            "system_monitoring": True,
            "file_management": True,
            "diagnostics": True
        }
    
    def start_session(self) -> str:
        """Initialize AIDEN session with comprehensive greeting"""
        greeting = self.aiden_core.greet()
        
        # Add capability report
        greeting += f"\n\nCapability Status Report:"
        for capability, status in self.capabilities.items():
            status_icon = "🟢" if status else "🔴"
            greeting += f"\n{status_icon} {capability.replace('_', ' ').title()}: {'Online' if status else 'Offline'}"
        
        if not self.capabilities["advanced_ai"]:
            greeting += f"\n\n[Note] Advanced AI features require Gemini API key. Set GOOGLE_API_KEY environment variable for enhanced capabilities."
        
        if self.capabilities["voice_recognition"]:
            greeting += f"\n\n🎤 Voice input is ready! I'll prioritize listening to you speak."
        
        greeting += f"\n\nI am AIDEN, ready to assist you, {self.user_name}. How may I help you today?"
        
        return greeting
    
    def listen(self) -> str:
        """
        Listen for user input via voice or text
        PRIORITIZES voice input - voice is the primary interface for AIDEN
        """
        if self.capabilities["voice_recognition"]:
            try:
                with self.microphone as source:
                    # More aggressive noise adjustment for better voice detection
                    print("🎤 Adjusting for ambient noise...")
                    self.speech_recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("🎤 Listening for your voice... (speak clearly)")
                    
                    # Longer timeout and phrase limit for natural conversation
                    audio = self.speech_recognizer.listen(source, timeout=10, phrase_time_limit=15)
                    text = self.speech_recognizer.recognize_google(audio, language='pt-BR')
                    print(f"🗣️  Recognized: {text}")
                    return text
                    
            except sr.WaitTimeoutError:
                print("⏰ Voice timeout - no speech detected. You can type instead or try speaking again.")
                return self._get_text_input()
            except sr.UnknownValueError:
                print("❓ Could not understand speech clearly. Please try again or type your request.")
                return self._get_text_input()
            except sr.RequestError as e:
                print(f"❌ Speech recognition service error: {e}")
                return self._get_text_input()
            except Exception as e:
                print(f"⚠️  Voice input error: {e}. Falling back to text input.")
                return self._get_text_input()
        else:
            print("ℹ️  Voice input not available. Using text mode.")
            return self._get_text_input()
    
    def _get_text_input(self) -> str:
        """Get text input from user"""
        try:
            return input(f"\n{self.user_name}: ").strip()
        except (EOFError, KeyboardInterrupt):
            return "sair"
    
    def speak(self, text: str) -> None:
        """
        Output text via speech or text with AIDEN formatting
        PRIORITIZES audio output - speech is the primary interface for AIDEN
        """
        # Format response with AIDEN styling
        formatted_text = f"🤖 AIDEN: {text}"
        print(formatted_text)
        
        # PRIORITY: Attempt text-to-speech if available
        if self.capabilities["text_to_speech"]:
            try:
                # Use improved TTS with user-specific voice settings
                if not speak_text(text, method='offline', user_id=self.user_name):
                    # Fallback to online TTS if offline fails
                    speak_text(text, method='online', user_id=self.user_name)
                    print("🔊 Audio output: Online TTS used")
                else:
                    print("🔊 Audio output: Offline TTS used")
            except Exception as e:
                print(f"🔇 TTS Error: {e} - Audio output unavailable")
        else:
            print("🔇 Text-to-speech not available - text only mode")
    
    def process_command(self, command: str) -> str:
        """
        Process user commands with enhanced intelligence and Firebase integration
        Combines AIDEN core capabilities with advanced AI and Firebase storage/search
        """
        if not command or command.lower() in ['sair', 'exit', 'quit', 'goodbye', 'tchau']:
            return self.shutdown()
        
        # Log conversation
        self.conversation_history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "user": command,
            "type": "user_input"
        })
        
        # Check Firebase for previous related searches FIRST
        previous_results = []
        if self.firebase_manager:
            try:
                previous_results = self.firebase_manager.search_previous_results(command, 3)
                if previous_results:
                    print(f"🔍 Found {len(previous_results)} related previous searches in database")
            except Exception as e:
                print(f"[Firebase Search Error] {e}")
        
        # Check for voice adaptation commands
        if any(keyword in command.lower() for keyword in ["voz", "voice", "falar", "speak", "volume", "velocidade", "grave", "agudo"]):
            return self._handle_voice_adaptation(command)
        
        # Check for core AIDEN commands first
        core_keywords = [
            "status", "diagnóstico", "diagnostics", "sistema", "system",
            "arquivo", "file", "diretório", "directory", "pasta", "folder",
            "tempo", "time", "data", "date", "processo", "process",
            "memória", "memory", "performance", "desempenho", "ajuda", "help"
        ]
        
        if any(keyword in command.lower() for keyword in core_keywords):
            response = self.aiden_core.process_command(command)
            
            # Save system command results to Firebase
            if self.firebase_manager:
                try:
                    self.firebase_manager.save_search_result(command, response, "system")
                except Exception as e:
                    print(f"[Firebase Save Error] {e}")
        
        # Web research commands with Firebase integration
        elif any(keyword in command.lower() for keyword in ["pesquisar", "procurar", "buscar", "search", "research"]):
            response = self._handle_research_with_firebase(command, previous_results)
        
        # Advanced AI conversation with Firebase storage
        elif self.capabilities["advanced_ai"]:
            try:
                # If we have previous results, include them in the context
                context_addition = ""
                if previous_results:
                    context_addition = f"\n\nRelevant previous information from database:\n"
                    for i, result in enumerate(previous_results[:2], 1):
                        context_addition += f"{i}. {result.get('query')}: {result.get('result')[:200]}...\n"
                
                # Enhanced prompt for AIDEN-like responses
                enhanced_prompt = f"""You are AIDEN (Advanced Interactive Digital Enhancement Network), an intelligent AI assistant. 
Respond in a helpful, professional, and friendly manner. 
Address the user naturally and provide detailed, accurate responses when appropriate.
Be conversational yet informative.
{context_addition}
User query: {command}"""
                
                response = self.conversational_ai.send_message(enhanced_prompt)
                
                # Save conversation to Firebase
                if self.firebase_manager:
                    try:
                        self.firebase_manager.save_conversation(command, response)
                        self.firebase_manager.save_search_result(command, response, "ai_conversation")
                    except Exception as e:
                        print(f"[Firebase Save Error] {e}")
                    
            except Exception as e:
                response = f"I apologize, {self.user_name}, but I'm experiencing difficulties with my advanced processing systems. Error: {str(e)}"
        
        # Fallback to intelligent responses with Firebase context
        else:
            response = self._generate_fallback_response(command, previous_results)
        
        # Log response
        self.conversation_history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "aiden": response,
            "type": "aiden_response"
        })
        
        return response
    
    def _handle_research_with_firebase(self, command: str, previous_results: List[Dict]) -> str:
        """Handle web research requests with Firebase integration"""
        query = command.lower()
        for term in ["pesquisar", "procurar", "buscar", "search", "research"]:
            query = query.replace(term, "").strip()
        
        response = f"Searching for: '{query}'\n\n"
        
        # Check if we have relevant previous results first
        if previous_results:
            response += "📋 Found relevant information from previous searches:\n\n"
            for i, result in enumerate(previous_results, 1):
                response += f"{i}. Previous: {result.get('query')}\n"
                response += f"   Result: {result.get('result')[:300]}...\n\n"
            response += "🔍 Now searching for new information...\n\n"
        
        if self.capabilities["web_research"]:
            try:
                # Use enhanced web search
                search_results = search_web(query, num_results=3)
                
                if search_results.get("results"):
                    response += "🌐 New web research results:\n\n"
                    
                    for i, result in enumerate(search_results["results"], 1):
                        response += f"{i}. {result.get('title', 'Sem título')}\n"
                        response += f"   {result.get('snippet', 'Sem descrição')}\n\n"
                    
                    # Save comprehensive results to Firebase
                    if self.firebase_manager:
                        try:
                            results_text = json.dumps(search_results, ensure_ascii=False, indent=2)
                            self.firebase_manager.save_search_result(query, results_text, "web")
                            response += "💾 Research results saved to database for future reference.\n"
                        except Exception as e:
                            print(f"[Firebase Save Error] {e}")
                else:
                    response += "🔍 Web search completed, but no clear results were found."
                    
            except Exception as e:
                response += f"Research systems are currently experiencing technical difficulties: {str(e)}"
        else:
            response += "Web research capabilities are currently offline. I recommend using a web browser to search for this information manually."
        
        return response
    
    def _handle_research(self, command: str) -> str:
        """Handle web research requests"""
        query = command.lower()
        for term in ["pesquisar", "procurar", "buscar", "search", "research"]:
            query = query.replace(term, "").strip()
        
        response = f"Initiating web research for: '{query}', {self.user_name}.\n\n"
        
        if self.capabilities["web_research"]:
            try:
                # Perform web search
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                soup = scrape_static_page(search_url)
                
                if soup:
                    # Try to extract search results
                    snippets = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")[:3]
                    if snippets:
                        response += "🔍 Research Results:\n\n"
                        for i, snippet in enumerate(snippets, 1):
                            response += f"{i}. {snippet.get_text()}\n\n"
                    else:
                        response += "Research completed, but I was unable to extract clear results from the current search format."
                else:
                    response += "I encountered difficulties accessing web resources for your research request."
                    
            except Exception as e:
                response += f"Research systems are currently experiencing technical difficulties: {str(e)}"
        else:
            response += "Web research capabilities are currently offline. I recommend using a web browser to search for this information manually."
        
        return response
    
    def _generate_fallback_response(self, command: str, previous_results: List[Dict] = None) -> str:
        """Generate intelligent fallback responses when advanced AI is unavailable"""
        command_lower = command.lower()
        
        # Include previous results context if available
        context_note = ""
        if previous_results:
            context_note = f"\n\nI found some related information from our previous conversations:\n"
            for result in previous_results[:1]:  # Show one relevant result
                context_note += f"• {result.get('query')}: {result.get('result')[:150]}...\n"
        
        # Greeting responses
        if any(word in command_lower for word in ["olá", "oi", "hello", "hi", "bom dia", "boa tarde", "boa noite"]):
            return f"Hello, {self.user_name}. I am AIDEN, your Advanced Interactive Digital Enhancement Network. How may I assist you today?{context_note}"
        
        # Question responses
        elif command_lower.endswith("?") or any(word in command_lower for word in ["como", "what", "how", "why", "quando", "where"]):
            return f"That's an interesting question, {self.user_name}. While I don't have access to my full AI capabilities at the moment, I can help with system operations, file management, and diagnostics.{context_note}"
        
        # Task requests
        elif any(word in command_lower for word in ["fazer", "criar", "do", "create", "make", "execute"]):
            return f"I understand you'd like me to perform a task, {self.user_name}. I can assist with system monitoring, file management, and diagnostic functions. Please specify what you'd like me to do.{context_note}"
        
        # Learning/knowledge requests
        elif any(word in command_lower for word in ["saber", "conhecer", "learn", "know", "ensinar", "teach"]):
            return f"Knowledge is important, {self.user_name}. I maintain operational knowledge about system administration and diagnostics, and I can search our conversation history for relevant information.{context_note}"
        
        # Default intelligent response
        else:
            return f"I acknowledge your request, {self.user_name}. I'm ready to help with system operations, diagnostics, file management, and can search our previous conversations for relevant information.{context_note}"
    
    def _handle_voice_adaptation(self, command: str) -> str:
        """Handle voice adaptation commands"""
        try:
            if TEXT_TO_SPEECH_AVAILABLE:
                adapted_settings = adapt_voice_settings(self.user_name, command)
                return f"Configurações de voz adaptadas com base no seu feedback: velocidade={adapted_settings.get('rate')}, volume={adapted_settings.get('volume'):.1f}, tom={adapted_settings.get('pitch'):.1f}. Experimentando as novas configurações agora!"
            else:
                return "As funcionalidades de adaptação de voz não estão disponíveis no momento. Instale as dependências de áudio para usar este recurso."
        except Exception as e:
            return f"Erro ao adaptar configurações de voz: {str(e)}"
    
    def shutdown(self) -> str:
        """AIDEN shutdown sequence"""
        session_duration = datetime.datetime.now() - self.session_start
        
        shutdown_message = f"\nInitiating shutdown sequence, {self.user_name}.\n\n"
        shutdown_message += f"Session Summary:\n"
        shutdown_message += f"• Duration: {session_duration}\n"
        shutdown_message += f"• Interactions: {len([h for h in self.conversation_history if h['type'] == 'user_input'])}\n"
        
        # Save conversation history
        try:
            history_file = f"aiden_session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "session_start": self.session_start.isoformat(),
                    "session_duration": str(session_duration),
                    "user_name": self.user_name,
                    "capabilities": self.capabilities,
                    "conversation_history": self.conversation_history
                }, f, indent=2, ensure_ascii=False)
            shutdown_message += f"• Session log saved: {history_file}\n"
        except Exception as e:
            shutdown_message += f"• Session log: Unable to save ({str(e)})\n"
        
        # Save final conversation to Firebase if available
        if self.firebase_manager:
            try:
                self.firebase_manager.save_conversation("shutdown", shutdown_message)
                shutdown_message += f"• Session data saved to Firebase\n"
            except Exception as e:
                print(f"[Firebase Save Error] {e}")
        
        shutdown_message += f"\nAll systems nominal. AIDEN offline.\n"
        shutdown_message += f"Thank you for using AIDEN, {self.user_name}. Have a great day!"
        
        return shutdown_message
    
    def run(self):
        """Main AIDEN execution loop with voice-first interaction"""
        try:
            # Welcome sequence with voice priority
            welcome = self.start_session()
            self.speak(welcome)
            
            # Continuous voice interaction reminder
            if self.capabilities["voice_recognition"]:
                self.speak("Voice mode is active! I'll be listening for your voice commands as the primary input method.")
            
            # Main interaction loop
            while True:
                try:
                    command = self.listen()
                    if command:
                        response = self.process_command(command)
                        if "AIDEN offline" in response:  # Shutdown detected
                            self.speak(response)
                            break
                        self.speak(response)
                    
                except KeyboardInterrupt:
                    self.speak(f"\nShutdown initiated by user interrupt, {self.user_name}.")
                    break
                except Exception as e:
                    self.speak(f"I encountered an unexpected error, {self.user_name}: {str(e)}")
                    self.speak("However, I remain operational. Please try your request again.")
        
        except Exception as e:
            print(f"\nCritical error in AIDEN main system: {e}")
            print("Emergency shutdown initiated.")


def main():
    """Main entry point for AIDEN"""
    print("🤖 AIDEN - Advanced Interactive Digital Enhancement Network")
    print("   Voice-First AI Assistant with Firebase Integration")
    print("   Prioritizing Audio Input/Output\n")
    
    # Get configuration
    user_name = os.getenv("AIDEN_USER_NAME", "User")
    gemini_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    # Initialize and run AIDEN
    aiden = AIDEN(user_name=user_name, gemini_api_key=gemini_api_key)
    aiden.run()


if __name__ == "__main__":
    main()