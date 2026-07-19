# 🔐 Keypass: Password Cracking Demonstrator

> **Self-Hosted Educational Security Tool** - Visually demonstrates the quantitative differences between Brute Force, Dictionary Attacks, and Rainbow Table lookups.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 What is Keypass?

Keypass is a local web application built with a Python FastAPI backend and a clean, responsive frontend. It serves as an educational instrument panel designed to show exactly why weak passwords fail. 

When a user inputs a password, the system hashes it and initiates a live race between three cracking methods: **Brute Force**, **Dictionary Attack**, and **Rainbow Table Lookup**. Through real-time WebSocket streaming, users can watch the raw candidate attempts and see the orders of magnitude difference in cracking times.

*Disclaimer: Educational tool only - test your own passwords only. Does not connect to live credential dumps.*

---

## ✨ Core Features

- **Multi-Algorithm Hasher**: Hashes inputs using `md5`, `sha1`, and `sha256`. Showcases the inherent vulnerabilities in older algorithms like md5.
- **Dictionary Attack Engine**: Streams through a localized wordlist (`common_passwords.txt`), hashes candidates, and reports match times instantly.
- **WebSocket Brute Force**: Uses `itertools.product` to exhaustively search characters. Streams live progress (attempts/sec, current candidate, elapsed time) directly to the frontend.
- **Rainbow Table Precomputation**: Demonstrates the terrifying speed of precomputation by caching hash-to-plaintext mappings for instant lookups.
- **Interactive Benchmark View**: Races all three methods side-by-side against passwords of increasing strength (e.g., `password1`, `Tr0ub4dor&3`, and random 16-char strings).

---

## 🛠️ Tech Stack & Design

- **Backend**: Python, FastAPI, WebSockets, `hashlib`, `itertools`
- **Frontend**: Vanilla HTML/CSS/JS (Lean and fast, no heavy UI framework bloat)
- **Design Language**: Cyber-instrumentation styling. Features deep slate backgrounds (`#0d1117`), real monospace typography (JetBrains Mono) for hash outputs and live attempt logs, and distinct state colors (Amber/Cyan) instead of generic hacker-green.

---

## 🚀 Quick Start (Local Run)

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/H8rsh100/Keypass.git
cd Keypass

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Server

```bash
# Start the FastAPI server
python backend/main.py
```
Open `http://localhost:8000` in your browser.

---

## 📁 Project Structure

```
Keypass/
├── backend/
│   ├── main.py              # FastAPI app, routes, websocket handlers
│   ├── hasher.py            # Hashing utility functions
│   ├── dictionary_attack.py # Dictionary streaming logic
│   ├── brute_force.py       # Itertools permutation engine
│   ├── rainbow_table.py     # Precomputation and SQLite/JSON caching
│   └── benchmark.py         # Side-by-side race coordinator
├── wordlists/
│   └── common_passwords.txt # Trimmed sample list (~10k-50k entries)
├── frontend/
│   ├── index.html           # Main instrument panel
│   ├── styles.css           # Slate/Amber UI theme
│   └── app.js               # WebSocket listeners & DOM updates
└── README.md
```

---

## ⚙️ GitHub Repository Configuration

To optimize your repository index card on GitHub, copy these tags into the **Topics** field in your repository settings:

`cybersecurity` `password-cracking` `fastapi` `websockets` `python` `educational-tool` `infosec` `cryptography`

---

## License

MIT - see LICENSE.
