# AIDEN - Advanced Interactive Digital Enhancement Network

**Voice-First AI Assistant with Firebase Integration**

AIDEN is a sophisticated AI assistant that prioritizes voice interaction and includes Firebase integration for persistent data storage and search capabilities.

## 🚀 Key Features

### Voice-First Interface
- **Priority Voice Input**: Voice recognition is the primary input method
- **Enhanced Audio Output**: Text-to-speech with offline and online modes
- **Optimized Recognition**: Tuned for natural conversation flow
- **Graceful Fallbacks**: Text mode when voice is unavailable

### Firebase Integration
- **Conversation Storage**: All interactions saved to Firebase
- **Search History**: Research results preserved for future reference
- **Context-Aware Responses**: Previous conversations inform new responses
- **Persistent Memory**: Information persists across sessions

### Advanced Capabilities
- **System Monitoring**: Real-time diagnostics and performance analysis
- **Intelligent Conversations**: Powered by Google Gemini AI
- **Web Research**: Integrated search with result storage
- **File Management**: Directory operations and system control
- **Contextual Memory**: Remembers and references previous interactions

## 🛠 Installation & Setup

### System Requirements
```bash
# Install system dependencies (Linux)
sudo apt-get update
sudo apt-get install portaudio19-dev python3-dev
```

### Python Dependencies
```bash
pip install -r requirements.txt
```

### Required Packages
- `google-generativeai` - For advanced AI conversations
- `SpeechRecognition` - For voice input
- `pyttsx3` - For offline text-to-speech
- `gTTS` - For online text-to-speech
- `pygame` - For audio playback
- `firebase-admin` - For Firebase integration
- `requests` - For web operations
- `beautifulsoup4` - For web scraping

### Configuration

#### Environment Variables
```bash
# AI Configuration
export GOOGLE_API_KEY="your_gemini_api_key"        # For advanced AI features
export AIDEN_USER_NAME="Your Name"                 # How AIDEN addresses you
export AIDEN_MODE="true"                          # Enable enhanced mode

# Firebase is auto-configured with provided credentials
```

#### Firebase Setup
Firebase integration is pre-configured with the provided credentials:
- Project: `aiden-dd627`
- Auto-configured for conversation and search storage
- No additional setup required for basic functionality

## 🎮 Usage

### Quick Start (Voice-First Mode)
```bash
python aiden_main.py
```

### Alternative Interface
```bash
python main_ai.py
```

### Voice Commands
AIDEN responds to natural Portuguese and English:
```
"Olá AIDEN"              → Greeting and status
"pesquisar inteligência artificial" → Web search with storage
"status do sistema"      → System diagnostics
"como está o tempo?"     → General conversation
"sair"                   → Shutdown
```

### System Commands
```
"status do sistema"      → Comprehensive system report
"diagnóstico"           → Health check
"informação sistema"    → Detailed system information
"listar arquivos"       → Directory contents
"memória"               → Memory usage
"performance"           → Performance metrics
```

## 🏗 Architecture

### Core Modules

1. **aiden_main.py**: Main voice-first interface with Firebase integration
2. **aiden_core.py**: Core system operations and diagnostics
3. **firebase_integration.py**: Firebase storage and search functionality
4. **voice_recognition.py**: Speech-to-text processing
5. **text_to_speech.py**: Text-to-speech synthesis
6. **conversational_ai.py**: Gemini AI integration
7. **web_scraper.py**: Web research capabilities

### Data Flow
1. **Voice Input** → Speech Recognition → Text Processing
2. **Firebase Search** → Previous context retrieval
3. **Command Processing** → AI/System/Web response generation
4. **Firebase Storage** → Save conversation and results
5. **Audio Output** → Text-to-speech synthesis

### Firebase Collections
- `conversations`: User inputs and AI responses
- `searches`: Search queries and results with source tracking
- Automatic session management and timestamping

## 🎯 Voice Features

### Optimized Voice Recognition
- Automatic ambient noise adjustment
- Extended timeout for natural conversation
- Portuguese (Brazil) language support
- Graceful error handling and retries

### Enhanced Audio Output
- Priority offline TTS for speed
- Online TTS fallback for quality
- Audio status indicators
- Volume and clarity optimization

### Conversation Flow
- Natural pause detection
- Context awareness across interactions
- Voice-first, text-available design
- Seamless mode switching

## 🔥 Firebase Features

### Intelligent Search
- Keyword-based previous result matching
- Relevance scoring for search results
- Context integration in new responses
- Cross-session memory persistence

### Data Storage
- Automatic conversation logging
- Search result preservation
- Session management
- Timestamped interactions

### Graceful Fallbacks
- Local storage when Firebase unavailable
- JSON file backups
- Error recovery mechanisms
- Offline operation capability

## 🚦 Status Indicators

### Startup Messages
- `🟢` Feature online and ready
- `🔴` Feature offline or unavailable
- `🎤` Voice input active
- `🔊` Audio output active
- `💾` Firebase storage ready

### Runtime Indicators
- `🤖 AIDEN:` AI responses
- `🎤` Listening for voice
- `🗣️` Speech recognized
- `🔍` Searching (web/database)
- `💾` Data saved to Firebase

## 🔒 Security & Privacy

### Data Protection
- Firebase security rules applied
- Environment variable protection
- Local fallback for sensitive operations
- Session isolation

### Audio Security
- Local speech processing
- No audio data stored permanently
- Voice recognition via Google API only
- Text-only storage in Firebase

## 📈 Performance

### System Requirements
- **Minimum**: Python 3.7+, 1GB RAM, Internet connection
- **Recommended**: Python 3.9+, 2GB RAM, Microphone, Speakers
- **Optimal**: Python 3.11+, 4GB RAM, Quality audio devices, Gemini API

### Resource Usage
- **Voice Mode**: ~200MB RAM
- **Firebase Integration**: +50MB RAM
- **With AI**: +100MB per conversation
- **Audio Processing**: ~100MB additional

## 🤝 Contributing

### Development Guidelines
1. Maintain voice-first priority in all features
2. Ensure Firebase integration in new capabilities
3. Add comprehensive error handling
4. Test with and without audio devices
5. Follow existing code patterns

### Feature Priorities
1. **Voice Enhancement**: Improve speech recognition accuracy
2. **Firebase Optimization**: Better search algorithms
3. **AI Integration**: Enhanced context awareness
4. **System Integration**: More system control features
5. **Performance**: Optimize resource usage

## 📝 License

This project provides an advanced voice-first AI assistant with persistent memory and sophisticated interaction capabilities.

---

**"AIDEN - Your Advanced Interactive Digital Enhancement Network is ready to assist."** 🎤🤖