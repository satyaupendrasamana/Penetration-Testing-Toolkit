import socket

def port_scanner(target, start_port, end_port):
    """Scans the target for open ports in a given range."""
    print(f"\nScanning {target} from port {start_port} to {end_port}...\n")
    
    for port in range(start_port, end_port + 1):
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
start_port = int(input("Enter the start port: "))
end_port = int(input("Enter the end port: "))

port_scanner(target_ip, start_port, end_port)
