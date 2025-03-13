import socket

def is_valid_ip(target):
    """Check if the input is a valid IP address or domain."""
    try:
        socket.gethostbyname(target)
        return True
    except socket.gaierror:
        return False

def port_scanner(target, start_port, end_port):
    """Scans the target for open ports in a given range and saves results."""
    results = []  # List to store scan results

    print(f"\nScanning {target} from port {start_port} to {end_port}...\n")
    
    for port in range(start_port, end_port + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Timeout of 1 second
            result = sock.connect_ex((target, port))
            
            if result == 0:
                result_text = f"✅ Port {port} is OPEN"
            else:
                result_text = f"❌ Port {port} is CLOSED"
            
            print(result_text)
            results.append(result_text)
            sock.close()
        except Exception as e:
            error_text = f"⚠️ Error scanning port {port}: {e}"
            print(error_text)
            results.append(error_text)

    # Save results to a file
    with open("scan_results.txt", "w") as file:
        file.write(f"Scan Results for {target} (Ports {start_port}-{end_port}):\n")
        file.write("\n".join(results))
    
    print("\n📄 Results saved to scan_results.txt!")

# Get user input with validation
while True:
    target_ip = input("Enter the target IP address or domain: ")
    if is_valid_ip(target_ip):
        break
    else:
        print("❌ Invalid IP or domain! Please enter a valid target.")

while True:
    try:
        start_port = int(input("Enter the start port (0-65535): "))
        end_port = int(input("Enter the end port (0-65535): "))

        if 0 <= start_port <= 65535 and 0 <= end_port <= 65535 and start_port <= end_port:
            break
        else:
            print("❌ Invalid port range! Please enter valid port numbers.")
    except ValueError:
        print("❌ Invalid input! Please enter numbers only.")

# Run the scanner
port_scanner(target_ip, start_port, end_port)
