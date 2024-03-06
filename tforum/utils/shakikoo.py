# Credits to aiotfm: https://github.com/Athesdrake/aiotfm

import base64
import hashlib

SALT = bytes((
    0xf7, 0x1a, 0xa6, 0xde, 0x8f, 0x17, 0x76, 0xa8, 0x03, 0x9d, 0x32, 0xb8, 0xa1, 0x56, 0xb2, 0xa9,
    0x3e, 0xdd, 0x43, 0x9d, 0xc5, 0xdd, 0xce, 0x56, 0xd3, 0xb7, 0xa4, 0x05, 0x4a, 0x0d, 0x08, 0xb0
))


def shakikoo(string):
    """Encrypt a password with the SHAKikoo algorithm."""
    sha256 = hashlib.sha256(string.encode())  # hash the password with SHA256
    hex256 = sha256.hexdigest().encode()  # convert it into hexdecamals
    hex256 += SALT  # salt it

    hashed = hashlib.sha256(hex256).digest()  # re-hash it
    return base64.b64encode(hashed)  # return it in base64 bytes
