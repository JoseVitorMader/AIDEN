# AIDEN - Advanced Interactive Digital Enhancement Network

**Assistente de IA com Voz Inteligente e Aprendizado Adaptativo**

AIDEN é um assistente de IA sofisticado que prioriza interação por voz e inclui recursos avançados de aprendizado de voz, integração com Firebase Realtime Database e capacidades aprimoradas de IA.

## 🚀 Principais Recursos

### Interface Prioritária por Voz
- **Entrada de Voz Prioritária**: Reconhecimento de voz como método principal de entrada
- **Saída de Áudio Aprimorada**: Síntese de fala com voz masculina menos robótica
- **Aprendizado de Voz**: Adapta-se gradualmente às preferências do usuário
- **Fallbacks Inteligentes**: Modo texto quando a voz não está disponível

### Aprendizado e Adaptação de Voz
- **Voz Masculina**: Configurado para usar vozes masculinas por padrão
- **Menos Robótica**: Configurações otimizadas para som mais natural
- **Aprendizado Adaptativo**: Armazena preferências e se adapta ao uso
- **Personalização**: Velocidade, volume e tom ajustáveis

### Integração Firebase Realtime Database
- **Armazenamento de Conversas**: Todas as interações salvas no Firebase
- **Histórico de Pesquisas**: Resultados de pesquisa preservados para referência futura
- **Perfis de Voz**: Dados de aprendizado de voz armazenados para melhoria contínua
- **Memória Persistente**: Informações persistem entre sessões

### Capacidades Avançadas de IA
- **Consultas de Data/Hora**: Respostas precisas sobre data e hora atual
- **Conversas Inteligentes**: Alimentado por Google Gemini AI
- **Pesquisa Web Aprimorada**: Busca integrada com extração melhorada de resultados
- **Memória Contextual**: Lembra e referencia interações anteriores

## 🛠 Instalação e Configuração

### Requisitos do Sistema
```bash
# Instalar dependências do sistema (Linux)
sudo apt-get update
sudo apt-get install portaudio19-dev python3-dev python3-pip

# Para Ubuntu/Debian
sudo apt-get install espeak espeak-data libespeak1 libespeak-dev

# Para sistemas com snapd
sudo snap install chromium
```

### Dependências Python
```bash
# Instalar dependências principais
pip install -r requirements.txt

# Se pyaudio falhar, instale primeiro as dependências do sistema:
sudo apt-get install portaudio19-dev python3-dev
pip install pyaudio
```

### Pacotes Necessários
- `google-generativeai` - Para conversas de IA avançadas
- `SpeechRecognition` - Para entrada de voz
- `pyttsx3` - Para síntese de fala offline (voz masculina)
- `gTTS` - Para síntese de fala online
- `pygame` - Para reprodução de áudio
- `firebase-admin` - Para integração Firebase Realtime Database
- `requests` - Para operações web
- `beautifulsoup4` - Para web scraping aprimorado

## ⚙️ Configuração

### Variáveis de Ambiente

1. **Copie o arquivo de exemplo:**
```bash
cp .env.example .env
```

2. **Configure suas chaves de API:**
```bash
# Edite o arquivo .env com suas configurações
nano .env
```

#### Configuração de IA (Obrigatória para recursos avançados)
```bash
# Chave da API do Google Gemini
# Obtenha em: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY="sua_chave_gemini_aqui"

# Nome do usuário - como AIDEN vai se dirigir a você
AIDEN_USER_NAME="Seu Nome"

# Ativar modo aprimorado
AIDEN_MODE=true
```

#### Configuração Firebase (Pré-configurada)
O Firebase Realtime Database já está configurado para uso básico:
- Projeto: `aiden-dd627`
- URL do Database: `https://aiden-dd627-default-rtdb.firebaseio.com/`
- Configuração automática para armazenamento de conversas e aprendizado de voz
- Nenhuma configuração adicional necessária para funcionalidade básica

#### Para Uso Avançado do Firebase
Se quiser usar seu próprio projeto Firebase:

1. **Crie um projeto no Firebase Console:**
   - Vá para https://console.firebase.google.com/
   - Crie um novo projeto
   - Ative o Realtime Database
   - Configure as regras de segurança

2. **Configure as variáveis de ambiente:**
```bash
FIREBASE_PROJECT_ID=seu-projeto-id
FIREBASE_DATABASE_URL=https://seu-projeto-id-default-rtdb.firebaseio.com/
```

3. **Para produção, use uma chave de conta de serviço:**
```bash
# Baixe a chave de conta de serviço do Firebase Console
# Salve como serviceAccountKey.json no diretório do projeto
GOOGLE_APPLICATION_CREDENTIALS=./serviceAccountKey.json
```

### Configuração de Voz

O AIDEN aprende e se adapta às suas preferências de voz automaticamente. Configurações iniciais:

```bash
# Configurações padrão de voz (serão adaptadas com o tempo)
VOICE_RATE=180        # Velocidade de fala (palavras por minuto)
VOICE_VOLUME=0.9      # Volume (0.0 a 1.0)
VOICE_LANGUAGE=pt-br  # Idioma (português brasileiro)
```

## 🎮 Uso

### Início Rápido (Modo Prioritário por Voz)
```bash
python aiden_main.py
```

### Interface Alternativa
```bash
python main_ai.py
```

### Comandos de Voz
AIDEN responde em português e inglês naturais:
```
"Olá AIDEN"                          → Saudação e status
"pesquisar inteligência artificial"  → Busca web com armazenamento
"que horas são?"                     → Informações de data/hora
"status do sistema"                  → Diagnósticos do sistema
"como está o tempo?"                 → Conversa geral
"adaptar voz mais grave"             → Adaptação de voz
"falar mais devagar"                 → Ajuste de velocidade
"sair"                               → Desligamento
```

### Comandos de Adaptação de Voz
```
"fale mais devagar"      → Reduz velocidade de fala
"fale mais rápido"       → Aumenta velocidade de fala
"volume mais baixo"      → Reduz volume
"volume mais alto"       → Aumenta volume
"voz mais grave"         → Tom mais grave
"voz mais aguda"         → Tom mais agudo
```

### Comandos do Sistema
```
"status do sistema"     → Relatório abrangente do sistema
"diagnóstico"          → Verificação de saúde
"informação sistema"   → Informações detalhadas do sistema
"listar arquivos"      → Conteúdo do diretório
"memória"              → Uso de memória
"performance"          → Métricas de performance
```

## 🏗 Arquitetura

### Módulos Principais

1. **aiden_main.py**: Interface principal com prioridade de voz e Firebase
2. **aiden_core.py**: Operações centrais do sistema e diagnósticos
3. **firebase_integration.py**: Armazenamento Firebase Realtime Database
4. **voice_recognition.py**: Processamento de fala para texto
5. **text_to_speech.py**: Síntese de fala com aprendizado adaptativo
6. **conversational_ai.py**: Integração Gemini AI aprimorada
7. **web_scraper.py**: Capacidades de pesquisa web melhoradas

### Fluxo de Dados
1. **Entrada de Voz** → Reconhecimento de Fala → Processamento de Texto
2. **Busca Firebase** → Recuperação de contexto anterior
3. **Processamento de Comandos** → Geração de resposta IA/Sistema/Web
4. **Armazenamento Firebase** → Salvar conversa, resultados e perfil de voz
5. **Saída de Áudio** → Síntese de fala com configurações aprendidas

### Coleções Firebase Realtime Database
- `conversations/`: Entradas do usuário e respostas da IA
- `searches/`: Consultas de pesquisa e resultados com rastreamento de origem
- `voice_profiles/`: Perfis de aprendizado de voz por usuário
- Gerenciamento automático de sessões e timestamps

## 🎯 Recursos de Voz

### Reconhecimento de Voz Otimizado
- Ajuste automático de ruído ambiente
- Timeout estendido para conversa natural
- Suporte ao idioma português (Brasil)
- Tratamento gracioso de erros e tentativas

### Saída de Áudio Aprimorada
- TTS offline prioritário para velocidade
- Fallback TTS online para qualidade
- Indicadores de status de áudio
- Otimização de volume e clareza

### Aprendizado de Voz
- **Armazenamento de Preferências**: Salva configurações de voz preferidas
- **Adaptação Gradual**: Melhora com base no feedback do usuário
- **Personalização**: Adapta velocidade, volume e tom
- **Memória Persistente**: Mantém preferências entre sessões

## 🔥 Recursos Firebase

### Pesquisa Inteligente
- Correspondência baseada em palavras-chave de resultados anteriores
- Pontuação de relevância para resultados de pesquisa
- Integração de contexto em novas respostas
- Persistência de memória entre sessões

### Armazenamento de Dados
- Log automático de conversas
- Preservação de resultados de pesquisa
- Perfis de aprendizado de voz
- Interações com timestamp

### Fallbacks Inteligentes
- Armazenamento local quando Firebase indisponível
- Backups em arquivos JSON
- Mecanismos de recuperação de erro
- Capacidade de operação offline

## 🚦 Indicadores de Status

### Mensagens de Inicialização
- `🟢` Recurso online e pronto
- `🔴` Recurso offline ou indisponível
- `🎤` Entrada de voz ativa
- `🔊` Saída de áudio ativa
- `💾` Armazenamento Firebase pronto
- `🎯` Aprendizado de voz ativo

### Indicadores de Runtime
- `🤖 AIDEN:` Respostas da IA
- `🎤` Ouvindo por voz
- `🗣️` Fala reconhecida
- `🔍` Pesquisando (web/database)
- `💾` Dados salvos no Firebase
- `🎙️` Configurações de voz adaptadas

## 🔒 Segurança e Privacidade

### Proteção de Dados
- Regras de segurança Firebase aplicadas
- Proteção de variáveis de ambiente
- Fallback local para operações sensíveis
- Isolamento de sessões

### Segurança de Áudio
- Processamento de fala local
- Nenhum dado de áudio armazenado permanentemente
- Reconhecimento de voz apenas via API Google
- Armazenamento apenas de texto no Firebase

## 📈 Performance

### Requisitos do Sistema
- **Mínimo**: Python 3.7+, 1GB RAM, Conexão com internet
- **Recomendado**: Python 3.9+, 2GB RAM, Microfone, Alto-falantes
- **Ótimo**: Python 3.11+, 4GB RAM, Dispositivos de áudio de qualidade, API Gemini

### Uso de Recursos
- **Modo Voz**: ~200MB RAM
- **Integração Firebase**: +50MB RAM
- **Com IA**: +100MB por conversa
- **Processamento de Áudio**: ~100MB adicional
- **Aprendizado de Voz**: +25MB para perfis

## 🎓 Aprendizado de Voz

### Como Funciona
1. **Coleta Inicial**: AIDEN usa configurações padrão de voz masculina
2. **Feedback do Usuário**: Comandos como "fale mais devagar" são processados
3. **Adaptação**: Configurações são ajustadas baseadas no feedback
4. **Armazenamento**: Preferências são salvas no Firebase/localmente
5. **Melhoria Contínua**: Cada interação refina o perfil de voz

### Dados Armazenados para Aprendizado
- Configurações de velocidade de fala preferidas
- Níveis de volume preferidos
- Preferências de tom/pitch
- Histórico de feedback de voz
- Estatísticas de uso (comprimento de texto, contagem de palavras)

### Banco de Dados Gratuito
O projeto usa Firebase Realtime Database gratuito:
- **Limite**: 1GB de armazenamento
- **Conexões**: 100 simultâneas
- **Suficiente para**: Milhares de conversas e perfis de voz
- **Alternativa Local**: Fallback automático para arquivos JSON

## 🛠 Solução de Problemas

### Problemas Comuns

#### Erro "Failed building wheel for pyaudio"
```bash
# Instale dependências do sistema primeiro
sudo apt-get install portaudio19-dev python3-dev
pip install pyaudio
```

#### Voz não funciona
```bash
# Teste o sistema de áudio
python -c "import pyttsx3; engine = pyttsx3.init(); engine.say('teste'); engine.runAndWait()"

# Verifique dispositivos de áudio
python -c "import pygame; pygame.mixer.init(); print('Audio OK')"
```

#### Firebase não conecta
```bash
# Verifique a conectividade
python -c "import firebase_admin; print('Firebase SDK OK')"

# Use modo offline se necessário
export FIREBASE_OFFLINE=true
```

#### IA não responde
```bash
# Verifique a chave da API
echo $GOOGLE_API_KEY

# Teste a conexão da API
python -c "import google.generativeai as genai; genai.configure(api_key='sua_chave'); print('API OK')"
```

## 🤝 Contribuição

### Diretrizes de Desenvolvimento
1. Manter prioridade de voz em todos os recursos
2. Garantir integração Firebase em novas capacidades
3. Adicionar tratamento abrangente de erros
4. Testar com e sem dispositivos de áudio
5. Seguir padrões de código existentes

### Prioridades de Recursos
1. **Melhoria de Voz**: Melhorar precisão do reconhecimento de fala
2. **Otimização Firebase**: Melhores algoritmos de busca
3. **Integração IA**: Consciência de contexto aprimorada
4. **Aprendizado de Voz**: Algoritmos de adaptação mais sofisticados
5. **Performance**: Otimizar uso de recursos

## 📝 Changelog

### v2.0.0 - Atualização de Aprendizado de Voz
- ✅ Migração de Firestore para Firebase Realtime Database
- ✅ Sistema de voz masculina menos robótica
- ✅ Recursos de aprendizado e adaptação de voz
- ✅ IA aprimorada com suporte a consultas de data/hora
- ✅ Web scraping melhorado
- ✅ Documentação abrangente de configuração
- ✅ Gerenciamento de variáveis de ambiente
- ✅ Fallbacks inteligentes para operação offline

## 📄 Licença

Este projeto fornece um assistente de IA avançado com prioridade de voz, memória persistente e capacidades sofisticadas de interação com aprendizado adaptativo de voz.

---

**"AIDEN - Sua Rede de Melhoria Digital Interativa Avançada está pronta para aprender e se adaptar à sua voz."** 🎤🤖🎯