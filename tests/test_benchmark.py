import pytest
from backend.benchmark import calculate_entropy, run_benchmark

def test_calculate_entropy_weak():
    # weak lowercase word
    res = calculate_entropy("hello")
    assert res["strength"] == "very_weak"
    assert res["pool_size"] == 26
    assert res["entropy_bits"] > 0

def test_calculate_entropy_strong():
    # Strong mixed-case alphanumeric symbol password
    res = calculate_entropy("S3cur3P@ssw0rd!#")
    assert res["strength"] in ["strong", "very_strong"]
    assert res["pool_size"] > 26

def test_run_benchmark():
    # Test benchmarking with a common password "monkey"
    # Ensure it finishes quickly and gives dictionary + rainbow table success
    benchmark_res = run_benchmark("monkey", "sha256")
    
    assert benchmark_res["password"] == "monkey"
    assert benchmark_res["algorithm"] == "sha256"
    assert "entropy" in benchmark_res
    assert benchmark_res["rainbow_table"]["cracked"] is True
    assert benchmark_res["dictionary"]["cracked"] is True
