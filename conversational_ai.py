import google.generativeai as genai
import os

# Importa dotenv de forma segura (caso não esteja instalado ainda)
try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:
    load_dotenv = None  # fallback

if load_dotenv:
    load_dotenv()
else:
    # Aviso leve; não é erro fatal porque ainda podemos usar variáveis de ambiente do sistema
    if os.getenv("GOOGLE_API_KEY") is None and os.getenv("GEMINI_API_KEY") is None:
        print("[Aviso] python-dotenv não instalado. Instale com 'pip install python-dotenv' para carregar .env automaticamente.")

class ConversationalAI:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message):
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            print(f"Erro ao enviar mensagem para o Gemini API: {e}")
            return "Desculpe, não consegui processar sua solicitação no momento."

    def get_history(self):
        return self.chat.history

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


