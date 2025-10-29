 
![License](https://img.shields.io/badge/License-MIT-yellow.svg)  
**Author:** [Shashi Samana](https://github.com/satyaupendrasamana)



# Penetration Testing Toolkit

A small collection of basic tools intended for learning and defensive testing:
- Port scanner for discovering open TCP ports on a target host.
- Brute-force tester for demonstrating password-guessing with a provided wordlist.

**Important:** Only use these tools on systems you own or have explicit permission to test. Unauthorized testing is illegal and unethical. See the Legal Disclaimer section below.

---

## Features
- Range-based TCP port scanning
- Brute-force login testing using a password list (configurable per target type)
- Simple CLI interface and structured text-based results
- Results written to the `results/` directory for review

---

## Repository structure

Penetration-Testing-Toolkit/
│
├── src/
│   ├── main.py           # Port scanner (CLI runner)
│   ├── brute_force.py    # Brute-force tester (HTTP form example)
│   ├── logger.py         # Logging utility
│   └── utils.py          # Optional helpers (validation, retry)
│
├── results/
│   └── scan_results.txt  # Run-time logs (ignored by default)
│
├── docs/
│   └── presentation.pptx # optional project PPT or notes
│
├── assets/
│   └── screenshots/      # example output images referenced in README
│
├── requirements.txt      # pip install -r requirements.txt
├── .gitignore
├── LICENSE
└── README.md

---

Author

Satya Upendra Samana
B.Tech – Mechanical Engineering
Aditya College of Engineering and Technology

Credits

This project was developed as part of the CODTECH IT SOLUTIONS PVT. LTD. Cybersecurity & Ethical Hacking Internship, with assistance from ChatGPT (OpenAI).



