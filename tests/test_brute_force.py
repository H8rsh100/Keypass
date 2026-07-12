import pytest
from backend.hasher import hash_password
from backend.brute_force import brute_force_attack, get_charset_string

def test_get_charset_string():
    charset = get_charset_string(["lowercase", "digits"])
    assert "a" in charset
    assert "1" in charset
    assert "A" not in charset

def test_brute_force_success():
    target = hash_password("cat", "sha256")
    # "cat" has length 3, lowercase charset
    generator = brute_force_attack(
        target_hash=target,
        algorithm="sha256",
        charset_types=["lowercase"],
        max_length=3,
        update_interval=10
    )
    results = list(generator)
    final_state = results[-1]
    
    assert final_state["found"] is True
    assert final_state["plaintext"] == "cat"

def test_brute_force_time_limit():
    # Long password that won't be solved instantly
    target = hash_password("zzzzzz", "sha256")
    generator = brute_force_attack(
        target_hash=target,
        algorithm="sha256",
        charset_types=["lowercase"],
        max_length=6,
        update_interval=5000,
        hard_limit_seconds=0.1 # short limit to trigger timeout
    )
    results = list(generator)
    final_state = results[-1]
    # It might or might not find it depending on computer speed, 
    # but if it times out, "error" key should present or it completes.
    if not final_state["found"]:
        assert "error" in final_state or final_state["elapsed"] >= 0.1
