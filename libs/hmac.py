import hmac, hashlib, base64

def hmac_sha512(secret, iv):
    return base64.b64encode(
        hmac.new(
            bytes(iv , 'latin-1'),
            msg=bytes(secret , 'latin-1'),
            digestmod=hashlib.sha512
        ).digest()
    ).decode()
