import os
import sqlite3
import hashlib
from typing import Optional, Dict, Any, Generator
from backend.hasher import hash_password

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "wordlists", "rainbow_table.db"))
WORDLIST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "wordlists", "common_passwords.txt"))

def get_db_connection() -> sqlite3.Connection:
    """
    Establishes a connection to the SQLite rainbow table database.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """
    Initializes the database schema.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create table for pre-computed hashes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hashes (
            hash_value TEXT NOT NULL,
            algorithm TEXT NOT NULL,
            plaintext TEXT NOT NULL,
            PRIMARY KEY (hash_value, algorithm)
        )
    """)
    # Add indexes for fast lookups
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_hash_algo ON hashes(hash_value, algorithm)")
    conn.commit()
    conn.close()

def precompute_rainbow_table(
    update_interval: int = 500
) -> Generator[Dict[str, Any], None, None]:
    """
    Precomputes hashes (md5, sha1, sha256) for the words in the wordlist.
    Yields progress dicts.
    """
    init_db()
    
    if not os.path.exists(WORDLIST_PATH):
        yield {"error": "Wordlist not found.", "status": "failed"}
        return

    try:
        with open(WORDLIST_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            words = [line.strip() for line in f if line.strip()]
    except Exception as e:
        yield {"error": f"Failed to read wordlist: {str(e)}", "status": "failed"}
        return

    total_words = len(words)
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get already indexed count to avoid double work or provide resume functionality
    cursor.execute("SELECT COUNT(*) as count FROM hashes")
    existing_count = cursor.fetchone()["count"]

    # We support MD5, SHA-1, SHA-256 for rainbow table (bcrypt is intentionally left out due to salting and slow-hashing demo)
    algorithms = ["md5", "sha1", "sha256"]
    
    # We will clear table and rebuild to ensure it matches the current wordlist
    cursor.execute("DELETE FROM hashes")
    conn.commit()

    batch_size = 500
    batch = []
    
    processed = 0

    for i, word in enumerate(words):
        for algo in algorithms:
            try:
                hashed = hash_password(word, algo)
                batch.append((hashed, algo, word))
            except Exception:
                continue

        processed += 1

        if len(batch) >= batch_size or processed == total_words:
            cursor.executemany(
                "INSERT OR REPLACE INTO hashes (hash_value, algorithm, plaintext) VALUES (?, ?, ?)",
                batch
            )
            conn.commit()
            batch = []
            
            yield {
                "processed": processed,
                "total": total_words,
                "percent": int((processed / total_words) * 100),
                "status": "in_progress"
            }

    conn.close()
    yield {
        "processed": total_words,
        "total": total_words,
        "percent": 100,
        "status": "complete"
    }

def lookup_hash(hash_val: str, algorithm: str) -> Optional[str]:
    """
    Performs an instant O(1) lookup in the precomputed database.
    """
    if not os.path.exists(DB_PATH):
        return None
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT plaintext FROM hashes WHERE hash_value = ? AND algorithm = ? LIMIT 1",
        (hash_val.lower(), algorithm.lower())
    )
    row = cursor.fetchone()
    conn.close()
    
    return row["plaintext"] if row else None
