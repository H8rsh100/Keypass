import pytest
from backend.hasher import hash_password
from backend.dictionary_attack import dictionary_attack

def test_dictionary_attack_success():
    # "letmein" is a common password on line 11
    target = hash_password("letmein", "sha256")
    generator = dictionary_attack(target, "sha256", update_interval=5)
    
    results = list(generator)
    
    # The last state should indicate it was found
    final_state = results[-1]
    assert final_state["found"] is True
    assert final_state["plaintext"] == "letmein"
    assert final_state["attempts"] > 0

def test_dictionary_attack_failure():
    # Some random password not in the 10k list
    target = hash_password("SuperSecretSecurePassword2026!", "sha256")
    generator = dictionary_attack(target, "sha256", update_interval=1000)
    
    results = list(generator)
    
    final_state = results[-1]
    assert final_state["found"] is False
    assert final_state["plaintext"] is None
