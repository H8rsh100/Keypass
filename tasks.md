# Keypass: Development Tasks & Progress

This task board tracks the implementation of **Keypass**, an educational password-cracking demonstrator featuring dictionary attacks, brute-forcing (with WebSocket streaming), and rainbow table lookups.

## Project Status
- **Current Phase:** Phase 7: Polish & Validation
- **Total Progress:** [██████████████████░░] 90% complete

---

## 📋 Roadmap & Task Checklist

### Phase 1: Environment & Core Cryptography (Setup)
- [x] Initialize Python environment and install dependencies (`fastapi`, `uvicorn`, `websockets`, `bcrypt`) <!-- id: setup_env -->
- [x] Implement `backend/hasher.py` with support for MD5, SHA-1, SHA-256, and bcrypt salting/hashing <!-- id: hasher_impl -->
- [x] Write unit tests for hashing algorithms and verify hashing output <!-- id: hasher_tests -->
- [x] Initialize FastAPI app structure (`backend/main.py`) <!-- id: fastapi_init -->

### Phase 2: Wordlist & Dictionary Attack
- [x] Download/trim a wordlist of 10,000-50,000 common passwords into `wordlists/common_passwords.txt` <!-- id: wordlist_setup -->
- [x] Implement `backend/dictionary_attack.py` for sequential dictionary attacks <!-- id: dict_attack -->
- [x] Implement live tracking of dictionary attack progress <!-- id: dict_progress -->
- [x] Connect dictionary attack endpoints to backend router <!-- id: dict_routes -->

### Phase 3: Brute Force & WebSocket Streaming
- [x] Implement `backend/brute_force.py` using `itertools.product` to search custom charsets <!-- id: brute_force_impl -->
- [x] Implement WebSocket endpoint in FastAPI for streaming brute force attempts (elapsed time, attempts/sec, keyspace) <!-- id: brute_force_ws -->
- [x] Implement speed-limiting/caps to prevent crashing the server on long charsets <!-- id: brute_force_caps -->

### Phase 4: Rainbow Tables (Precomputation)
- [x] Implement `backend/rainbow_table.py` for precomputing and storing hash-plaintext pairs in JSON/SQLite database <!-- id: rainbow_table_impl -->
- [x] Create precomputation script for the wordlist to demonstrate instant lookup <!-- id: rainbow_table_precompute -->
- [x] Implement instant lookups for all supported hash algorithms <!-- id: rainbow_table_lookup -->

### Phase 5: Benchmark & Security Insights
- [x] Implement `backend/benchmark.py` to compare brute force, dictionary, and rainbow table methods side-by-side <!-- id: benchmark_impl -->
- [x] Calculate password entropy and estimated time to crack for typical weak vs. strong passwords <!-- id: benchmark_entropy -->

### Phase 6: Front-end Interface (UI/UX)
- [x] Build clean, responsive single-page frontend using plain HTML, CSS (sleek dark mode, custom monospace fonts, high-performance styling) and JS <!-- id: frontend_setup -->
- [x] Implement real-time WebSocket logs and charts for live attempts visualizer <!-- id: frontend_ws -->
- [x] Add educational safety disclaimer and guardrails to prevent unauthorized cracking attempts <!-- id: frontend_guardrails -->

### Phase 7: Polish & Validation
- [ ] Verify security guardrails (no uploading external hashes, local-only execution) <!-- id: security_audit -->
- [ ] Complete full end-to-end user experience walkthrough and performance tuning <!-- id: final_polish -->
