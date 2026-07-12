import pytest
import os
from backend.hasher import hash_password
from backend.rainbow_table import precompute_rainbow_table, lookup_hash, DB_PATH

def test_rainbow_table_lifecycle():
    # Run the precomputation generator to build the SQLite database
    generator = precompute_rainbow_table()
    results = list(generator)
    
    # Confirm the last step completed successfully
    assert results[-1]["status"] == "complete"
    assert os.path.exists(DB_PATH)

    # Let's perform some lookups
    # 1. "letmein" is a common password
    hash_md5 = hash_password("letmein", "md5")
    hash_sha256 = hash_password("letmein", "sha256")
    
    assert lookup_hash(hash_md5, "md5") == "letmein"
    assert lookup_hash(hash_sha256, "sha256") == "letmein"

    # 2. Lookup non-existent hash
    assert lookup_hash("nonexistenthashvalue", "sha256") is None
