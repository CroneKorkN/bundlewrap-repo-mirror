import base64
from nacl.public import PrivateKey
from nacl.encoding import Base64Encoder
from bundlewrap.utils import Fault

def gen_privkey(repo, identifier):
    return repo.vault.random_bytes_as_base64_for(identifier)

def get_pubkey_from_privkey(identifier, privkey):
    # FIXME this assumes the privkey is always a base64 encoded string
    def derive_pubkey():
        pub_key = PrivateKey(base64.b64decode(str(privkey))).public_key
        return pub_key.encode(encoder=Base64Encoder).decode('ascii')

    return Fault(f'pubkey from privkey {identifier}', derive_pubkey)
