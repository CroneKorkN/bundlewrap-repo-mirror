from base64 import standard_b64encode
from hashlib import pbkdf2_hmac, sha256
import hmac


def b64enc(b: bytes) -> str:
    return standard_b64encode(b).decode('utf8')

def generate_scram_sha_256(password, salt):
    if len(salt) != 16:
        raise ValueError(f"Salt '{salt}' is not 16, but {len(salt)} characters long.")

    digest_len = 32
    iterations = 4096

    digest_key = pbkdf2_hmac('sha256', password.encode('utf8'), salt, iterations, digest_len)
    client_key = hmac.digest(digest_key, 'Client Key'.encode('utf8'), 'sha256')
    stored_key = sha256(client_key).digest()
    server_key = hmac.digest(digest_key, 'Server Key'.encode('utf8'), 'sha256')

    return f'SCRAM-SHA-256${iterations}:{b64enc(salt)}${b64enc(stored_key)}:{b64enc(server_key)}'


