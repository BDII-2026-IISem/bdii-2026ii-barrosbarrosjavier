import hashlib
import secrets


def generate_refresh_value():
    """Genera un refresh token opaco (no JWT) usando secrets."""
    return secrets.token_urlsafe(48)


def hash_token(raw_token):
    """Devuelve el hash SHA-256 en hexadecimal del refresh en claro."""
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
