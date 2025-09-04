import google.generativeai as genai
import os
import datetime
import locale
from typing import Optional

# Safe import for dotenv
try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()
else:
    # Mild warning; not fatal since we can still use system environment variables
    if os.getenv("GOOGLE_API_KEY") is None and os.getenv("GEMINI_API_KEY") is None:
        print("[Aviso] python-dotenv não instalado. Instale com 'pip install python-dotenv' para carregar .env automaticamente.")

class ConversationalAI:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.chat = self.model.start_chat(history=[])
        
        # Set Portuguese locale for date/time formatting
        try:
            locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
            except:
                pass  # Fallback to system default

    def _get_current_datetime_info(self) -> str:
        """Get comprehensive current date and time information."""
        now = datetime.datetime.now()
        
        # Format in Portuguese
        date_str = now.strftime("%A, %d de %B de %Y")
        time_str = now.strftime("%H:%M:%S")
        
        # Additional context
        day_of_year = now.timetuple().tm_yday
        week_number = now.isocalendar()[1]
        
        return f"""
        Data e hora atual:
        - Data: {date_str}
        - Hora: {time_str}
        - Dia do ano: {day_of_year}
        - Semana do ano: {week_number}
        - Timestamp: {now.isoformat()}
        - Timezone: {now.astimezone().tzname()}
        """

    def _enhance_prompt_with_context(self, message: str) -> str:
        """Enhance the user's message with current context and capabilities."""
        
        # Check if the message is specifically asking for date/time information
        # Using more precise patterns to avoid false positives
        message_lower = message.lower()
        
        # Specific time/date question patterns
        time_question_patterns = [
            'que horas', 'que hora', 'qual hora', 'hora atual', 'horário',
            'que dia', 'qual data', 'data atual', 'data de hoje', 'hoje é',
            'what time', 'current time', 'what date', 'current date', 'today is',
            'quando é', 'que data é', 'calendário hoje'
        ]
        
        # Check for standalone time keywords (as complete words)
        standalone_time_words = ['agora', 'hoje', 'current', 'calendar', 'calendário']
        
        enhanced_prompt = f"""Você é AIDEN (Advanced Interactive Digital Enhancement Network), um assistente de IA inteligente.
        
        Suas capacidades incluem:
        - Acesso a informações de data e hora atuais
        - Conhecimento geral e conversação natural
        - Assistência com tarefas e perguntas
        - Respostas em português brasileiro
        
        Diretrizes de resposta:
        - Seja útil, profissional e amigável
        - Responda de forma conversacional mas informativa
        - Para perguntas sobre data/hora, use as informações atuais fornecidas
        - Mantenha respostas concisas mas completas
        """
        
        # Check if any time question pattern is present
        has_time_pattern = any(pattern in message_lower for pattern in time_question_patterns)
        
        # Check if message is only a standalone time word (or very short phrase with time word)
        is_standalone_time = any(
            word.strip() == message_lower.strip() or 
            (len(message_lower.split()) <= 2 and word in message_lower.split())
            for word in standalone_time_words
        )
        
        if has_time_pattern or is_standalone_time:
            enhanced_prompt += f"\n\nInformações atuais de data e hora:\n{self._get_current_datetime_info()}"
        
        enhanced_prompt += f"\n\nPergunta do usuário: {message}"
        
        return enhanced_prompt

    def send_message(self, message: str) -> str:
        """Send a message to the AI with enhanced context and error handling."""
        try:
            # Enhance the prompt with context
            enhanced_message = self._enhance_prompt_with_context(message)
            
            # Send to Gemini
            response = self.chat.send_message(enhanced_message)
            return response.text
            
        except Exception as e:
            print(f"Erro ao enviar mensagem para o Gemini API: {e}")
            
            # Provide intelligent fallback responses
            return self._generate_fallback_response(message)
    
    def _generate_fallback_response(self, message: str) -> str:
        """Generate intelligent fallback responses when API fails."""
        message_lower = message.lower()
        
        # Handle date/time queries locally using improved detection
        time_question_patterns = [
            'que horas', 'que hora', 'qual hora', 'hora atual', 'horário',
            'que dia', 'qual data', 'data atual', 'data de hoje', 'hoje é',
            'what time', 'current time', 'what date', 'current date', 'today is',
            'quando é', 'que data é', 'calendário hoje'
        ]
        
        standalone_time_words = ['agora', 'hoje', 'current', 'calendar', 'calendário']
        
        # Check if any time question pattern is present
        has_time_pattern = any(pattern in message_lower for pattern in time_question_patterns)
        
        # Check if message is only a standalone time word (or very short phrase with time word)
        is_standalone_time = any(
            word.strip() == message_lower.strip() or 
            (len(message_lower.split()) <= 2 and word in message_lower.split())
            for word in standalone_time_words
        )
        
        if has_time_pattern or is_standalone_time:
            return f"Informações atuais de data e hora:{self._get_current_datetime_info()}"
        
        # Handle greetings
        greeting_keywords = ['olá', 'oi', 'hello', 'hi', 'bom dia', 'boa tarde', 'boa noite']
        if any(keyword in message_lower for keyword in greeting_keywords):
            return "Olá! Sou o AIDEN, seu assistente de IA. Como posso ajudá-lo hoje? (Nota: Algumas funcionalidades avançadas estão temporariamente indisponíveis)"
        
        # Handle questions
        if message.endswith('?') or any(word in message_lower for word in ['como', 'what', 'how', 'why', 'quando', 'where']):
            return "Esta é uma pergunta interessante. Infelizmente, minhas capacidades de IA avançadas estão temporariamente indisponíveis, mas posso ajudar com informações básicas sobre sistema, data/hora e outras consultas simples."
        
        # Default response
        return "Desculpe, não consegui processar sua solicitação no momento devido a dificuldades técnicas com meus sistemas de IA avançados. Por favor, tente novamente ou reformule sua pergunta."

    def get_history(self):
        """Get chat history."""
        return self.chat.history
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.chat = self.model.start_chat(history=[])
        
    def get_ai_status(self) -> dict:
        """Get AI system status."""
        try:
            # Test API connection with a simple request
            test_response = self.model.generate_content("Test")
            return {
                "api_connected": True,
                "model": "gemini-1.5-flash",
                "status": "operational",
                "features": ["conversational_ai", "datetime_queries", "general_knowledge"]
            }
        except Exception as e:
            return {
                "api_connected": False,
                "model": "gemini-1.5-flash",
                "status": "error",
                "error": str(e),
                "fallback_features": ["datetime_queries", "basic_responses"]
            }

if __name__ == "__main__":
    # Substitua "YOUR_API_KEY" pela sua chave de API do Google Gemini
    # É altamente recomendável usar variáveis de ambiente para chaves de API
    # Ex: export GOOGLE_API_KEY="sua_chave_aqui"
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Por favor, defina a variável de ambiente GOOGLE_API_KEY.")
    else:
        ai = ConversationalAI(api_key)
        print("IA Conversacional iniciada. Digite 'sair' para encerrar.")
        while True:
            user_input = input("Você: ")
            if user_input.lower() == 'sair':
                break
            response = ai.send_message(user_input)
            print(f"IA: {response}")


