from base64 import b64decode, b64encode
from hashlib import sha3_224

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption


def generate_ed25519_key_pair(secret):
    privkey_bytes = Ed25519PrivateKey.from_private_bytes(secret)
    
    nondeterministic_privatekey = privkey_bytes.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.OpenSSH,
        encryption_algorithm=NoEncryption()
    ).decode()

    # handle random 32bit number, occuring twice in a row
    nondeterministic_bytes = b64decode(''.join(nondeterministic_privatekey.split('\n')[1:-2]))
    random_bytes = sha3_224(secret).digest()[0:4]
    deterministic_bytes = nondeterministic_bytes[:98] + random_bytes + random_bytes + nondeterministic_bytes[106:]
    deterministic_privatekey = '\n'.join([
        '-----BEGIN OPENSSH PRIVATE KEY-----',
        b64encode(deterministic_bytes).decode(),
        '-----END OPENSSH PRIVATE KEY-----',
    ])

    public_key = privkey_bytes.public_key().public_bytes(
        encoding=Encoding.OpenSSH,
        format=PublicFormat.OpenSSH,
    ).decode()
    
    return (deterministic_privatekey, public_key)
