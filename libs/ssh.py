from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization


def generate_ad25519_key_pair(secret):
    privkey_bytes = Ed25519PrivateKey.from_private_bytes(secret)
    
    nondeterministic_privatekey = privkey_bytes.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()
    nondeterministic_bytes = b64decode(''.join(nondeterministic_privatekey.split('\n')[1:-2]))
    # handle random 32bit number, occuring twice in a row
    deterministic_bytes = nondeterministic_bytes[:98] + b'00000000' + nondeterministic_bytes[106:]
    deterministic_privatekey = '\n'.join([
        '-----BEGIN OPENSSH PRIVATE KEY-----',
        b64encode(deterministic_bytes).decode(),
        '-----END OPENSSH PRIVATE KEY-----',
    ])

    public_key = privkey_bytes.public_key().public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH,
    ).decode()
    return (deterministic_privatekey, public_key)
