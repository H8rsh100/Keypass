import pytest
from backend.hasher import hash_password, verify_password

def test_md5_hashing():
    password = "password123"
    # Expected MD5 hash for "password123" is 482c811da5d5b4bc6d497ffa98491e38
    expected = "482c811da5d5b4bc6d497ffa98491e38"
    hashed = hash_password(password, "md5")
    assert hashed == expected
    assert verify_password(password, hashed, "md5") is True
    assert verify_password("wrongpassword", hashed, "md5") is False

def test_sha1_hashing():
    password = "password123"
    # Expected SHA-1 hash for "password123" is cbfdac6008f9cab4083784cbd1874f76618d2a97
    expected = "cbfdac6008f9cab4083784cbd1874f76618d2a97"
    hashed = hash_password(password, "sha1")
    assert hashed == expected
    assert verify_password(password, hashed, "sha1") is True
    assert verify_password("wrongpassword", hashed, "sha1") is False

def test_sha256_hashing():
    password = "password123"
    # Expected SHA-256 hash for "password123" is ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
    expected = "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"
    hashed = hash_password(password, "sha256")
    assert hashed == expected
    assert verify_password(password, hashed, "sha256") is True
    assert verify_password("wrongpassword", hashed, "sha256") is False

def test_bcrypt_hashing():
    password = "password123"
    hashed = hash_password(password, "bcrypt")
    # Bcrypt hashes generate random salts, so we verify by using verify_password
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")
    assert verify_password(password, hashed, "bcrypt") is True
    assert verify_password("wrongpassword", hashed, "bcrypt") is False

def test_bcrypt_custom_rounds():
    password = "password123"
    # test with minimum cost factor for speed in tests
    hashed = hash_password(password, "bcrypt", bcrypt_rounds=4)
    # The cost factor is encoded in the 3rd sub-field of the bcrypt hash, e.g. $2b$04$
    assert hashed.startswith("$2b$04$") or hashed.startswith("$2a$04$")
    assert verify_password(password, hashed, "bcrypt") is True

def test_unsupported_algorithm():
    with pytest.raises(ValueError):
        hash_password("hello", "sha512")
    with pytest.raises(ValueError):
        verify_password("hello", "hash", "sha512")
