import time
import os
from typing import Generator, Dict, Any, Optional
from backend.hasher import verify_password

WORDLIST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "wordlists", "common_passwords.txt"))

def dictionary_attack(
    target_hash: str, 
    algorithm: str, 
    update_interval: int = 200
) -> Generator[Dict[str, Any], None, None]:
    """
    Performs a dictionary attack against a target hash using the wordlist.
    Yields progress dictionary updates periodically.
    """
    if not os.path.exists(WORDLIST_PATH):
        yield {
            "error": "Wordlist file not found.",
            "attempts": 0,
            "found": False,
            "elapsed": 0.0
        }
        return

    start_time = time.time()
    attempts = 0
    
    # Read the file to get total lines for progress tracking
    try:
        with open(WORDLIST_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            words = [line.strip() for line in f if line.strip()]
    except Exception as e:
        yield {
            "error": f"Failed to read wordlist: {str(e)}",
            "attempts": 0,
            "found": False,
            "elapsed": 0.0
        }
        return

    total_words = len(words)

    for word in words:
        attempts += 1
        elapsed = time.time() - start_time
        
        # Check if password matches
        is_match = verify_password(word, target_hash, algorithm)
        
        if is_match:
            yield {
                "attempts": attempts,
                "total": total_words,
                "current_candidate": word,
                "elapsed": elapsed,
                "attempts_per_second": int(attempts / elapsed) if elapsed > 0 else 0,
                "found": True,
                "plaintext": word
            }
            return

        # Yield progress updates periodically
        if attempts % update_interval == 0 or attempts == total_words:
            yield {
                "attempts": attempts,
                "total": total_words,
                "current_candidate": word,
                "elapsed": elapsed,
                "attempts_per_second": int(attempts / elapsed) if elapsed > 0 else 0,
                "found": False
            }
            # Short sleep to prevent blocking the async loop entirely
            time.sleep(0.001)

    # Finished and not found
    elapsed = time.time() - start_time
    yield {
        "attempts": attempts,
        "total": total_words,
        "current_candidate": "",
        "elapsed": elapsed,
        "attempts_per_second": int(attempts / elapsed) if elapsed > 0 else 0,
        "found": False,
        "plaintext": None
    }
