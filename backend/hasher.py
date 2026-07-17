import hashlib
import bcrypt

def hash_password(password: str, algorithm: str, bcrypt_rounds: int = 12) -> str:
    """
    Hashes a password string using the specified algorithm.
    Supported algorithms: md5, sha1, sha256, bcrypt
    """
    algo = algorithm.lower()
    password_bytes = password.encode('utf-8')

    if algo == 'md5':
        return hashlib.md5(password_bytes).hexdigest()
    elif algo == 'sha1':
        return hashlib.sha1(password_bytes).hexdigest()
    elif algo == 'sha256':
        return hashlib.sha256(password_bytes).hexdigest()
    elif algo == 'bcrypt':
        # Generate a salt with custom cost factor and hash the password
        salt = bcrypt.gensalt(rounds=bcrypt_rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    else:
        raise ValueError(f"Unsupported hashing algorithm: {algorithm}")

def verify_password(password: str, hashed: str, algorithm: str) -> bool:
    """
    Verifies a plaintext password against a hash using the specified algorithm.
    """
    algo = algorithm.lower()
    password_bytes = password.encode('utf-8')

    if algo in ['md5', 'sha1', 'sha256']:
        # For standard hashes, re-compute and compare
        computed = hash_password(password, algo)
        return computed == hashed.lower()
    elif algo == 'bcrypt':
        # For bcrypt, use the library's checkpw function
        try:
            hashed_bytes = hashed.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception:
            return False
    else:
        raise ValueError(f"Unsupported hashing algorithm: {algorithm}")
