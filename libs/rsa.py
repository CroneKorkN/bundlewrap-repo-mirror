# https://stackoverflow.com/a/18266970

from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.serialization import load_der_private_key
from functools import cache
from subprocess import check_output
from os.path import join


@cache
def generate_deterministic_rsa_private_key(repo_path, secret_bytes):
    privkey_der = check_output([
        join(repo_path, 'bin', 'deterministic_rsa_privkey'),
        '2048',
        b64encode(secret_bytes),
    ])

    return load_der_private_key(
        b64decode(privkey_der),
        password=None,
    )
