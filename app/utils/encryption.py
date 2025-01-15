from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from os import urandom
import base64

def encrypt_data(data, master_password):
    salt = urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    key = kdf.derive(master_password.encode())

    iv = urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()

    return base64.b64encode(salt + iv + encryptor.tag + encrypted_data).decode()

def decrypt_data(encoded_data, master_password):
    encoded_data = base64.b64decode(encoded_data)

    salt = encoded_data[:16]
    iv = encoded_data[16:32]
    tag = encoded_data[32:48]
    data = encoded_data[48:]

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    key = kdf.derive(master_password.encode())

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(data) + decryptor.finalize()

    return decrypted_data.decode()
