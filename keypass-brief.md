# Project Brief: Keypass (Password Cracking Demonstrator)

Hand this whole document to your coding agent as the spec. It's self-contained — architecture, features, and UI direction. Build it as a self-hosted educational tool: it hashes and cracks passwords the tool itself generates or that the user pastes in for the demo — no live/third-party credential dumps.

---

## 1. What we're building

A local web app (Python backend + browser frontend) that shows, visually and quantitatively, why weak passwords fail. User picks or types a password, it gets hashed, and three cracking methods race against it: brute force, dictionary attack, rainbow table lookup. The point is the *comparison* — 8 lowercase chars cracks in under a second, add length/symbols and it stops finishing in a demo's lifetime.

## 2. Tech stack

- **Backend:** Python, FastAPI (gives you WebSockets for live crack progress — much better demo than a spinner)
- **Hashing:** `hashlib` (md5, sha1, sha256 — deliberately include md5 to show why it's a bad choice), optionally `bcrypt` later to demonstrate salting/slow-hash defense
- **Frontend:** plain HTML/CSS/JS or React — agent's call, but no heavy UI framework bloat. This is a small app; keep it lean.
- **Wordlist:** ship a trimmed `common_passwords.txt` (~10-50k entries, not the full rockyou.txt) so the repo stays small and doesn't look like it's shipping attack infrastructure

## 3. Core features

1. **Hasher** — input a password (or list), output hash in chosen algorithm. Show the raw hash.
2. **Dictionary attack** — stream through wordlist, hash each candidate, compare. Report time and which entry (if any) matched.
3. **Brute force** — `itertools.product` over a charset up to a max length (cap it — e.g. 6 chars for live demo, warn the user anything past 8 with full charset will not finish live). Live progress via WebSocket: attempts/sec, current candidate, elapsed time.
4. **Rainbow table** — precompute hash→plaintext for the wordlist once, cache as JSON/SQLite. Lookup is instant. This is the "why precomputation is terrifying" moment — same wordlist, orders of magnitude faster than dictionary attack because the work was already done.
5. **Benchmark/report view** — run all three methods against a few example passwords of increasing strength (`password1`, `Tr0ub4dor&3`-style, a 16-char random string) and lay the results side by side: time to crack, method that succeeded, entropy estimate.

## 4. Guardrails to build in (not optional)

- No feature for cracking arbitrary uploaded hash files from unknown origin — the tool only cracks hashes it generated in-session or a password the user typed for the demo.
- No networking/scraping of leaked credential databases.
- Add a one-line disclaimer in the UI footer: "Educational tool — test your own passwords only."

## 5. File structure

```
Keypass/
├── backend/
│   ├── main.py              # FastAPI app, routes, websocket handlers
│   ├── hasher.py
│   ├── dictionary_attack.py
│   ├── brute_force.py
│   ├── rainbow_table.py
│   └── benchmark.py
├── wordlists/
│   └── common_passwords.txt
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── README.md
```

## 6. UI direction — read this whole section before writing any CSS

Goal: looks like a tool a security researcher actually built for a CTF or a conference talk — not a generic "hacker theme" template, and not a generic AI-generated dashboard. Specificity is what sells it.

**Avoid the defaults.** Skip: pure black background with a single neon-green matrix-rain accent, Courier New everywhere, terminal-cursor blink on every element, stock "glitch text" effects on the title. These read as *stock hacker aesthetic*, not as something someone actually designed. Also avoid the opposite failure mode — a soft dark-mode SaaS dashboard with rounded cards and a purple gradient — that just looks like every other AI-generated admin panel with black paint on top.

**Ground it in the real material.** The actual visual language of this domain isn't "hacker movie" — it's the tools themselves: hex dumps, hash outputs, terminal logs, packet captures, monospace tables of attempt counts. Let the UI look like an instrument panel for that material, not a costume.

**A concrete direction to build from (adjust as you like, but stay this specific):**
- **Palette:** near-black but not pure black background (`#0d1117`-ish, GitHub-dark-adjacent but pick your own), a desaturated slate/blue-gray for panels, one accent color used sparingly for "success/cracked" states and a second, different hue for "in progress" — don't use green-for-everything. Consider amber or cyan as the primary accent instead of the reflexive matrix-green.
- **Type:** a real monospace for data (hash output, live attempt counter, wordlist entries) — JetBrains Mono, Berkeley Mono, IBM Plex Mono — paired with a plain, restrained sans for UI chrome and labels. Don't set body copy in monospace; that's the tell of an unconsidered choice.
- **Layout signature:** make the live crack process the hero — a real-time scrolling log panel (like `tail -f`) showing candidates being tried, with the matched one highlighting distinctly when found, sitting next to a stats readout (attempts/sec, elapsed, charset size, keyspace remaining). That live panel *is* the demo; don't bury it below a summary card.
- **Motion:** the scrolling attempt log itself is the animation — that's enough. Don't add extra glitch/flicker effects on top; it'll undercut the credibility of the live data instead of adding to it.
- **Structural detail with a reason:** if you show the three methods side by side, don't just number them 1/2/3 — label them by what they actually are (dictionary size, keyspace size, precompute time) so the comparison itself teaches the lesson.

**Before shipping, sanity check:** would this look at home in a writeup on a real infosec blog, or does it look like a stock template with a dark filter? If the second, cut one effect and add one specific, real detail (an actual hash format, a real attempts/sec number, a real wordlist stat) instead.

## 7. Suggested build order

1. `hasher.py` + basic FastAPI route — confirm hashing works
2. `dictionary_attack.py` — get one method fully working end-to-end with the UI before building the other two
3. `brute_force.py` with WebSocket progress streaming
4. `rainbow_table.py` — precompute + lookup
5. `benchmark.py` + comparison view
6. UI pass — apply the design direction above once the functionality is real, so the live-data panel has real data to show off
