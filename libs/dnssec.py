# https://medium.com/iocscan/how-dnssec-works-9c652257be0
# https://de.wikipedia.org/wiki/RRSIG_Resource_Record
# https://metebalci.com/blog/a-minimum-complete-tutorial-of-dnssec/
# https://bind9.readthedocs.io/en/latest/dnssec-guide.html

from sys import argv
from os.path import realpath, dirname
from bundlewrap.repo import Repository
from base64 import b64decode, urlsafe_b64encode
from cryptography.utils import int_to_bytes
from cryptography.hazmat.primitives import serialization as crypto_serialization
from struct import pack, unpack
from hashlib import sha1, sha256


def long_to_base64(n):
    return urlsafe_b64encode(int_to_bytes(n, None)).decode()

flags = 256
protocol = 3
algorithm = 8
algorithm_name = 'RSASHA256'

# ZSK/KSK DNSKEY
#
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateNumbers
# https://crypto.stackexchange.com/a/21104

def generate_signing_key_pair(zone, salt, repo):
    privkey = repo.libs.rsa.generate_deterministic_rsa_private_key(
        b64decode(str(repo.vault.random_bytes_as_base64_for(f'dnssec {salt} ' + zone)))
    )

    public_exponent = privkey.private_numbers().public_numbers.e
    modulo = privkey.private_numbers().public_numbers.n
    private_exponent = privkey.private_numbers().d
    prime1 = privkey.private_numbers().p
    prime2 = privkey.private_numbers().q
    exponent1 = privkey.private_numbers().dmp1
    exponent2 = privkey.private_numbers().dmq1
    coefficient = privkey.private_numbers().iqmp
    flags = 256 if salt == 'zsk' else 257

    dnskey = ''.join(privkey.public_key().public_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode().split('\n')[1:-2])

    return {
        'dnskey': dnskey,
        'dnskey_record': f'{zone}. IN DNSKEY {flags} {protocol} {algorithm} {dnskey}',
        'key_id': _calc_keyid(flags, protocol, algorithm, dnskey),
        'privkey_file': {
            'Private-key-format': 'v1.3',
            'Algorithm': f'{algorithm} ({algorithm_name})',
            'Modulus': long_to_base64(modulo),
            'PublicExponent': long_to_base64(public_exponent),
            'PrivateExponent': long_to_base64(private_exponent),
            'Prime1': long_to_base64(prime1),
            'Prime2': long_to_base64(prime2),
            'Exponent1': long_to_base64(exponent1),
            'Exponent2': long_to_base64(exponent2),
            'Coefficient': long_to_base64(coefficient),
            'Created': 20230428110109,
            'Publish': 20230428110109,
            'Activate': 20230428110109,
        },
    }


# DS
#
# https://gist.github.com/wido/4c6288b2f5ba6d16fce37dca3fc2cb4a#file-dnskey_to_dsrecord-py-L40

def _calc_ds(zone, flags, protocol, algorithm, dnskey):
    if zone.endswith('.') is False:
        zone += '.'

    signature = bytes()
    for i in zone.split('.'):
        signature += pack('B', len(i)) + i.encode()

    signature += pack('!HBB', int(flags), int(protocol), int(algorithm))
    signature += b64decode(dnskey)

    return {
        'sha1':    sha1(signature).hexdigest().upper(),
        'sha256':  sha256(signature).hexdigest().upper(),
    }

def _calc_keyid(flags, protocol, algorithm, dnskey):
    st = pack('!HBB', int(flags), int(protocol), int(algorithm))
    st += b64decode(dnskey)

    cnt = 0
    for idx in range(len(st)):
        s = unpack('B', st[idx:idx+1])[0]
        if (idx % 2) == 0:
            cnt += s << 8
        else:
            cnt += s

    return ((cnt & 0xFFFF) + (cnt >> 16)) & 0xFFFF

def dnskey_to_ds(zone, flags, protocol, algorithm, dnskey, key_id):
    ds = _calc_ds(zone, flags, protocol, algorithm, dnskey)

    return[
        f"{zone}. IN DS {str(key_id)} {str(algorithm)} 1 {ds['sha1'].lower()}",
        f"{zone}. IN DS {str(key_id)} {str(algorithm)} 2 {ds['sha256'].lower()}",
    ]

# Result

def generate_dnssec_for_zone(zone, node):
    zsk_data = generate_signing_key_pair(zone, salt='zsk', repo=node.repo)
    ksk_data = generate_signing_key_pair(zone, salt='ksk', repo=node.repo)
    ds_records = dnskey_to_ds(zone, flags, protocol, algorithm, ksk_data['dnskey'], ksk_data['key_id'])

    return {
        'zsk_data': zsk_data,
        'ksk_data': ksk_data,
        'ds_records': ds_records,
    }
