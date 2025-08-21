## Fase 1: Análise de requisitos e arquitetura do sistema

- [x] Definir as tecnologias e bibliotecas a serem utilizadas para reconhecimento de voz: SpeechRecognition (com suporte a Google Speech Recognition API para online e PocketSphinx para offline), Whisper (OpenAI) para maior precisão. (Assumindo funcionalidade em ambiente com áudio real)
- [x] Definir as tecnologias e bibliotecas a serem utilizadas para síntese de fala: pyttsx3 (offline) e gTTS (online).
- [x] Definir as tecnologias e bibliotecas a serem utilizadas para webscraping: BeautifulSoup e Requests para web scraping simples, Selenium para interações mais complexas com JavaScript.
- [x] Definir a arquitetura geral do sistema (módulos, comunicação entre eles): Módulos separados para Reconhecimento de Voz (ASR), Processamento de Linguagem Natural (NLP) e Geração de Resposta, Síntese de Fala (TTS) e Web Scraping. Comunicação via APIs internas.
- [x] Esboçar um plano de como a IA conversacional será implementada (fluxo de diálogo, gerenciamento de contexto): Utilizar um modelo de linguagem grande (LLM) para o núcleo conversacional, com capacidade de gerenciar o contexto da conversa e integrar informações do web scraping. Fluxo de diálogo baseado em intenções e entidades.
- [x] Considerar requisitos de hardware e software para execução contínua: Execução em ambiente Linux, com Python 3.x. Requisitos de RAM e CPU dependerão do LLM escolhido e da carga de trabalho de web scraping. Considerar o uso de Docker para orquestração e fácil implantação.

## Fase 2: Implementação do sistema de reconhecimento de voz

- [x] Instalar as bibliotecas necessárias (SpeechRecognition, PyAudio).
- [x] Criar um módulo Python para reconhecimento de voz.
- [x] Implementar a funcionalidade de gravação de áudio do microfone.
- [x] Implementar a conversão de audio para texto usando a API do Google Speech Recognition.
- [x] Adicionar tratamento de erros para áudio não reconhecido ou problemas de conexão.

## Fase 3: Implementação do sistema de síntese de fala

- [x] Instalar as bibliotecas necessárias (pyttsx3, gTTS).
- [x] Criar um módulo Python para síntese de fala.
- [x] Implementar a conversão de texto para fala usando pyttsx3 (offline).
- [x] Implementar a conversão de texto para fala usando gTTS (online).
- [x] Adicionar tratamento de erros para problemas de síntese.

## Fase 4: Desenvolvimento do módulo de webscraping

- [x] Instalar as bibliotecas necessárias (BeautifulSoup, Requests, Selenium).
- [x] Criar um módulo Python para webscraping.
- [x] Implementar funcionalidade de webscraping básico com Requests e BeautifulSoup.
- [x] Implementar funcionalidade de webscraping para páginas dinâmicas com Selenium.
- [x] Adicionar tratamento de erros para falhas de requisição e parsing.

## Fase 5: Criação do sistema de conversação e IA

- [x] Definir a API ou biblioteca para o modelo de linguagem grande (LLM): Google Gemini API (via `google-generativeai` Python library).
- [x] Implementar a lógica de processamento de linguagem natural (NLP) para entender a intenção e entidades.
- [x] Desenvolver o gerenciamento de contexto da conversa.
- [x] Integrar o módulo de webscraping para responder a perguntas baseadas em informações da web.
- [x] Implementar a lógica de geração de resposta.
- [x] Adicionar tratamento de erros para falhas na comunicação com o LLM ou no processamento de NLP.




## Fase 6: Integração e sistema de execução contínua

- [x] Criar um script principal para orquestrar todos os módulos (reconhecimento de voz, IA conversacional, síntese de fala, webscraping).
- [x] Implementar um loop de execução contínua para a IA.
- [x] Configurar o ambiente para execução em segundo plano (daemon).
- [x] Adicionar mecanismos de resiliência e reinício automático em caso de falha.




## Fase 7: Testes e demonstração do sistema

- [x] Realizar testes unitários e de integração de cada módulo.
- [x] Testar o fluxo completo da IA (voz para texto, processamento, webscraping, texto para voz).
- [x] Demonstrar a capacidade da IA de conversar e responder a perguntas usando webscraping.
- [x] Documentar os resultados dos testes.


