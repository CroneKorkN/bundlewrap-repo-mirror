"""rsa: deterministic RSA private-key generation backed by a seeded PRNG, cached on disk."""

# https://stackoverflow.com/a/18266970

from base64 import urlsafe_b64encode
from Crypto.PublicKey import RSA
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.serialization import load_der_private_key
from functools import cache
from hashlib import sha256, sha3_512
from os import replace
from pathlib import Path
from struct import pack
from tempfile import NamedTemporaryFile

# generating a 2048 bit key takes about a second, every metadata build of the mail server needs several
CACHE_DIR = Path(__file__).resolve().parent.parent / '.cache' / 'rsa'


class PRNG(object):
    def __init__(self, seed):
        self.index = 0
        self.seed = sha3_512(seed).digest()
        self.buffer = b""
    def __call__(self, n):
        while len(self.buffer) < n:
            self.buffer += sha3_512(self.seed + pack("<d", self.index)).digest()
            self.index += 1
        result, self.buffer = self.buffer[:n], self.buffer[n:]
        return result


def _generate_deterministic_rsa_private_key(secret_bytes):
    return RSA.generate(2048, randfunc=PRNG(secret_bytes)).export_key('DER')


def _cached_der(secret_bytes):
    """The key as DER, from the cache when possible.

    The file name and the encryption key both derive from the secret, so the cache neither
    reveals it nor holds a private key in plaintext; whoever can decrypt it could regenerate the key anyway.
    """
    path = CACHE_DIR / sha256(b'name' + secret_bytes).hexdigest()
    fernet = Fernet(urlsafe_b64encode(sha256(b'key' + secret_bytes).digest()))

    try:
        return fernet.decrypt(path.read_bytes())
    except (FileNotFoundError, InvalidToken):
        pass

    der = _generate_deterministic_rsa_private_key(secret_bytes)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    # atomic, bundlewrap builds metadata in several threads
    with NamedTemporaryFile(dir=CACHE_DIR, delete=False) as tmp:
        tmp.write(fernet.encrypt(der))
    replace(tmp.name, path)
    return der


@cache
def generate_deterministic_rsa_private_key(secret_bytes):
    return load_der_private_key(
        _cached_der(secret_bytes),
        password=None,
        # generated here or decrypted with authentication, the consistency check costs ~65 ms per key
        unsafe_skip_rsa_key_validation=True,
    )
