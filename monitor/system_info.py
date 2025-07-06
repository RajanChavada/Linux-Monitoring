"""
    This module provides monitoring capabilites: 
    - CPU usage
    - RAM usage 
    - Disk usage
    - System Uptime

"""

import psutil
import platform
import time 
import subprocess
from datetime import timedelta


class SystemInfo:
    def __init__(self):
        # Initialize the SystemInfo class
        pass

    def get_cpu_usage(self) -> dict:
        """Returns the CPU usage as a percentage."""
        return { 
            "cpu_percent": psutil.cpu_percent(interval=1),
            "cpu_count": psutil.cpu_count(logical=True),
            "cpu_freq": self._to_dict(psutil.cpu_freq())
        }
    
    def get_memory_info(self) -> dict: 
        """ Returns the total/avaialb/used memory as a percentage"""
        mem = psutil.virtual_memory()
        return { 
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "percent": mem.percent
        }
    
    def get_disk_info(self) -> dict:
        """ returns the dick information (usage, total, used, free, percentage)"""
        # path is the home 
        disk = psutil.disk_usage('/')  
        return { 
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }
    
    def get_system_info(self) -> dict:
        """ Get more system information """
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "uptime": str(timedelta(seconds=time.time() - psutil.boot_time()))
        }

    def get_hardware_info(self):
        if platform.system() == "Darwin":
            return {
                "cpu": self._run_command("sysctl -n machdep.cpu.brand_string"),
                "memory": self._run_command("sysctl hw.memsize"),
                "system_profiler": self._run_command("system_profiler SPHardwareDataType")
            }
        else: 
            return {
                "lscpu": self._run_command("lscpu"),
                "lshw": self._run_command("lshw -short", sudo=True),
                "dmidecode": self._run_command("dmidecode -t system", sudo=True)
            }

    def get_gpu_info(self):
        if platform.system() == "Darwin":
            return {
                "gpu_details": self._run_command("system_profiler SPDisplaysDataType")
            }
        else:
            return {
                "gpu_details": self._run_command("lspci | grep -i 'vga\\|3d\\|display'")
            }
    
    def collect_all(self) -> dict:
        """Returns the cpu memory disk and system information"""
        return {
            "cpu": self.get_cpu_usage(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "system": self.get_system_info(),
            "hardware": self.get_hardware_info(),
            "gpu": self.get_gpu_info()
        }

    def _to_dict(self, named_tuple):
        return named_tuple._asdict() if hasattr(named_tuple, '_asdict') else {}

    def _run_command(self, command, sudo=False, safe=False):
        try:
            if sudo:
                command = "sudo " + command
            output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL if safe else None)
            return output.decode().strip()
        except subprocess.CalledProcessError:
            return "Command failed"
        except Exception as e:
            return f"Error: {e}"
