"""
TODO:
- make the data transfer use JSON. This should allow transfer files too.
"""

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

def GenerateKeys():
    key = RSA.generate(2048)
    privateKey = key.export_key()
    publicKey = key.publickey().export_key()

    with open(r"rsa_keys\private.pem", "wb") as out_file:
        out_file.write(privateKey)

    with open(r"rsa_keys\public.pem", "wb") as out_file:
        out_file.write(publicKey)

def Encrypt(public_key=None, data=None):
    recipient_key = RSA.import_key(open(public_key).read())
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data.encode("utf-8"))

    return enc_session_key, cipher_aes.nonce, tag, ciphertext

def Decrypt(private_key=None, enc_session_key=None, nonce=None, tag=None, encrypted_data=None):
    receiver_key = RSA.import_key(open(private_key).read())

    # Decrypt session key with private RSA key
    cipher_rsa = PKCS1_OAEP.new(receiver_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = (cipher_aes.decrypt_and_verify(encrypted_data, tag)).decode("utf-8")

    return data

enc_session_key, nonce, tag, ciphertext = Encrypt(public_key=r"rsa_keys\public.pem", data="Hello World!")
data = Decrypt(private_key=r"rsa_keys\private.pem", enc_session_key=enc_session_key, nonce=nonce, tag=tag, encrypted_data=ciphertext)

print(data)
