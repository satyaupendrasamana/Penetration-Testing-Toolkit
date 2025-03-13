import socket

def port_scanner(target, ports):
    """Scans the target for open ports."""
    print(f"\nScanning {target} for open ports...\n")
    
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout of 1 second
        result = sock.connect_ex((target, port))
        
        if result == 0:
            print(f"✅ Port {port} is OPEN")
        else:
            print(f"❌ Port {port} is CLOSED")
        
        sock.close()

# Example usage
target_ip = input("Enter the target IP address: ")
ports_to_scan = [22, 80, 443, 8080]  # Common ports
port_scanner(target_ip, ports_to_scan)
