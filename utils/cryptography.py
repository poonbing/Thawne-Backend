
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
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
    data = data.encode('utf-8')
    key = hashlib.sha256(key.encode('utf-8')).digest()
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    encrypted = base64.b64encode(cipher.nonce + tag + ciphertext)
    encrypted_data = encrypted.decode('utf-8')
    return encrypted_data


def decrypt_data(encrypted_data, key):
    encrypted = encrypted_data.encode('utf-8')
    cipher_object = base64.b64decode(encrypted)
    nonce = cipher_object[:16]
    tag = cipher_object[16:32]
    ciphertext = cipher_object[32:]
    key = hashlib.sha256(key.encode('utf-8')).digest()
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    print(decrypt_data)
    return decrypted_data.decode('utf-8')

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