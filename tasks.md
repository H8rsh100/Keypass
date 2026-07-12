# Keypass: Development Tasks & Progress

This task board tracks the implementation of **Keypass**, an educational password-cracking demonstrator featuring dictionary attacks, brute-forcing (with WebSocket streaming), and rainbow table lookups.

## Project Status
- **Current Phase:** Phase 1: Project Setup & Core Hasher
- **Total Progress:** [░░░░░░░░░░░░░░░░░░░░] 0% complete

---

## 📋 Roadmap & Task Checklist

### Phase 1: Environment & Core Cryptography (Setup)
- [ ] Initialize Python environment and install dependencies (`fastapi`, `uvicorn`, `websockets`, `bcrypt`) <!-- id: setup_env -->
- [ ] Implement `backend/hasher.py` with support for MD5, SHA-1, SHA-256, and bcrypt salting/hashing <!-- id: hasher_impl -->
- [ ] Write unit tests for hashing algorithms and verify hashing output <!-- id: hasher_tests -->
- [ ] Initialize FastAPI app structure (`backend/main.py`) <!-- id: fastapi_init -->

### Phase 2: Wordlist & Dictionary Attack
- [ ] Download/trim a wordlist of 10,000-50,000 common passwords into `wordlists/common_passwords.txt` <!-- id: wordlist_setup -->
- [ ] Implement `backend/dictionary_attack.py` for sequential dictionary attacks <!-- id: dict_attack -->
- [ ] Implement live tracking of dictionary attack progress <!-- id: dict_progress -->
- [ ] Connect dictionary attack endpoints to backend router <!-- id: dict_routes -->

### Phase 3: Brute Force & WebSocket Streaming
- [ ] Implement `backend/brute_force.py` using `itertools.product` to search custom charsets <!-- id: brute_force_impl -->
- [ ] Implement WebSocket endpoint in FastAPI for streaming brute force attempts (elapsed time, attempts/sec, keyspace) <!-- id: brute_force_ws -->
- [ ] Implement speed-limiting/caps to prevent crashing the server on long charsets <!-- id: brute_force_caps -->

### Phase 4: Rainbow Tables (Precomputation)
- [ ] Implement `backend/rainbow_table.py` for precomputing and storing hash-plaintext pairs in JSON/SQLite database <!-- id: rainbow_table_impl -->
- [ ] Create precomputation script for the wordlist to demonstrate instant lookup <!-- id: rainbow_table_precompute -->
- [ ] Implement instant lookups for all supported hash algorithms <!-- id: rainbow_table_lookup -->

### Phase 5: Benchmark & Security Insights
- [ ] Implement `backend/benchmark.py` to compare brute force, dictionary, and rainbow table methods side-by-side <!-- id: benchmark_impl -->
- [ ] Calculate password entropy and estimated time to crack for typical weak vs. strong passwords <!-- id: benchmark_entropy -->

### Phase 6: Front-end Interface (UI/UX)
- [ ] Build clean, responsive single-page frontend using plain HTML, CSS (sleek dark mode, custom monospace fonts, high-performance styling) and JS <!-- id: frontend_setup -->
- [ ] Implement real-time WebSocket logs and charts for live attempts visualizer <!-- id: frontend_ws -->
- [ ] Add educational safety disclaimer and guardrails to prevent unauthorized cracking attempts <!-- id: frontend_guardrails -->

### Phase 7: Polish & Validation
- [ ] Verify security guardrails (no uploading external hashes, local-only execution) <!-- id: security_audit -->
- [ ] Complete full end-to-end user experience walkthrough and performance tuning <!-- id: final_polish -->
