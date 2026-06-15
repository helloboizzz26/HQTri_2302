import os
import rsa

class RSACipher:
    def __init__(self):
        self.key_dir = os.path.join(os.path.dirname(__file__), 'key')
        os.makedirs(self.key_dir, exist_ok=True)
        self.pub_key_path = os.path.join(self.key_dir, 'public.pem')
        self.priv_key_path = os.path.join(self.key_dir, 'private.pem')

    def generate_keys(self):
        (pubkey, privkey) = rsa.newkeys(1024)
        with open(self.pub_key_path, 'wb') as f:
            f.write(pubkey.save_pkcs1())
        with open(self.priv_key_path, 'wb') as f:
            f.write(privkey.save_pkcs1())

    def load_keys(self):
        if not os.path.exists(self.pub_key_path) or not os.path.exists(self.priv_key_path):
            self.generate_keys()
        
        with open(self.pub_key_path, 'rb') as f:
            pub_data = f.read()
            pubkey = rsa.PublicKey.load_pkcs1(pub_data)
            
        with open(self.priv_key_path, 'rb') as f:
            priv_data = f.read()
            privkey = rsa.PrivateKey.load_pkcs1(priv_data)
            
        return privkey, pubkey

    def encrypt(self, message, key):
        if isinstance(message, str):
            message = message.encode('utf-8')
        # Python-rsa encrypt expects PublicKey. If for some reason PrivateKey is supplied,
        # we raise ValueError.
        if not isinstance(key, rsa.PublicKey):
            raise ValueError("RSA encryption requires the public key.")
        return rsa.encrypt(message, key)

    def decrypt(self, ciphertext, key):
        if not isinstance(key, rsa.PrivateKey):
            raise ValueError("RSA decryption requires the private key.")
        decrypted_bytes = rsa.decrypt(ciphertext, key)
        return decrypted_bytes.decode('utf-8')

    def sign(self, message, private_key):
        if isinstance(message, str):
            message = message.encode('utf-8')
        return rsa.sign(message, private_key, 'SHA-256')

    def verify(self, message, signature, public_key):
        if isinstance(message, str):
            message = message.encode('utf-8')
        try:
            rsa.verify(message, signature, public_key)
            return True
        except rsa.VerificationError:
            return False