"""
Port scanner (clean, handwritten)

Scans a range of TCP ports on a target host, prints results, writes a
human-readable results file to results/scan_results.txt, and optionally
uses a project logger (if src/logger.py exists).

Run from project root so paths resolve correctly:
    PYTHONPATH=src python src/port_scanner.py
"""

from typing import List
import socket
from pathlib import Path
from datetime import datetime
import json

# Optional logger import (logger.log_entry(event, target, details))
try:
    from logger import log_entry  # type: ignore
except Exception:
    log_entry = None  # type: ignore

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
RESULT_FILE = RESULTS_DIR / "scan_results.txt"

DEFAULT_TIMEOUT = 1.0


def _now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def is_valid_host(target: str) -> bool:
    """Return True if target resolves to an IP address (hostname or IP allowed)."""
    try:
        socket.gethostbyname(target)
        return True
    except socket.gaierror:
        return False


def scan_range(target: str, start_port: int, end_port: int, timeout: float = DEFAULT_TIMEOUT) -> List[int]:
    """
    Scan TCP ports on `target` from `start_port` to `end_port` (inclusive).

    Returns a sorted list of open ports. Raises ValueError for invalid inputs.
    """
    if not target:
        raise ValueError("Target cannot be empty.")
    if not is_valid_host(target):
        raise ValueError(f"Cannot resolve host: {target}")
    if not (0 <= start_port <= 65535 and 0 <= end_port <= 65535):
        raise ValueError("Port numbers must be between 0 and 65535.")
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
            # Host resolution problem
            raise ValueError(f"Unable to resolve host while scanning: {target}")
        except Exception:
            # Ignore transient socket errors and continue
            continue

    # Structured logging via logger if available
    if log_entry:
        if open_ports:
            log_entry("OPEN_PORTS", target, {"ports": open_ports, "checked": end_port - start_port + 1, "time": _now_iso()})
        else:
            log_entry("NO_OPEN_PORTS", target, {"checked": end_port - start_port + 1, "time": _now_iso()})

    return open_ports


def save_results_human(target: str, start_port: int, end_port: int, lines: List[str]) -> Path:
    """
    Write a human-readable summary to results/scan_results.txt and return the Path.
    Appends to the file (keeps history).
    """
    header = f"Scan Results for {target} (Ports {start_port}-{end_port}) - { _now_iso() }\n"
    with RESULT_FILE.open("a", encoding="utf-8") as f:
        f.write(header)
        for line in lines:
            f.write(line + "\n")
        f.write("\n")
    return RESULT_FILE


def run_cli() -> None:
    """Minimal CLI entry point. Run from project root so paths resolve."""
    target = input("Enter the target IP address or domain: ").strip()
    if not target:
        print("No target provided. Exiting.")
        return
    if not is_valid_host(target):
        print("Invalid IP or domain. Exiting.")
        return

    try:
        start_port = int(input("Enter the start port (0-65535): ").strip())
        end_port = int(input("Enter the end port (0-65535): ").strip())
    except ValueError:
        print("Invalid input: ports must be integers. Exiting.")
        return

    try:
        open_ports = scan_range(target, start_port, end_port)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Prepare lines for human-readable result file and console
    lines = []
    for port in range(start_port, end_port + 1):
        status = "OPEN" if port in open_ports else "CLOSED"
        line = f"{status} {port}/tcp on {target}"
        print(line)
        lines.append(line)

    saved = save_results_human(target, start_port, end_port, lines)
    print(f"\nResults appended to {saved}")


if __name__ == "__main__":
    run_cli()
