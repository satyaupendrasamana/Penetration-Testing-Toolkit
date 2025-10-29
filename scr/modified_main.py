"""
Port scanner (handwritten, professional)

Scans a range of TCP ports on a target host. The scanner returns a list of
open ports and optionally logs findings using a project logger if available.

Usage (run from project root so relative paths work):
    PYTHONPATH=src python src/modified.py
"""

from typing import List
import socket
from pathlib import Path
from datetime import datetime

# Try to import a logger if present (logger.log_entry(event, target, details))
try:
    from logger import log_entry  # type: ignore
except Exception:
    log_entry = None  # type: ignore

DEFAULT_TIMEOUT = 1.0


def _now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def scan_range(target: str, start_port: int, end_port: int, timeout: float = DEFAULT_TIMEOUT) -> List[int]:
    """
    Scan TCP ports on target from start_port to end_port (inclusive).

    Args:
        target: IP or hostname to scan.
        start_port: starting port (1-65535).
        end_port: ending port (1-65535).
        timeout: socket timeout in seconds.

    Returns:
        A sorted list of open ports found.
    """
    if start_port < 1 or end_port < 1 or start_port > 65535 or end_port > 65535:
        raise ValueError("Port numbers must be in range 1-65535.")
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
            # Host resolution failed — bubble up meaningful error
            raise ValueError(f"Unable to resolve host: {target}")
        except Exception:
            # For other socket errors, skip this port and continue scanning
            continue

    # Optional: log result using project logger if available
    if log_entry:
        if open_ports:
            log_entry("OPEN_PORTS", target, {"ports": open_ports, "checked": end_port - start_port + 1, "time": _now_iso()})
        else:
            log_entry("NO_OPEN_PORTS", target, {"checked": end_port - start_port + 1, "time": _now_iso()})

    return open_ports


def to_int(value: str, default: int = 0) -> int:
    """Convert string to int safely, returning default on failure."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


if __name__ == "__main__":
    # Interactive CLI
    target_input = input("Enter target IP or hostname: ").strip()
    if not target_input:
        print("No target provided. Exiting.")
        raise SystemExit(1)

    start_input = input("Enter start port (e.g. 1): ").strip()
    end_input = input("Enter end port (e.g. 1024): ").strip()

    start = to_int(start_input, 1)
    end = to_int(end_input, 1024)

    try:
        open_ports = scan_range(target_input, start, end)
    except ValueError as e:
        print(f"Input error: {e}")
        raise SystemExit(1)

    if open_ports:
        for p in open_ports:
            print(f"Port {p} is OPEN on {target_input}")
    else:
        print(f"No open ports detected on {target_input} (checked {end - start + 1} ports).")
