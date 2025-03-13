# Penetration-Testing-Toolkit.


This toolkit includes essential tools for penetration testing, helping security professionals and researchers identify vulnerabilities in systems.

## Features

- Port Scanner
- Brute-Force Tester

## Requirements

- Python 3.x
- Required libraries:
  - `requests`
  - `socket`

Install dependencies using:

```
pip install requests
```

## Usage

### Port Scanner

The Port Scanner scans a target system for open ports.

#### Steps to Run:

1. Run the script:
   ```
   python main.py
   ```
2. Enter the target IP or domain.
3. Enter the start and end ports to scan.
4. The script will display open and closed ports.
5. Results are saved in `scan_results.txt`.

### Brute-Force Tester

The Brute-Force Tester attempts to guess login credentials using a wordlist.

#### Steps to Run:

1. Ensure `passwords.txt` exists in the script directory with a list of test passwords.
2. Run the script:
   ```
   python brute_force.py
   ```
3. Enter the username for testing.
4. The script will attempt different passwords and display successful attempts.

## Legal Disclaimer

This toolkit is for educational and security research purposes only. Do not use it on unauthorized systems. The author is not responsible for any misuse.

# Penetration Testing Toolkit



