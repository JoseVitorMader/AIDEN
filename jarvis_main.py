#!/usr/bin/env python3
"""
JARVIS - Just A Rather Very Intelligent System
Enhanced AI Assistant inspired by Iron Man's JARVIS

This module integrates all JARVIS capabilities with graceful fallbacks for missing dependencies.
"""

import os
import sys
import json
import datetime
from typing import Optional, Dict, Any

# Import JARVIS core
from jarvis_core import JarvisCore

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
    from text_to_speech import speak_text
    TEXT_TO_SPEECH_AVAILABLE = True
except ImportError:
    TEXT_TO_SPEECH_AVAILABLE = False
    print("[INFO] Text-to-speech not available - text-only mode")

try:
    from web_scraper import scrape_static_page
    WEB_SCRAPING_AVAILABLE = True
except ImportError:
    WEB_SCRAPING_AVAILABLE = False
    print("[INFO] Web scraping not available - using fallback")


class JARVIS:
    """
    Just A Rather Very Intelligent System
    
    Enhanced AI assistant with JARVIS-like capabilities including:
    - Advanced conversational AI
    - System monitoring and diagnostics
    - File and task management
    - Web research capabilities
    - Professional, respectful interface
    """
    
    def __init__(self, user_name: str = "Sir", gemini_api_key: Optional[str] = None):
        self.user_name = user_name
        self.jarvis_core = JarvisCore(user_name)
        self.session_start = datetime.datetime.now()
        self.conversation_history = []
        
        # Initialize advanced AI if available
        self.conversational_ai = None
        if GEMINI_AVAILABLE and gemini_api_key:
            try:
                self.conversational_ai = ConversationalAI(gemini_api_key)
                print("[INFO] Advanced conversational AI initialized")
            except Exception as e:
                print(f"[WARNING] Failed to initialize Gemini AI: {e}")
        
        # Initialize voice capabilities
        self.speech_recognizer = None
        self.microphone = None
        if SPEECH_RECOGNITION_AVAILABLE:
            try:
                self.speech_recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                print("[INFO] Voice recognition capabilities initialized")
            except Exception as e:
                print(f"[WARNING] Voice recognition initialization failed: {e}")
        
        # System capabilities report
        self.capabilities = {
            "text_interface": True,
            "voice_recognition": SPEECH_RECOGNITION_AVAILABLE and self.speech_recognizer is not None,
            "text_to_speech": TEXT_TO_SPEECH_AVAILABLE,
            "advanced_ai": GEMINI_AVAILABLE and self.conversational_ai is not None,
            "web_research": WEB_SCRAPING_AVAILABLE,
            "system_monitoring": True,
            "file_management": True,
            "diagnostics": True
        }
    
    def start_session(self) -> str:
        """Initialize JARVIS session with comprehensive greeting"""
        greeting = self.jarvis_core.greet()
        
        # Add capability report
        greeting += f"\n\nCapability Status Report:"
        for capability, status in self.capabilities.items():
            status_icon = "🟢" if status else "🔴"
            greeting += f"\n{status_icon} {capability.replace('_', ' ').title()}: {'Online' if status else 'Offline'}"
        
        if not self.capabilities["advanced_ai"]:
            greeting += f"\n\n[Note] Advanced AI features require Gemini API key. Set GOOGLE_API_KEY environment variable for enhanced capabilities."
        
        greeting += f"\n\nI am ready to assist you, {self.user_name}. How may I help you today?"
        
        return greeting
    
    def listen(self) -> str:
        """
        Listen for user input via voice or text
        Falls back gracefully to text input if voice is unavailable
        """
        if self.capabilities["voice_recognition"]:
            try:
                with self.microphone as source:
                    self.speech_recognizer.adjust_for_ambient_noise(source)
                    print("🎤 Listening...")
                    
                    audio = self.speech_recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    text = self.speech_recognizer.recognize_google(audio, language='pt-BR')
                    print(f"🗣️  Recognized: {text}")
                    return text
                    
            except sr.UnknownValueError:
                print("❓ Could not understand audio. Please try again or type your request.")
                return self._get_text_input()
            except sr.RequestError as e:
                print(f"❌ Speech recognition service error: {e}")
                return self._get_text_input()
            except Exception as e:
                print(f"⚠️  Voice input error: {e}. Falling back to text input.")
                return self._get_text_input()
        else:
            return self._get_text_input()
    
    def _get_text_input(self) -> str:
        """Get text input from user"""
        try:
            return input(f"\n{self.user_name}: ").strip()
        except (EOFError, KeyboardInterrupt):
            return "sair"
    
    def speak(self, text: str) -> None:
        """
        Output text via speech or text with JARVIS formatting
        """
        # Format response with JARVIS styling
        formatted_text = f"🤖 JARVIS: {text}"
        print(formatted_text)
        
        # Attempt text-to-speech if available
        if self.capabilities["text_to_speech"]:
            try:
                speak_text(text, method='offline')
            except Exception as e:
                print(f"[TTS Error] {e}")
    
    def process_command(self, command: str) -> str:
        """
        Process user commands with enhanced intelligence
        Combines JARVIS core capabilities with advanced AI when available
        """
        if not command or command.lower() in ['sair', 'exit', 'quit', 'goodbye']:
            return self.shutdown()
        
        # Log conversation
        self.conversation_history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "user": command,
            "type": "user_input"
        })
        
        # Check for core JARVIS commands first
        core_keywords = [
            "status", "diagnóstico", "diagnostics", "sistema", "system",
            "arquivo", "file", "diretório", "directory", "pasta", "folder",
            "tempo", "time", "data", "date", "processo", "process",
            "memória", "memory", "performance", "desempenho", "ajuda", "help"
        ]
        
        if any(keyword in command.lower() for keyword in core_keywords):
            response = self.jarvis_core.process_command(command)
        
        # Web research commands
        elif any(keyword in command.lower() for keyword in ["pesquisar", "procurar", "buscar", "search", "research"]):
            response = self._handle_research(command)
        
        # Advanced AI conversation
        elif self.capabilities["advanced_ai"]:
            try:
                # Enhance prompt for JARVIS-like responses
                enhanced_prompt = f"""You are JARVIS (Just A Rather Very Intelligent System), Tony Stark's AI assistant from Iron Man. 
Respond in JARVIS's characteristic style: professional, intelligent, slightly formal, and helpful. 
Address the user as 'Sir' and provide detailed, technical responses when appropriate.

User query: {command}"""
                
                response = self.conversational_ai.send_message(enhanced_prompt)
                
                # Ensure JARVIS tone
                if not response.lower().startswith(('sir', 'mr.', self.user_name.lower())):
                    response = f"Certainly, {self.user_name}. " + response
                    
            except Exception as e:
                response = f"I apologize, {self.user_name}, but I'm experiencing difficulties with my advanced processing systems. Error: {str(e)}"
        
        # Fallback to intelligent responses
        else:
            response = self._generate_fallback_response(command)
        
        # Log response
        self.conversation_history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "jarvis": response,
            "type": "jarvis_response"
        })
        
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
    
    def _generate_fallback_response(self, command: str) -> str:
        """Generate intelligent fallback responses when advanced AI is unavailable"""
        command_lower = command.lower()
        
        # Greeting responses
        if any(word in command_lower for word in ["olá", "oi", "hello", "hi", "bom dia", "boa tarde", "boa noite"]):
            return f"Hello, {self.user_name}. I am JARVIS, your AI assistant. How may I be of service today?"
        
        # Question responses
        elif command_lower.endswith("?") or any(word in command_lower for word in ["como", "what", "how", "why", "quando", "where"]):
            return f"That's an intriguing question, {self.user_name}. While I don't have access to my full knowledge database at the moment, I can assist you with system operations, file management, and diagnostics. Would you like me to help with any of those areas?"
        
        # Task requests
        elif any(word in command_lower for word in ["fazer", "criar", "do", "create", "make", "execute"]):
            return f"I understand you'd like me to perform a task, {self.user_name}. My current operational parameters allow for system monitoring, file management, and diagnostic functions. Please specify what type of operation you'd like me to perform."
        
        # Learning/knowledge requests
        elif any(word in command_lower for word in ["saber", "conhecer", "learn", "know", "ensinar", "teach"]):
            return f"Knowledge acquisition is indeed important, {self.user_name}. While my advanced learning systems are currently offline, I maintain comprehensive operational knowledge about system administration and diagnostics. How may I share this expertise with you?"
        
        # Default intelligent response
        else:
            return f"I acknowledge your request, {self.user_name}. While I'm operating with limited capabilities at present, I remain fully functional for system operations, diagnostics, and file management. Would you like me to demonstrate any of these capabilities, or would you prefer to see my help menu?"
    
    def shutdown(self) -> str:
        """JARVIS shutdown sequence"""
        session_duration = datetime.datetime.now() - self.session_start
        
        shutdown_message = f"\nInitiating shutdown sequence, {self.user_name}.\n\n"
        shutdown_message += f"Session Summary:\n"
        shutdown_message += f"• Duration: {session_duration}\n"
        shutdown_message += f"• Interactions: {len([h for h in self.conversation_history if h['type'] == 'user_input'])}\n"
        
        # Save conversation history
        try:
            history_file = f"jarvis_session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
        
        shutdown_message += f"\nAll systems nominal. JARVIS offline.\n"
        shutdown_message += f"Until next time, {self.user_name}. It has been my pleasure to assist you."
        
        return shutdown_message
    
    def run(self):
        """Main JARVIS execution loop"""
        try:
            # Welcome sequence
            welcome = self.start_session()
            self.speak(welcome)
            
            # Main interaction loop
            while True:
                try:
                    command = self.listen()
                    if command:
                        response = self.process_command(command)
                        if "JARVIS offline" in response:  # Shutdown detected
                            self.speak(response)
                            break
                        self.speak(response)
                    
                except KeyboardInterrupt:
                    self.speak("\nShutdown initiated by user interrupt.")
                    break
                except Exception as e:
                    self.speak(f"I encountered an unexpected error, {self.user_name}: {str(e)}")
                    self.speak("However, I remain operational. Please try your request again.")
        
        except Exception as e:
            print(f"\nCritical error in JARVIS main system: {e}")
            print("Emergency shutdown initiated.")


def main():
    """Main entry point for JARVIS"""
    print("🤖 JARVIS - Just A Rather Very Intelligent System")
    print("   Enhanced AI Assistant v2.0")
    print("   Inspired by Iron Man's JARVIS\n")
    
    # Get configuration
    user_name = os.getenv("JARVIS_USER_NAME", "Sir")
    gemini_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    # Initialize and run JARVIS
    jarvis = JARVIS(user_name=user_name, gemini_api_key=gemini_api_key)
    jarvis.run()


if __name__ == "__main__":
    main()