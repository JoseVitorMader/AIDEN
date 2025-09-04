#!/bin/bash

# AIDEN Setup Script
# Este script configura automaticamente o AIDEN com todas as dependências necessárias

echo "🤖 AIDEN - Setup e Configuração Automática"
echo "=========================================="
echo ""

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Função para instalar dependências do sistema
install_system_deps() {
    echo "📦 Instalando dependências do sistema..."
    
    if command_exists apt-get; then
        sudo apt-get update
        sudo apt-get install -y portaudio19-dev python3-dev python3-pip
        sudo apt-get install -y espeak espeak-data libespeak1 libespeak-dev
        echo "✅ Dependências do sistema instaladas (apt-get)"
    elif command_exists yum; then
        sudo yum install -y portaudio-devel python3-devel python3-pip
        sudo yum install -y espeak espeak-devel
        echo "✅ Dependências do sistema instaladas (yum)"
    elif command_exists brew; then
        brew install portaudio
        brew install espeak
        echo "✅ Dependências do sistema instaladas (brew)"
    else
        echo "⚠️ Gerenciador de pacotes não detectado. Instale manualmente:"
        echo "   - portaudio19-dev"
        echo "   - python3-dev"
        echo "   - espeak"
    fi
}

# Função para instalar dependências Python
install_python_deps() {
    echo "🐍 Instalando dependências Python..."
    
    # Tentar instalar PyAudio primeiro (pode falhar sem dependências do sistema)
    if pip install pyaudio; then
        echo "✅ PyAudio instalado com sucesso"
    else
        echo "⚠️ PyAudio falhou - pode funcionar sem reconhecimento de voz"
    fi
    
    # Instalar outras dependências
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo "✅ Dependências Python instaladas"
    else
        echo "❌ Erro ao instalar dependências Python"
        exit 1
    fi
}

# Função para configurar arquivo de ambiente
setup_environment() {
    echo "⚙️ Configurando arquivo de ambiente..."
    
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "📝 Arquivo .env criado a partir de .env.example"
        echo ""
        echo "⚠️ IMPORTANTE: Edite o arquivo .env para adicionar suas chaves de API:"
        echo "   - GOOGLE_API_KEY: Obtenha em https://makersuite.google.com/app/apikey"
        echo "   - AIDEN_USER_NAME: Seu nome"
        echo ""
        echo "📝 Para editar: nano .env"
    else
        echo "✅ Arquivo .env já existe"
    fi
}

# Função para testar a instalação
test_installation() {
    echo "🧪 Testando instalação..."
    
    # Teste básico de importação
    if python3 -c "import aiden_main; print('✅ AIDEN importado com sucesso')"; then
        echo "✅ Teste básico passou"
    else
        echo "❌ Teste básico falhou"
        return 1
    fi
    
    # Teste de voz (pode falhar sem PyAudio)
    if python3 -c "from text_to_speech import get_voice_settings; print('✅ Sistema de voz funcionando')"; then
        echo "✅ Sistema de voz OK"
    else
        echo "⚠️ Sistema de voz com problemas (normal sem PyAudio)"
    fi
    
    # Teste Firebase
    if python3 -c "from firebase_integration import get_firebase_manager; print('✅ Firebase integration OK')"; then
        echo "✅ Integração Firebase OK"
    else
        echo "❌ Problema com Firebase"
    fi
    
    echo ""
    echo "🎉 Instalação concluída!"
}

# Função para mostrar instruções de uso
show_usage() {
    echo ""
    echo "🚀 Como usar o AIDEN:"
    echo "===================="
    echo ""
    echo "1. Configure suas chaves de API no arquivo .env:"
    echo "   nano .env"
    echo ""
    echo "2. Execute o AIDEN:"
    echo "   python3 aiden_main.py"
    echo ""
    echo "3. Comandos de voz úteis:"
    echo "   - 'Olá AIDEN' - Saudação"
    echo "   - 'que horas são?' - Data e hora"
    echo "   - 'pesquisar [tema]' - Pesquisa web"
    echo "   - 'fale mais devagar' - Ajustar voz"
    echo "   - 'status do sistema' - Diagnósticos"
    echo "   - 'sair' - Encerrar"
    echo ""
    echo "📚 Documentação completa: README_IMPROVED.md"
    echo ""
}

# Execução principal
main() {
    echo "Iniciando configuração do AIDEN..."
    echo ""
    
    # Verificar Python
    if ! command_exists python3; then
        echo "❌ Python 3 não encontrado. Instale Python 3.7+ primeiro."
        exit 1
    fi
    
    echo "✅ Python 3 encontrado: $(python3 --version)"
    echo ""
    
    # Pedir confirmação para instalar dependências do sistema
    read -p "Instalar dependências do sistema? (s/N): " install_sys
    if [[ $install_sys =~ ^[Ss]$ ]]; then
        install_system_deps
        echo ""
    fi
    
    # Instalar dependências Python
    install_python_deps
    echo ""
    
    # Configurar ambiente
    setup_environment
    echo ""
    
    # Testar instalação
    test_installation
    echo ""
    
    # Mostrar instruções
    show_usage
}

# Verificar se script está sendo executado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi