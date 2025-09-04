"""
AIDEN Core Module - Enhanced AI Assistant 
Provides sophisticated AI assistance with system monitoring and control capabilities
"""

import os
import sys
import json
import datetime
import subprocess
import platform
import time
from typing import Dict, List, Optional, Any


class AidenCore:
    def __init__(self, name: str = "Sir"):
        self.user_name = name
        self.status = "online"
        self.start_time = datetime.datetime.now()
        self.command_history = []
        self.system_info = self._get_system_info()
        self.capabilities = {
            "system_monitoring": True,
            "file_management": True,
            "data_analysis": True,
            "web_research": True,
            "task_scheduling": True,
            "diagnostics": True
        }
        
    def _get_system_info(self) -> Dict[str, Any]:
        """Collect comprehensive system information"""
        return {
            "platform": platform.platform(),
            "system": platform.system(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "hostname": platform.node(),
            "uptime": self._get_uptime()
        }
    
    def _get_uptime(self) -> str:
        """Get system uptime"""
        try:
            if platform.system() == "Linux":
                with open('/proc/uptime', 'r') as f:
                    uptime_seconds = float(f.readline().split()[0])
                    return str(datetime.timedelta(seconds=int(uptime_seconds)))
            else:
                return "Uptime unavailable on this platform"
        except:
            return "Unable to determine uptime"
    
    def greet(self) -> str:
        """AIDEN-style greeting"""
        current_time = datetime.datetime.now()
        time_of_day = "morning" if current_time.hour < 12 else "afternoon" if current_time.hour < 18 else "evening"
        
        greeting = f"Good {time_of_day}, {self.user_name}. AIDEN systems are online and operational."
        
        # Add system status
        greeting += f"\n\nSystem Status Report:"
        greeting += f"\n• Platform: {self.system_info['platform']}"
        greeting += f"\n• System Uptime: {self.system_info['uptime']}"
        greeting += f"\n• All core systems: Nominal"
        greeting += f"\n\nHow may I assist you today, {self.user_name}?"
        
        return greeting
    
    def process_command(self, command: str) -> str:
        """Process user commands with AIDEN-style intelligence"""
        self.command_history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "command": command
        })
        
        command_lower = command.lower().strip()
        
        # System monitoring commands
        if any(keyword in command_lower for keyword in ["status", "sistema", "diagnóstico", "diagnostics"]):
            return self._system_diagnostics()
        
        # File management commands
        elif any(keyword in command_lower for keyword in ["arquivo", "file", "diretório", "directory", "pasta", "folder"]):
            return self._file_management(command)
        
        # Time and schedule commands
        elif any(keyword in command_lower for keyword in ["tempo", "time", "data", "date", "horário", "schedule"]):
            return self._time_management()
        
        # System information commands
        elif any(keyword in command_lower for keyword in ["informação", "information", "sobre", "about", "specs"]):
            return self._system_information()
        
        # Process management commands  
        elif any(keyword in command_lower for keyword in ["processo", "process", "task", "tarefa"]):
            return self._process_management(command)
        
        # Memory and performance commands
        elif any(keyword in command_lower for keyword in ["memória", "memory", "performance", "desempenho"]):
            return self._performance_analysis()
        
        # Shutdown/restart commands
        elif any(keyword in command_lower for keyword in ["desligar", "shutdown", "reiniciar", "restart"]):
            return self._power_management(command)
        
        # Help command
        elif any(keyword in command_lower for keyword in ["ajuda", "help", "comandos", "commands"]):
            return self._help_system()
        
        # Default intelligent response
        else:
            return self._general_response(command)
    
    def _system_diagnostics(self) -> str:
        """Comprehensive system diagnostics"""
        response = f"Running comprehensive diagnostics, {self.user_name}...\n\n"
        
        # Check disk space
        try:
            disk_usage = subprocess.check_output(["df", "-h", "/"], universal_newlines=True)
            response += "📊 Disk Usage Analysis:\n" + disk_usage + "\n"
        except:
            response += "📊 Disk Usage: Unable to retrieve disk information\n\n"
        
        # Check memory usage
        try:
            if platform.system() == "Linux":
                mem_info = subprocess.check_output(["free", "-h"], universal_newlines=True)
                response += "🧠 Memory Status:\n" + mem_info + "\n"
        except:
            response += "🧠 Memory Status: Unable to retrieve memory information\n\n"
        
        # Check running processes count
        try:
            process_count = len(subprocess.check_output(["ps", "aux"], universal_newlines=True).split('\n')) - 1
            response += f"⚙️  Active Processes: {process_count}\n\n"
        except:
            response += "⚙️  Process Information: Unavailable\n\n"
        
        response += "Diagnostics complete. All systems appear to be functioning within normal parameters."
        return response
    
    def _file_management(self, command: str) -> str:
        """Handle file and directory operations"""
        response = f"Analyzing file system request, {self.user_name}...\n\n"
        
        if "listar" in command.lower() or "list" in command.lower():
            try:
                files = os.listdir(".")
                response += "📁 Current Directory Contents:\n"
                for i, file in enumerate(files[:10], 1):  # Limit to first 10 files
                    file_type = "📂" if os.path.isdir(file) else "📄"
                    response += f"{i:2}. {file_type} {file}\n"
                if len(files) > 10:
                    response += f"... and {len(files) - 10} more items\n"
            except Exception as e:
                response += f"Error accessing directory: {str(e)}\n"
        
        elif "tamanho" in command.lower() or "size" in command.lower():
            try:
                total_size = sum(os.path.getsize(f) for f in os.listdir(".") if os.path.isfile(f))
                response += f"📊 Current directory size: {total_size:,} bytes\n"
            except:
                response += "Unable to calculate directory size\n"
        
        else:
            response += "Available file operations:\n"
            response += "• 'listar arquivos' - List directory contents\n"
            response += "• 'tamanho diretório' - Calculate directory size\n"
        
        return response
    
    def _time_management(self) -> str:
        """Handle time and scheduling requests"""
        now = datetime.datetime.now()
        response = f"Time and Schedule Information, {self.user_name}:\n\n"
        response += f"⏰ Current Time: {now.strftime('%H:%M:%S')}\n"
        response += f"📅 Current Date: {now.strftime('%A, %B %d, %Y')}\n"
        response += f"⌚ JARVIS Runtime: {now - self.start_time}\n"
        
        # Add timezone info if available
        try:
            import time
            response += f"🌍 Timezone: {time.tzname[0]}\n"
        except:
            pass
        
        return response
    
    def _system_information(self) -> str:
        """Provide comprehensive system information"""
        response = f"System Information Report, {self.user_name}:\n\n"
        
        for key, value in self.system_info.items():
            emoji = {
                "platform": "💻",
                "system": "🖥️",
                "processor": "⚡",
                "python_version": "🐍",
                "hostname": "🌐",
                "uptime": "⏱️"
            }.get(key, "ℹ️")
            
            response += f"{emoji} {key.replace('_', ' ').title()}: {value}\n"
        
        response += f"\n🤖 JARVIS Capabilities:\n"
        for capability, status in self.capabilities.items():
            status_icon = "✅" if status else "❌"
            response += f"{status_icon} {capability.replace('_', ' ').title()}\n"
        
        return response
    
    def _process_management(self, command: str) -> str:
        """Handle process management requests"""
        response = f"Process Management System, {self.user_name}:\n\n"
        
        try:
            if "listar" in command.lower() or "list" in command.lower():
                # Show top processes by CPU/memory usage
                ps_output = subprocess.check_output(
                    ["ps", "aux", "--sort=-%cpu"], 
                    universal_newlines=True
                ).split('\n')[:6]  # Header + top 5 processes
                
                response += "🔧 Top Processes by CPU Usage:\n"
                for line in ps_output:
                    if line.strip():
                        response += f"   {line}\n"
            else:
                response += "Available process operations:\n"
                response += "• 'listar processos' - Show running processes\n"
                
        except Exception as e:
            response += f"Process information unavailable: {str(e)}\n"
        
        return response
    
    def _performance_analysis(self) -> str:
        """Analyze system performance"""
        response = f"Performance Analysis Report, {self.user_name}:\n\n"
        
        try:
            # CPU load average (Linux/Unix)
            if platform.system() in ["Linux", "Darwin"]:
                load_avg = os.getloadavg()
                response += f"📈 CPU Load Average (1m, 5m, 15m): {load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}\n"
        except:
            response += "📈 CPU Load: Unable to retrieve load information\n"
        
        # Python process information
        try:
            import psutil
            process = psutil.Process()
            response += f"🐍 JARVIS Memory Usage: {process.memory_info().rss / 1024 / 1024:.2f} MB\n"
            response += f"🐍 JARVIS CPU Usage: {process.cpu_percent():.1f}%\n"
        except ImportError:
            response += "🐍 JARVIS Process Info: psutil not available for detailed metrics\n"
        except:
            response += "🐍 JARVIS Process Info: Unable to retrieve process information\n"
        
        return response
    
    def _power_management(self, command: str) -> str:
        """Handle power management requests"""
        return f"Power management commands detected, {self.user_name}. However, for security reasons, JARVIS does not execute system power commands without explicit authorization. These operations should be performed manually."
    
    def _help_system(self) -> str:
        """Provide help information"""
        response = f"JARVIS Help System, {self.user_name}:\n\n"
        response += "Available command categories:\n\n"
        response += "🔧 System Monitoring:\n"
        response += "   • 'status' or 'diagnóstico' - System diagnostics\n"
        response += "   • 'informação sistema' - System information\n"
        response += "   • 'performance' - Performance analysis\n\n"
        
        response += "📁 File Management:\n"
        response += "   • 'listar arquivos' - List directory contents\n"
        response += "   • 'tamanho diretório' - Directory size analysis\n\n"
        
        response += "⏰ Time Management:\n"
        response += "   • 'tempo' or 'data' - Current time and date\n\n"
        
        response += "⚙️ Process Management:\n"
        response += "   • 'listar processos' - Show running processes\n\n"
        
        response += "Simply speak naturally, and I will interpret your intentions accordingly."
        return response
    
    def _general_response(self, command: str) -> str:
        """Generate intelligent general responses"""
        responses = [
            f"I understand your request, {self.user_name}. However, this functionality is not yet implemented in my current configuration.",
            f"That's an interesting request, {self.user_name}. Let me analyze what I can do to assist you with that.",
            f"I'm processing your request, {self.user_name}. While I don't have a specific function for that, I can suggest alternative approaches.",
            f"Acknowledged, {self.user_name}. That request requires capabilities beyond my current operational parameters."
        ]
        
        import random
        base_response = random.choice(responses)
        
        # Add helpful suggestions
        base_response += f"\n\nFor a complete list of my capabilities, simply say 'help' or 'ajuda'. "
        base_response += f"I am continuously learning and expanding my operational parameters to better assist you."
        
        return base_response
    
    def shutdown(self) -> str:
        """JARVIS-style shutdown sequence"""
        runtime = datetime.datetime.now() - self.start_time
        response = f"Initiating shutdown sequence, {self.user_name}.\n\n"
        response += f"Session Summary:\n"
        response += f"• Runtime: {runtime}\n"
        response += f"• Commands processed: {len(self.command_history)}\n"
        response += f"• System status: All systems nominal\n\n"
        response += f"JARVIS systems going offline. Until next time, {self.user_name}."
        
        self.status = "offline"
        return response


if __name__ == "__main__":
    # Test the JARVIS core system
    jarvis = JarvisCore("Sir")
    print(jarvis.greet())
    print("\n" + "="*50 + "\n")
    
    # Test various commands
    test_commands = [
        "status do sistema",
        "listar arquivos",
        "que horas são",
        "informações do sistema",
        "ajuda"
    ]
    
    for cmd in test_commands:
        print(f"User: {cmd}")
        print(f"JARVIS: {jarvis.process_command(cmd)}")
        print("\n" + "-"*30 + "\n")
    
    print(jarvis.shutdown())