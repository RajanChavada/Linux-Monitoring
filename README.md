# Linux-Monitoring
A lightweight Linux system monitoring and hardware inspection tool built in Python.

## Features

- CPU, RAM, and disk usage collection
- Hardware probing (PCI, sensors)
- Log parsing from `dmesg`, `/var/log/syslog`
- REST API support (optional)
- Dockerized for portable deployment

## How to Run

```bash
python run.py

# or  with Docker 
docker build -t amd-sysmon .
docker run amd-sysmon
``` 