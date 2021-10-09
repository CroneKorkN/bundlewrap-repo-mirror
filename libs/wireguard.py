import base64
from nacl.public import PrivateKey
from nacl.encoding import Base64Encoder

def privkey(id):
    return str(repo.vault.random_bytes_as_base64_for(f"wireguard privkey {id}"))

def pubkey(id):
    return PrivateKey(base64.b64decode(privkey(id))).public_key.encode(encoder=Base64Encoder).decode('ascii')
    
def psk(id1, id2):
    return repo.vault.random_bytes_as_base64_for(f"wireguard psk {' '.join(sorted([id1, id2]))}")
