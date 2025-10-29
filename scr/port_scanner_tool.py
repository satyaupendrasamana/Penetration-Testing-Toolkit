"""
Port scanner utility (handwritten, professional)

Provides a small, synchronous TCP port scanner that attempts to connect to each
target port and returns which ports are open. The module is written for clarity
and reuse: the scanning function returns results instead of printing only.

If a `logger.log_entry` function is available in the repository, the scanner
will call it to record findings in `results/scan_results.txt`.
"""

from typing import Iterable, List, Tuple
import socket
from pathlib import Path
from datetime import datetime

# Attempt to import a project logger if present (optional).
try:
    from logger import log_entry  # expects src/logger.py to provide log_entry()
except Exception:
    log_entry = None  # type: ignore

DEFAULT_TIMEOUT = 1.0
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def _timestamp() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def scan_ports(target: str, ports: Iterable[int], timeout: float = DEFAULT_TIMEOUT) -> List[int]:
    """
    Scan the given TCP ports on the target host.

    Args:
        target: IP address or hostname to scan.
        ports: Iterable of integer port numbers to test.
        timeout: Socket timeout in seconds for each connection attempt.

    Returns:
        A list of open ports (integers). The list is empty if no open ports found.
    """
    open_ports: List[int] = []

    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
        except socket.gaierror:
            # Hostname resolution failed for target
            raise ValueError(f"Unable to resolve host: {target}")
        except Exception:
            # Any other socket error — skip this port and continue
            continue

    # Optional logging
    if log_entry:
        if open_ports:
            log_entry(f"OPEN {' '.join(str(p) for p in open_ports)} on {target}")
        else:
            log_entry(f"NO_OPEN_PORTS on {target}")

    return open_ports


def parse_ports(port_input: str) -> List[int]:
    """
    Parse a user-provided port specification into a list of port integers.

    Supported formats:
      - Comma-separated list: "22,80,443"
      - Range: "1-1024"
      - Mixed: "22,80,1000-1010"

    Returns:
        A sorted list of unique port numbers (within 1-65535).
    """
    ports = set()
    for token in (p.strip() for p in port_input.split(",")):
        if not token:
            continue
        if "-" in token:
            try:
                start_str, end_str = token.split("-", 1)
                start = int(start_str)
                end = int(end_str)
                for p in range(max(1, start), min(65535, end) + 1):
                    ports.add(p)
            except ValueError:
                continue
        else:
            try:
                val = int(token)
                if 1 <= val <= 65535:
                    ports.add(val)
            except ValueError:
                continue
    return sorted(ports)


if __name__ == "__main__":
    # Simple CLI for interactive use. Run from project root:
    #   PYTHONPATH=src python src/port_scanner.py
    target = input("Enter target IP or hostname: ").strip()
    if not target:
        print("No target provided. Exiting.")
        raise SystemExit(1)

    port_spec = input("Enter ports (e.g. 22,80,443 or 1-1024): ").strip() or "1-1024"
    ports_list = parse_ports(port_spec)
    if not ports_list:
        print("No valid ports parsed. Exiting.")
        raise SystemExit(1)

    try:
        found = scan_ports(target, ports_list)
    except ValueError as e:
        print(e)
        raise SystemExit(1)

    if found:
        for p in found:
            print(f"Port {p} is OPEN on {target}")
    else:
        print(f"No open ports detected on {target} (checked {len(ports_list)} ports).")
