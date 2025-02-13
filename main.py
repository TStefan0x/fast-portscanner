#!/usr/bin/env python3
import socket
import threading
import ipaddress
import sys
import os
import time
import argparse
from concurrent.futures import ThreadPoolExecutor
from typing import List

class PortScanner:
    def __init__(self, max_threads=500, ports=None):
        self.max_threads = max_threads
        self.ports = ports or [22]
        self.banner_mode = False
        self.output_file = "scan_results.txt"
        self.banner_file = "banner.log"
        self.hosts_scanned = 0
        self.total_hosts = 0
        self.lock = threading.Lock()
        self.found_hosts = []
        self.scanning_complete = False  # Flag to signal display loop to stop

    def print_banner(self):
        banner = """
\033[32m╔════════════════════════════════════════╗
║    Network Port Scanner v1.0           ║
║    For Educational Purposes Only!      ║
╚════════════════════════════════════════╝\033[0m

\033[33m[!] Legal Disclaimer: This tool is for educational 
    and authorized testing purposes only.
    Unauthorized scanning is prohibited.\033[0m
"""
        print(banner)

    def check_port(self, ip: str, port: int) -> bool:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.2)
        try:
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            sock.close()
            return False

    def display_loop(self):
        """Continuously refresh the screen to show found hosts and a static progress bar."""
        while not self.scanning_complete:
            with self.lock:
                # Clear screen and move cursor to top.
                sys.stdout.write("\033[2J\033[H")
                # (Optional) Reprint a header/banner.
                print("\033[32mNetwork Port Scanner v1.0\033[0m")
                print("\033[33mFor Educational Purposes Only\033[0m\n")
                # Print all found host messages.
                for msg in self.found_hosts:
                    print(msg)
                print("\n")
                # Calculate and print the progress bar.
                if self.total_hosts > 0:
                    percentage = (self.hosts_scanned / self.total_hosts) * 100
                    bar_length = 50
                    filled_length = int(bar_length * self.hosts_scanned / self.total_hosts)
                    bar = '█' * filled_length + '░' * (bar_length - filled_length)
                    progress_str = f'\033[36m[*] Progress: |{bar}| {percentage:.1f}% Complete ({self.hosts_scanned}/{self.total_hosts})\033[0m'
                else:
                    progress_str = "\033[36m[*] Progress: No hosts to scan.\033[0m"
                # Print the progress bar as the last (static) line.
                print(progress_str, end='')
            time.sleep(0.5)
        # Final update after scanning completes.
        with self.lock:
            sys.stdout.write("\033[2J\033[H")
            print("\033[32mNetwork Port Scanner v1.0 - Scan Completed\033[0m")
            print("\033[33mFor Educational Purposes Only\033[0m\n")
            for msg in self.found_hosts:
                print(msg)
            print("\n")
            if self.total_hosts > 0:
                percentage = (self.hosts_scanned / self.total_hosts) * 100
                bar_length = 50
                filled_length = int(bar_length * self.hosts_scanned / self.total_hosts)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                progress_str = f'\033[36m[*] Final Progress: |{bar}| {percentage:.1f}% Complete ({self.hosts_scanned}/{self.total_hosts})\033[0m'
            else:
                progress_str = "\033[36m[*] Progress: No hosts to scan.\033[0m"
            print(progress_str)

    def quick_scan_host(self, ip: str):
        for port in self.ports:
            if self.check_port(str(ip), port):
                if self.banner_mode:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(0.3)
                        sock.connect((str(ip), port))
                        banner = sock.recv(1024).decode().strip()
                        sock.close()
                        with open(self.banner_file, 'a') as f:
                            f.write(f"{ip}:{port}:{banner}\n")
                    except:
                        banner = "No banner"
                with open(self.output_file, 'a') as f:
                    f.write(f"{ip}:{port}\n")
                with self.lock:
                    # Append found host message (without immediate printing).
                    self.found_hosts.append(f"\033[92m[+] Found open port {port} on {ip}\033[0m")
        with self.lock:
            self.hosts_scanned += 1

    def scan_network(self, network: str):
        try:
            network_obj = ipaddress.ip_network(network, strict=False)
            hosts = list(network_obj.hosts())
            with self.lock:
                self.total_hosts += len(hosts)
            # Print a one-time message to the console (will be overwritten by display_loop).
            print(f"\n\033[36m[*] Scanning network: {network_obj}")
            print(f"[*] Ports to scan: {', '.join(map(str, self.ports))}")
            print(f"[*] Hosts to scan in this range: {len(hosts)}\033[0m\n")
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                executor.map(self.quick_scan_host, hosts)
        except Exception as e:
            print(f"\n\033[91m[!] Error scanning network {network}: {str(e)}\033[0m")

def parse_ports(ports_str: str) -> List[int]:
    """Parse port string into list of integers."""
    try:
        if ',' in ports_str:
            return [int(p) for p in ports_str.split(',')]
        elif '-' in ports_str:
            start, end = map(int, ports_str.split('-'))
            return list(range(start, end + 1))
        else:
            return [int(ports_str)]
    except:
        return None

def get_user_confirmation(args):
    """Get user confirmation for default values."""
    if not args.ports and not args.threads:
        print("\n\033[93m[!] No ports or thread count specified. Default values are:")
        print("    - Port: 22 (SSH)")
        print("    - Threads: 500")
        response = input("Do you want to continue with these defaults? (y/n): \033[0m").lower()
        if response != 'y':
            print("\n\033[91mScan cancelled. Please specify ports using --ports option.")
            print("Example: --ports 22,80,443 or --ports 20-25\033[0m")
            sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='Network Port Scanner')
    parser.add_argument('target', help='Target network (e.g., 10, 192.168, or "all")')
    parser.add_argument('--ports', help='Ports to scan (e.g., "22,80,443" or "20-25")')
    parser.add_argument('--banner', action='store_true', help='Enable banner grabbing')
    parser.add_argument('--threads', type=int, help='Number of threads (default: 500)')
    args = parser.parse_args()

    # Check if default values should be used.
    get_user_confirmation(args)

    # Parse ports.
    ports = parse_ports(args.ports) if args.ports else None
    if args.ports and not ports:
        print("\033[91m[!] Invalid port specification. Use format: 22,80,443 or 20-25\033[0m")
        sys.exit(1)

    scanner = PortScanner(
        max_threads=args.threads or 500,
        ports=ports
    )
    scanner.print_banner()
    scanner.banner_mode = args.banner

    # Start the display thread to refresh output.
    display_thread = threading.Thread(target=scanner.display_loop, daemon=True)
    display_thread.start()

    start_time = time.time()

    # Handle different input formats.
    target = args.target
    if target == "all":
        ranges = ["192.168.0.0/16", "172.16.0.0/12", "10.0.0.0/8"]
    elif len(target.split('.')) == 1:
        ranges = [f"{target}.0.0.0/8"]
    elif len(target.split('.')) == 2:
        ranges = [f"{target}.0.0/16"]
    elif len(target.split('.')) == 3:
        ranges = [f"{target}.0/24"]
    else:
        ranges = [target]

    for network in ranges:
        scanner.scan_network(network)

    # Signal the display thread that scanning is complete.
    scanner.scanning_complete = True
    display_thread.join()

    duration = time.time() - start_time
    print(f"\n\n\033[94m[*] Scan completed in {duration:.2f} seconds")
    print(f"[*] Results saved to {scanner.output_file}")
    if args.banner:
        print(f"[*] Banner information saved to {scanner.banner_file}\033[0m")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[91m[!] Scan interrupted by user\033[0m")
        sys.exit(0)
