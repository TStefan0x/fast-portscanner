# fast-portscanner
A port scanner developed in python that supports multi-threading and helps you in your pentesting path scanning local ranges (even A class like 10,172) without having root !
Advanced Network Port Scanner
A high-performance, multi-threaded network port scanner designed for educational and authorized penetration testing purposes.
Features

🚀 High-speed scanning with customizable thread count
🎯 Flexible port specification (single, multiple, or ranges)
🌐 Support for various network range formats
📊 Real-time progress tracking
🔍 Banner grabbing capability
💾 Automatic result logging
⚡ Optimized for both speed and accuracy

Installation
bashCopy# Clone the repository
git clone https://github.com/yourusername/advanced-portscanner.git
cd advanced-portscanner

# Install requirements
pip install -r requirements.txt

# Make executable
chmod +x portscanner.py
Usage
Basic scan with default settings (port 22):
bashCopy./portscanner.py 192.168
Scan multiple ports:
bashCopy./portscanner.py 10 --ports 22,80,443
Scan port range:
bashCopy./portscanner.py 192.168 --ports 20-25
Scan with custom thread count:
bashCopy./portscanner.py 10 --ports 22 --threads 800
Enable banner grabbing:
bashCopy./portscanner.py 192.168 --ports 80 --banner
Command Line Options
Copyusage: portscanner.py [-h] [--ports PORTS] [--banner] [--threads THREADS] target

Network Port Scanner

positional arguments:
  target           Target network (e.g., 10, 192.168, or "all")

optional arguments:
  -h, --help       show this help message and exit
  --ports PORTS    Ports to scan (e.g., "22,80,443" or "20-25")
  --banner         Enable banner grabbing
  --threads THREADS  Number of threads (default: 500)
Input Formats

Single octet: 10 (scans 10.0.0.0/8)
Two octets: 192.168 (scans 192.168.0.0/16)
Three octets: 192.168.1 (scans 192.168.1.0/24)
Full range: 192.168.1.0/24
Special: all (scans all private ranges)

Output Files

scan_results.txt: Contains all discovered IP:Port combinations
banner.log: Contains banner information when banner grabbing is enabled

Security Notice
This tool is intended for educational purposes and authorized testing only. Always ensure you have proper authorization before scanning any networks or systems.
License
MIT License
