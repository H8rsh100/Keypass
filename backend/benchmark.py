import time
import math
from typing import Dict, Any, List
from backend.hasher import hash_password
from backend.dictionary_attack import dictionary_attack
from backend.brute_force import brute_force_attack, get_charset_string
from backend.rainbow_table import lookup_hash

def calculate_entropy(password: str) -> Dict[str, Any]:
    """
    Calculates password entropy in bits and estimates real-world cracking speed.
    Formula: Entropy = length * log2(pool_size)
    """
    length = len(password)
    if length == 0:
        return {
            "entropy_bits": 0.0,
            "pool_size": 0,
            "pool_description": "none",
            "combinations": 0,
            "estimated_crack_time_seconds": 0.0,
            "strength": "very_weak"
        }

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not (c.isalnum() or c.isspace()) for c in password)

    pool_size = 0
    pool_desc = []
    if has_lower:
        pool_size += 26
        pool_desc.append("lowercase")
    if has_upper:
        pool_size += 26
        pool_desc.append("uppercase")
    if has_digit:
        pool_size += 10
        pool_desc.append("digits")
    if has_symbol:
        pool_size += 32  # standard ASCII symbols count
        pool_desc.append("symbols")

    if pool_size == 0:
        pool_size = 26
        pool_desc.append("lowercase (default)")

    entropy = length * math.log2(pool_size)
    combinations = pool_size ** length

    # Estimate time to crack at 100 million hashes/sec (100 MH/s - standard GPU)
    hash_rate = 100_000_000
    estimated_seconds = combinations / hash_rate

    # Determine strength level
    if entropy < 28:
        strength = "very_weak"
    elif entropy < 36:
        strength = "weak"
    elif entropy < 60:
        strength = "medium"
    elif entropy < 80:
        strength = "strong"
    else:
        strength = "very_strong"

    return {
        "entropy_bits": round(entropy, 2),
        "pool_size": pool_size,
        "pool_description": ", ".join(pool_desc),
        "combinations": combinations,
        "estimated_crack_time_seconds": estimated_seconds,
        "strength": strength
    }

def run_benchmark(password: str, algorithm: str) -> Dict[str, Any]:
    """
    Runs rainbow table lookup, dictionary attack, and a safe/short brute-force
    attempt to compare their effectiveness and execution times.
    """
    target_hash = hash_password(password, algorithm)
    entropy_info = calculate_entropy(password)
    
    results = {
        "password": password,
        "algorithm": algorithm,
        "hash": target_hash,
        "entropy": entropy_info,
        "rainbow_table": {"cracked": False, "time_taken": 0.0, "message": ""},
        "dictionary": {"cracked": False, "time_taken": 0.0, "attempts": 0},
        "brute_force": {"cracked": False, "time_taken": 0.0, "attempts": 0, "status": ""}
    }

    # 1. Rainbow Table (Instant)
    start = time.time()
    rt_match = lookup_hash(target_hash, algorithm)
    results["rainbow_table"]["time_taken"] = time.time() - start
    if rt_match:
        results["rainbow_table"]["cracked"] = True
        results["rainbow_table"]["message"] = "Found in SQLite index"
    else:
        results["rainbow_table"]["message"] = "Not in table"

    # 2. Dictionary Attack
    start = time.time()
    dict_gen = dictionary_attack(target_hash, algorithm, update_interval=1000)
    dict_results = list(dict_gen)
    results["dictionary"]["time_taken"] = time.time() - start
    if dict_results:
        final_dict = dict_results[-1]
        results["dictionary"]["cracked"] = final_dict.get("found", False)
        results["dictionary"]["attempts"] = final_dict.get("attempts", 0)

    # 3. Brute Force (Safe - maximum length 4, max 5 seconds)
    # We use all charset pools matching the password characters to be fair
    charset_types = []
    if any(c.islower() for c in password): charset_types.append("lowercase")
    if any(c.isupper() for c in password): charset_types.append("uppercase")
    if any(c.isdigit() for c in password): charset_types.append("digits")
    if any(not (c.isalnum() or c.isspace()) for c in password): charset_types.append("symbols")
    if not charset_types:
        charset_types = ["lowercase"]

    start = time.time()
    # Capped at length 4 and max 2 seconds for benchmark execution speed
    bf_gen = brute_force_attack(
        target_hash=target_hash,
        algorithm=algorithm,
        charset_types=charset_types,
        max_length=min(len(password), 4),
        update_interval=10000,
        hard_limit_seconds=2.0
    )
    bf_results = list(bf_gen)
    results["brute_force"]["time_taken"] = time.time() - start
    if bf_results:
        final_bf = bf_results[-1]
        results["brute_force"]["cracked"] = final_bf.get("found", False)
        results["brute_force"]["attempts"] = final_bf.get("attempts", 0)
        if "error" in final_bf:
            results["brute_force"]["status"] = "timed_out"
        elif final_bf.get("found", False):
            results["brute_force"]["status"] = "cracked"
        else:
            results["brute_force"]["status"] = "exhausted"

    return results
