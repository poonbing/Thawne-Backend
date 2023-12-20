import uuid
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import os
import base64
import bcrypt


def generate_salt():
    return bcrypt.gensalt(12)


def derive_key(
    password, salt, iterations=100000, key_length=32, hash_algorithm="sha256"
):
    key = hashlib.pbkdf2_hmac(
        hash_algorithm, password.encode("utf-8"), salt, iterations, dklen=key_length
    )
    return key


def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode("utf-8"))
    return cipher.nonce + tag + ciphertext


def decrypt_data(encrypted_data, key):
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data.decode("utf-8")
