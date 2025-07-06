""" 
    This module will provide the monitoring capabilites 
    
"""


from monitor.system_info import SystemInfo

import json 



def main(): 
    system_monitor = SystemInfo()
    data = system_monitor.collect_all()
    print(json.dumps(data, indent=2))

if __name__ == "__main__": 
    main()