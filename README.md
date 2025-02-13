# Advanced Network Port Scanner

This is an educational project demonstrating a high-performance, multi-threaded network port scanner. It's designed for learning about network security concepts and practicing ethical hacking techniques in controlled environments.

**Features**

* 🚀 High-speed scanning with customizable thread count
* 🎯 Flexible port specification (single, multiple, or ranges)
* 🌐 Support for various network range formats (CIDR notation, single octets)
* 📊 Real-time progress tracking
* 🔍 Banner grabbing capability (optional)
* 💾 Automatic result logging
* ⚡ Optimized for both speed and accuracy

**Disclaimer:** This tool is intended for educational purposes and authorized penetration testing only.  Use it responsibly and ethically. Always ensure you have proper authorization before scanning any networks or systems. Unauthorized scanning is illegal and can have serious consequences.

**Installation**
# Clone the repository
```bash
git clone https://github.com/TStefan0x/fast-portscanner.git
cd fast-portscanner
```
# Install requirements
```bash
pip install -r requirements.txt
```
# Make executable (if necessary)
```bash
chmod +x portscanner.py
```
# Scan multiple ports
```bash
./portscanner.py 192.168.1.0/24 --ports 22,80,443
```
# Enable banner grabbing (use with caution)
```bash
./portscanner.py 192.168.1.0/24 --ports 80 --banner
```
# Command Line Options

usage: portscanner.py [-h] [--ports PORTS] [--banner] [--threads THREADS] target

Network Port Scanner

positional arguments:
  target           Target network (e.g., 192.168.1.0/24, 10.0.0.0/8)

optional arguments:
  -h, --help       show this help message and exit
  --ports PORTS    Ports to scan (e.g., "22,80,443" or "20-25")
  --banner         Enable banner grabbing
  --threads THREADS  Number of threads (default: 500)

# Input Formats

CIDR notation: 192.168.1.0/24
Single octet: 10 (scans 10.0.0.0/8)
Two octets: 192.168 (scans 192.168.0.0/16)
Three octets: 192.168.1 (scans 192.168.1.0/24)
# Output Files

scan_results.txt: Contains all discovered IP:Port combinations
banner.log: Contains banner information when banner grabbing is enabled
