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
    key = hashlib.sha256(key.encode('utf-8')).digest()[:16]
    print(key)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode("utf-8"))
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')


def decrypt_data(encrypted_data, key):
    key = hashlib.sha256(key.encode('utf-8')).digest()[:16]
    encrypted_data = base64.b64decode(encrypted_data.encode('utf-8'))
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data.decode("utf-8")

def sha256_hash_bytes(input_string):
    input_bytes = input_string.encode('utf-8')
    sha256_hash_obj = hashlib.sha256()
    sha256_hash_obj.update(input_bytes)
    hashed_bytes = sha256_hash_obj.digest()
    return hashed_bytes

def generate_key(user_id, password):
    salt = sha256_hash_bytes(user_id)[:32]
    key_bytes = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    key = base64.b64encode(key_bytes).decode('utf-8')
    return key