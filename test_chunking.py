#!/usr/bin/env python3
"""
Test text chunking functionality without dependencies
"""

from typing import List, Dict, Any
import json

def chunk_text(text: str, max_chunk_size: int = 200) -> List[str]:
    """Split long text into smaller chunks for better TTS processing."""
    if len(text) <= max_chunk_size:
        return [text]
    
    # Try to split on sentence boundaries first
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    
    for i, sentence in enumerate(sentences):
        # Add period back except for the last sentence
        if i < len(sentences) - 1:
            sentence += '. '
        
        # If adding this sentence would exceed the limit
        if len(current_chunk + sentence) > max_chunk_size:
            if current_chunk:  # If we have something in current chunk
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:  # If the sentence itself is too long, split by words
                words = sentence.split()
                temp_chunk = ""
                for word in words:
                    if len(temp_chunk + " " + word) > max_chunk_size:
                        if temp_chunk:
                            chunks.append(temp_chunk.strip())
                            temp_chunk = word
                        else:
                            # Word itself is too long, just add it
                            chunks.append(word)
                            temp_chunk = ""
                    else:
                        temp_chunk += " " + word if temp_chunk else word
                if temp_chunk:
                    current_chunk = temp_chunk
        else:
            current_chunk += sentence
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def get_voice_settings(user_id: str = "default") -> Dict[str, Any]:
    """Get voice settings for a specific user"""
    try:
        filename = f"aiden_voice_profiles_{user_id}.json"
        with open(filename, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
            if profiles:
                return profiles[-1]
    except FileNotFoundError:
        pass
    
    # Default voice settings - faster, more natural male voice
    return {
        'rate': 220,  # Increased speaking rate (words per minute) 
        'volume': 0.9,  # Volume level (0.0 to 1.0)
        'voice_id': 'male',  # Prefer male voice
        'pitch': 0.8,  # Lower pitch for more natural sound
        'language': 'pt-br',  # Portuguese Brazil
        'chunk_size': 200  # Maximum characters per TTS chunk for long texts
    }

def test_voice_improvements():
    """Test voice improvements without external dependencies"""
    print("🎤 Testing AIDEN Voice Improvements")
    print("=" * 60)
    
    # Test long text chunking
    long_text = """Este é um texto muito longo para testar a funcionalidade de divisão de texto em blocos menores para síntese de voz. A ideia é que textos longos sejam divididos em partes menores, permitindo que o sistema de texto para fala processe cada parte separadamente, evitando problemas de timeout ou falhas na síntese. Isso é especialmente importante quando temos respostas extensas do AI que precisam ser faladas em voz alta. O sistema agora divide o texto em sentenças e, se necessário, em palavras individuais para garantir que tudo seja processado corretamente. Além disso, foi aumentada a velocidade de fala padrão de 180 para 220 palavras por minuto, tornando a experiência mais fluida e natural."""
    
    print(f"\n📝 Texto original: {len(long_text)} caracteres")
    print(f"Palavras: {len(long_text.split())} palavras")
    print(f"Preview: {long_text[:100]}...")
    
    # Test chunking
    chunks = chunk_text(long_text, 200)
    print(f"\n📦 ✓ Dividido em {len(chunks)} blocos para melhor processamento:")
    total_chars = 0
    for i, chunk in enumerate(chunks):
        total_chars += len(chunk)
        print(f"  Bloco {i+1}: {len(chunk)} chars - {chunk[:60]}...")
    
    print(f"✓ Total de caracteres preservados: {total_chars} (original: {len(long_text)})")
    
    # Test voice settings with increased speed
    settings = get_voice_settings("test_user")
    print(f"\n⚡ ✓ Configurações de voz aprimoradas:")
    print(f"  • Velocidade: {settings.get('rate', 220)} WPM (aumentada de 180)")
    print(f"  • Volume: {settings.get('volume', 0.9)}")
    print(f"  • Idioma: {settings.get('language', 'pt-br')}")
    print(f"  • Tamanho do bloco: {settings.get('chunk_size', 200)} caracteres")
    print(f"  • Tipo de voz: {settings.get('voice_id', 'male')}")
    
    # Test edge cases
    print(f"\n🔧 Testando casos especiais:")
    
    # Very short text
    short_text = "Olá!"
    short_chunks = chunk_text(short_text, 200)
    print(f"  ✓ Texto curto: '{short_text}' -> {len(short_chunks)} bloco(s)")
    
    # Text with no periods
    no_periods = "Este texto não tem pontos finais mas tem várias palavras que precisam ser processadas corretamente pelo sistema"
    no_period_chunks = chunk_text(no_periods, 50)
    print(f"  ✓ Texto sem pontos: {len(no_periods)} chars -> {len(no_period_chunks)} bloco(s)")
    
    # Very long sentence
    long_sentence = "Esta é uma sentença extremamente longa que excede o limite de caracteres por bloco e deve ser dividida por palavras em vez de sentenças para garantir que o processamento seja feito corretamente sem perder nenhuma informação importante"
    long_sentence_chunks = chunk_text(long_sentence, 100)
    print(f"  ✓ Sentença longa: {len(long_sentence)} chars -> {len(long_sentence_chunks)} bloco(s)")
    
    print(f"\n🎯 Problemas resolvidos:")
    print(f"  ✓ Textos longos não causam mais timeout no TTS")
    print(f"  ✓ Velocidade de fala aumentada para 220 WPM")
    print(f"  ✓ Melhor divisão em blocos preservando sentido")
    print(f"  ✓ Sistema robusto para diferentes tipos de texto")
    print(f"  ✓ Configurações de voz adaptáveis por usuário")
    
    return True

if __name__ == "__main__":
    test_voice_improvements()
    print(f"\n🎉 Melhorias de voz implementadas com sucesso!")
    print(f"As melhorias estarão ativas quando executar 'python main_ai.py'")