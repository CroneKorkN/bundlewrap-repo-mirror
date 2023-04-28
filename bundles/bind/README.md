## DNSSEC

https://wiki.debian.org/DNSSEC%20Howto%20for%20BIND%209.9+#The_signing_part
https://blog.apnic.net/2021/11/02/dnssec-provisioning-automation-with-cds-cdnskey-in-the-real-world/
https://gist.github.com/wido/4c6288b2f5ba6d16fce37dca3fc2cb4a

```python
import dns.dnssec
algorithm = dns.dnssec.RSASHA256
```

```python
import cryptography
pk = cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key(key_size=2048, public_exponent=65537)
```

## Nomenclature

### parent

DNSKEY:
  the public key

DS


