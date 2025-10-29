"""
Port scanner module (clean, handwritten)

Functions:
- is_valid_host(target) -> bool
- scan_range(target, start_port, end_port, timeout) -> list[int]
- parse_port_input(s) -> int

CLI: run from project root so relative paths and logger work:
    PYTHONPATH=src python src/port_scanner.py
"""

from typing import List, Tuple
import socket
from datetime import datetime
from pathlib import Path

# Optional logger: if src/logger.py provides log_entry(event, target, details)
try:
    from logger import log_entry  # type: ignore
except Exception:
    log_entry = None  # type: ignore

DEFAULT_TIMEOUT = 1.0


def _now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def is_valid_host(target: str) -> bool:
    """Return True if target resolves to an IP address (hostname or IP accepted)."""
    try:
        socket.gethostbyname(target)
        return True
    except socket.gaierror:
        return False


def scan_range(target: str, start_port: int, end_port: int, timeout: float = DEFAULT_TIMEOUT) -> List[int]:
    """
    Scan TCP ports on `target` from `start_port` to `end_port` (inclusive).

    Returns:
        A sorted list of open ports.

    Raises:
        ValueError on invalid input (bad host or out-of-range ports).
    """
    if not target:
        raise ValueError("Target cannot be empty.")
    if not is_valid_host(target):
        raise ValueError(f"Cannot resolve host: {target}")
    if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
        raise ValueError("Port numbers must be between 1 and 65535.")
    if end_port < start_port:
        raise ValueError("end_port must be greater than or equal to start_port.")

    open_ports: List[int] = []

    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
        except socket.gaierror:
            # Host resolution failed while scanning
            raise ValueError(f"Unable to resolve host while scanning: {target}")
        except Exception:
            # Ignore transient socket errors and continue scanning
            continue

    # Optional structured logging
    if log_entry:
        if open_ports:
            log_entry("OPEN_PORTS", target, {"ports": open_ports, "checked": end_port - start_port + 1, "time": _now_iso()})
        else:
            log_entry("NO_OPEN_PORTS", target, {"checked": end_port - start_port + 1, "time": _now_iso()})

    return open_ports


def parse_port_input(value: str, default: int) -> int:
    """Convert a string input to int; return default on empty input or raise ValueError on invalid."""
    if not value.strip():
        return default
    try:
        return int(value.strip())
    except ValueError:
        raise ValueError("Port must be an integer.")


def _cli() -> None:
    """Minimal CLI entry point. Run from project root so logger and results paths work."""
    target = input("Enter the target IP address or domain: ").strip()
    if not target:
        print("No target provided. Exiting.")
        return
    if not is_valid_host(target):
        print("Invalid or unresolved host. Exiting.")
        return

    try:
        start = parse_port_input(input("Enter the start port (1-65535, default 1): "), 1)
        end = parse_port_input(input("Enter the end port (1-65535, default 1024): "), 1024)
    except ValueError as e:
        print(f"Input error: {e}")
        return

    try:
        open_ports = scan_range(target, start, end)
    except ValueError as e:
        print(f"Error: {e}")
        return

    if open_ports:
        for p in open_ports:
            print(f"Port {p} is OPEN on {target}")
    else:
        print(f"No open ports detected on {target} (checked {end - start + 1} ports).")


if __name__ == "__main__":
    _cli()
