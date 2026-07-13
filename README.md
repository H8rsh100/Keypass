# Keypass: Password Cracking Demonstrator

Keypass is an interactive, local educational tool designed to visually demonstrate the strength and vulnerabilities of different password hashing configurations. By pitting three cracking methods (brute-force, dictionary attack, and precomputed rainbow tables) against user-defined or randomly generated passwords, it provides a quantitative lesson on password entropy and modern cryptographic hygiene.

## Key Features

1. **Multi-Algorithm Hasher:** Generates and displays raw hashes using MD5, SHA-1, SHA-256, and bcrypt to show the difference between weak legacy hashes and modern slow salted hashes.
2. **Sequential Dictionary Attack:** Streams candidate passwords from a trimmed local list (~10,000 common credentials), showing real-time iteration speed and matched items.
3. **Combinatorial Brute Force:** Generates character permutations dynamically using custom pools (lowercase, uppercase, digits, symbols) and streams live metrics via WebSockets with configurable length caps and execution limits.
4. **Precomputed Rainbow Tables:** Precomputes hashes for the entire wordlist and caches them in an SQLite database, showing why precomputed index tables can break weak hashes in absolute O(1) time.
5. **Insights & Benchmarks:** Displays password entropy calculation alongside side-by-side crack comparisons, highlighting why length and complexity are key defenses.

---

## Architecture & Project Structure

The project is structured cleanly to separate backend logic, the wordlist assets, and a lightweight web dashboard:

```
Keypass/
├── backend/
│   ├── main.py              # FastAPI application & WebSocket handlers
│   ├── hasher.py            # Password hashing & verification wrapper
│   ├── dictionary_attack.py # Dictionary matching generator
│   ├── brute_force.py       # Itertools-based brute-force generator
│   ├── rainbow_table.py     # SQLite precomputation & O(1) lookup
│   └── benchmark.py         # Side-by-side performance comparator & entropy formula
├── wordlists/
│   ├── common_passwords.txt # Trimmed 10,000 common passwords list
│   └── rainbow_table.db     # SQLite cache (generated dynamically)
├── frontend/
│   ├── index.html           # Dark-themed CTF-style UI template
│   ├── styles.css           # Vanilla CSS layout and animations
│   └── app.js               # Frontend controller, WebSocket streams, and chart logic
├── tests/                   # Pytest suite verifying backend functionality
├── requirements.txt         # Python dependencies
└── tasks.md                 # Project roadmap and checklist
```

---

## Guardrails & Disclaimers

To align with ethical guidelines and prevent potential abuse:
- **No Remote Credential Lookups:** The application operates completely locally and does not fetch or query any external third-party credential databases or leaks.
- **No Arbitrary Uploads:** The system only cracks hashes generated during the active session or entered into the demonstrator dashboard.
- **Strict Execution Limits:** Brute force and dictionary attempts are rate-limited on the backend and capped to prevent server crashes or lockups.
- **Educational Intent Only:** Built solely for cybersecurity educators, students, and professionals to demonstrate credential safety.

---

## Local Setup & Execution

### 1. Prerequisites
- Python 3.10+
- Git

### 2. Installation
Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/H8rsh100/Keypass.git
cd Keypass
```

Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Start the FastAPI server using Uvicorn:
```bash
uvicorn backend.main:app --reload --port 8000
```
Open your browser and navigate to: `http://localhost:8000`

### 4. Running the Tests
To run the full suite of cryptography and cracking logic tests, run:
```bash
pytest
```
