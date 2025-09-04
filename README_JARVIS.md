# AIDEN/JARVIS - Just A Rather Very Intelligent System

**Enhanced AI Assistant System inspired by Iron Man's JARVIS**

AIDEN has been transformed into a sophisticated AI assistant that combines the original functionality with JARVIS-like capabilities, providing professional, intelligent assistance with advanced system monitoring and control features.

## 🚀 New JARVIS Features

### Core Enhancements
- **JARVIS Personality**: Professional, respectful, and intelligent responses
- **Enhanced Interface**: Formal communication style with "Sir" addressing  
- **System Diagnostics**: Comprehensive system monitoring and analysis
- **Advanced Error Handling**: Graceful fallbacks for missing dependencies
- **Dual Mode Operation**: Can run as original Manus or enhanced JARVIS

### Advanced Capabilities
- **System Monitoring**: Real-time diagnostics, memory usage, disk space, process monitoring
- **File Management**: Directory listing, size analysis, file operations
- **Performance Analysis**: CPU load, memory usage, system performance metrics
- **Time Management**: Current time, date, scheduling information, runtime tracking
- **Process Management**: Running processes analysis and monitoring
- **Intelligent Fallbacks**: Smart responses when advanced AI is unavailable

## 🎯 JARVIS vs Original Comparison

| Feature | Original Manus | Enhanced JARVIS |
|---------|----------------|-----------------|
| Personality | Casual, friendly | Professional, formal |
| Addressing | Generic | "Sir" or custom name |
| System Control | Basic | Advanced diagnostics |
| Error Handling | Basic | Comprehensive fallbacks |
| Interface | Simple | Sophisticated with emojis |
| Capabilities | Voice + AI | Voice + AI + System Management |

## 🛠 Installation & Setup

### Basic Requirements
```bash
# Core Python packages (already included)
- os, sys, json, datetime, subprocess, platform
```

### Enhanced Features (Optional)
```bash
pip install google-generativeai      # For advanced AI
pip install SpeechRecognition       # For voice input  
pip install pyttsx3                 # For text-to-speech
pip install gTTS                    # For online TTS
pip install beautifulsoup4          # For web research
pip install requests                # For web operations
pip install python-dotenv           # For environment variables
```

### Audio Dependencies (Linux)
```bash
sudo apt-get install portaudio19-dev  # For voice recognition
pip install pyaudio                   # Audio processing
```

## 🎮 Usage

### Quick Start (JARVIS Mode)
```bash
python main_ai.py
```

### Quick Start (Original Mode)  
```bash
export JARVIS_MODE=false
python main_ai.py
```

### Standalone JARVIS
```bash
python jarvis_main.py
```

### Configuration Options
```bash
# Environment Variables
export JARVIS_MODE=true              # Enable JARVIS mode (default)
export JARVIS_USER_NAME="Sir"        # How JARVIS addresses you
export GOOGLE_API_KEY="your_key"     # For advanced AI features
export GEMINI_API_KEY="your_key"     # Alternative API key name
```

## 🎯 Command Examples

### System Monitoring
```
"status do sistema"     → Comprehensive diagnostics
"diagnóstico"          → System health check  
"performance"          → Performance analysis
"informação sistema"   → Detailed system info
```

### File Management
```
"listar arquivos"      → Directory contents
"tamanho diretório"    → Directory size analysis
```

### Time & Scheduling
```
"tempo"               → Current time and date
"data"                → Date information
```

### Process Management
```
"listar processos"    → Running processes
"processo"            → Process information
```

### General Commands
```
"ajuda"               → Help system
"pesquisar [topic]"   → Web research
"sair"                → Shutdown JARVIS
```

## 🏗 Architecture

### Core Modules

1. **jarvis_core.py**: Core JARVIS functionality and system operations
2. **jarvis_main.py**: Standalone JARVIS with full capabilities
3. **main_ai.py**: Enhanced original with JARVIS integration
4. **conversational_ai.py**: Gemini AI integration
5. **voice_recognition.py**: Speech-to-text processing
6. **text_to_speech.py**: Text-to-speech synthesis
7. **web_scraper.py**: Web research capabilities

### Dependency Management
The system gracefully handles missing dependencies:
- **No audio libraries**: Falls back to text-only mode
- **No AI API**: Uses intelligent fallback responses  
- **No web scraping**: Provides alternative suggestions
- **No TTS**: Text-only output mode

## 🎨 JARVIS Personality Features

### Communication Style
- Professional and respectful tone
- Addresses user as "Sir" or custom name
- Technical precision with helpful explanations
- Formal language with sophisticated vocabulary

### Response Examples
```
Original: "Encontrei isto: [result]"
JARVIS:   "Research complete, Sir. [detailed analysis]"

Original: "Não consegui processar"  
JARVIS:   "I apologize, Sir, but I'm experiencing difficulties with my advanced processing systems."

Original: "Como posso ajudar?"
JARVIS:   "How may I assist you today, Sir?"
```

## 🔧 Development

### Running Tests
```bash
python test_integration.py          # Integration tests
python jarvis_core.py               # Core functionality test
python -c "import main_ai; print('✓ Main module loads')"
```

### Adding New Features
1. **System Commands**: Add to `jarvis_core.py`
2. **AI Responses**: Enhance prompts in `main_ai.py`  
3. **Web Features**: Extend `web_scraper.py`
4. **Voice Features**: Modify `voice_recognition.py`

## 🚦 Status Indicators

### Startup Messages
- `[INFO]` - System information
- `[WARNING]` - Non-critical issues
- `[ERROR]` - Critical problems
- `🟢` - Feature online
- `🔴` - Feature offline

### Runtime Indicators  
- `🤖 JARVIS:` - JARVIS responses
- `🎤` - Listening for voice
- `📊` - System analysis
- `🔍` - Web research
- `⚙️` - Process management

## 🔒 Security Features

- No automatic system power commands
- Safe web scraping with error handling
- Environment variable protection
- Process isolation for external commands
- Input validation and sanitization

## 📈 Performance

### System Requirements
- **Minimum**: Python 3.7+, 512MB RAM
- **Recommended**: Python 3.9+, 2GB RAM, Audio device
- **Optimal**: Python 3.11+, 4GB RAM, Fast internet, Gemini API

### Resource Usage
- **Text Mode**: ~50MB RAM
- **Voice Mode**: ~150MB RAM  
- **Full JARVIS**: ~200MB RAM
- **With AI**: +100MB per conversation

## 🤝 Contributing

### Development Guidelines
1. Maintain JARVIS personality consistency
2. Ensure graceful dependency fallbacks
3. Add comprehensive error handling
4. Follow existing code patterns
5. Test with and without dependencies

### Feature Priorities
1. **Core Stability**: Ensure basic features always work
2. **JARVIS Enhancement**: Improve personality and capabilities
3. **System Integration**: Add more system control features
4. **AI Enhancement**: Better conversational capabilities
5. **Performance**: Optimize resource usage

## 📝 License

This project enhances the original AIDEN with JARVIS-inspired capabilities while maintaining compatibility and adding sophisticated AI assistant features.

---

**"Just A Rather Very Intelligent System at your service, Sir."** 🤖