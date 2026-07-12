import time
import itertools
from typing import Generator, Dict, Any, List

# Define common charsets
CHARSETS = {
    "lowercase": "abcdefghijklmnopqrstuvwxyz",
    "uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "digits": "0123456789",
    "symbols": "!@#$%^&*()-_=+[]{}|;:',.<>?/"
}

def get_charset_string(selected_types: List[str]) -> str:
    """
    Combines pre-defined charsets based on selected types.
    """
    charset = ""
    for t in selected_types:
        if t in CHARSETS:
            charset += CHARSETS[t]
    # Remove duplicates and maintain order
    return "".join(sorted(list(set(charset))))

def brute_force_attack(
    target_hash: str,
    algorithm: str,
    charset_types: List[str],
    max_length: int = 4,
    update_interval: int = 50000,
    hard_limit_seconds: float = 60.0
) -> Generator[Dict[str, Any], None, None]:
    """
    Performs a brute-force attack using itertools.product.
    Yields progress dicts periodically.
    Caps length to prevent freezing the server, and has a hard time limit.
    """
    charset = get_charset_string(charset_types)
    if not charset:
        yield {
            "error": "No charset selected.",
            "attempts": 0,
            "found": False,
            "elapsed": 0.0
        }
        return

    # Hard cap on max length to prevent crashes
    if max_length > 8:
        max_length = 8

    # Calculate total keyspace
    keyspace = sum(len(charset) ** l for l in range(1, max_length + 1))
    
    start_time = time.time()
    attempts = 0
    from backend.hasher import verify_password

    # Iterate over lengths
    for length in range(1, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            attempts += 1
            word = "".join(combo)
            elapsed = time.time() - start_time
            
            # Check matching
            if verify_password(word, target_hash, algorithm):
                yield {
                    "attempts": attempts,
                    "keyspace": keyspace,
                    "current_candidate": word,
                    "elapsed": elapsed,
                    "attempts_per_second": int(attempts / elapsed) if elapsed > 0 else 0,
                    "found": True,
                    "plaintext": word
                }
                return

            # Check time limit
            if elapsed > hard_limit_seconds:
                yield {
                    "attempts": attempts,
                    "keyspace": keyspace,
                    "current_candidate": word,
                    "elapsed": elapsed,
                    "attempts_per_second": int(attempts / elapsed) if elapsed > 0 else 0,
                    "found": False,
                    "error": f"Time limit of {hard_limit_seconds}s exceeded."
                }
                return

            # Yield progress periodically
            if attempts % update_interval == 0:
                yield {
                    "attempts": attempts,
                    "keyspace": keyspace,
                    "current_candidate": word,
                    "elapsed": elapsed,
                    "attempts_per_second": int(attempts / elapsed) if elapsed > 0 else 0,
                    "found": False
                }
                # Let asyncio context yield
                time.sleep(0.001)

    # Finished and not found
    elapsed = time.time() - start_time
    yield {
        "attempts": attempts,
        "keyspace": keyspace,
        "current_candidate": "",
        "elapsed": elapsed,
        "attempts_per_second": int(attempts / elapsed) if elapsed > 0 else 0,
        "found": False,
        "plaintext": None
    }
