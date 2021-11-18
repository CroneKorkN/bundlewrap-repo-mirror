import bcrypt
from base64 import b64decode, b64encode
from binascii import hexlify
from hashlib import sha3_256

def line(user, pw, salt, repo):
    full_salt = str(repo.vault.password_for(user+pw+salt))
    sha = sha3_256(full_salt.encode()).digest()
    sha_base64 = b64encode(sha)[0:22]
    salt_string = f"$2b$10${sha_base64.decode().replace('+', '.')}"
    print(sha, sha_base64, salt_string)
    hash = bcrypt.hashpw(
        pw.encode(),
        salt_string.encode()
    ).decode()

    return f'{user}:{hash}'
