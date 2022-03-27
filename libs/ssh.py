from base64 import b64decode, b64encode
from hashlib import sha3_224, sha1
from functools import cache
import hmac

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption


@cache
def generate_ed25519_key_pair(secret):
    privkey_bytes = Ed25519PrivateKey.from_private_bytes(secret)

    # PRIVATE KEY
    
    nondeterministic_privatekey = privkey_bytes.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.OpenSSH,
        encryption_algorithm=NoEncryption()
    ).decode()

    # get relevant lines from string
    nondeterministic_bytes = b64decode(''.join(nondeterministic_privatekey.split('\n')[1:-2]))
    
    # sanity check
    if nondeterministic_bytes[98:102] != nondeterministic_bytes[102:106]:
        raise Exception("checksums should be the same: whats going on here?")
    
    # replace random bytes with deterministic values
    random_bytes = sha3_224(secret).digest()[0:4]
    deterministic_bytes = nondeterministic_bytes[:98] + random_bytes + random_bytes + nondeterministic_bytes[106:]
    
    # reassemble file
    deterministic_privatekey = '\n'.join([
        '-----BEGIN OPENSSH PRIVATE KEY-----',
        b64encode(deterministic_bytes).decode(),
        '-----END OPENSSH PRIVATE KEY-----',
    ])

    # PUBLIC KEY

    public_key = privkey_bytes.public_key().public_bytes(
        encoding=Encoding.OpenSSH,
        format=PublicFormat.OpenSSH,
    ).decode()
    
    # RETURN
    
    return (deterministic_privatekey, public_key)


#https://www.fragmentationneeded.net/2017/10/ssh-hashknownhosts-file-format.html
# test this:
# - `ssh-keyscan -H 10.0.0.5`
# - take the salt from the ssh-ed25519 entry (first field after '|1|')
# - `bw debug -c 'repo.libs.ssh.known_hosts_entry_for(repo.get_node(<node with hostname 10.0.0.5>), <salt from ssh-keygen>)'`
@cache
def known_hosts_entry_for(node, test_salt=None):
    lines = set()

    for hostname in sorted(node.metadata.get('ssh/hostnames')):
        if test_salt:
            salt = b64decode(test_salt)
        else:
            salt = sha1((node.metadata.get('id') + hostname).encode()).digest()

        hash = hmac.new(salt, hostname.encode(), sha1).digest()
        pubkey = node.metadata.get('ssh/host_key/public')
        
        lines.add(f'|1|{b64encode(salt).decode()}|{b64encode(hash).decode()} {" ".join(pubkey.split()[:2])}')
        
    return '\n'.join(sorted(lines))
