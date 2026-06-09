import os
import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# secp256k1 curve parameters
P = 2**256 - 2**32 - 977
A = 0
B = 7
Gx = 55072459820054705922899322147341382244039050585141943881583130777579453888772
Gy = 32670510020758816978083085130507043184471273380659243275938901209192513626190
G = (Gx, Gy)
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337

def mod_inv(n, p):
    return pow(n, p - 2, p)

def point_add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and y1 != y2:
        return None
    if x1 == x2:
        m = (3 * x1 * x1 + A) * mod_inv(2 * y1, P)
    else:
        m = (y2 - y1) * mod_inv(x2 - x1, P)
    x3 = (m * m - x1 - x2) % P
    y3 = (m * (x1 - x3) - y1) % P
    return (x3, y3)

def point_mult(k, point):
    R = None
    Q = point
    while k > 0:
        if k & 1:
            R = point_add(R, Q)
        Q = point_add(Q, Q)
        k >>= 1
    return R

class ECCCipher:
    def __init__(self):
        self.key_dir = os.path.join(os.path.dirname(__file__), 'key')
        os.makedirs(self.key_dir, exist_ok=True)
        self.pub_key_path = os.path.join(self.key_dir, 'public_key.txt')
        self.priv_key_path = os.path.join(self.key_dir, 'private_key.txt')

    def generate_keys(self):
        priv_key = random.randint(1, N - 1)
        pub_key = point_mult(priv_key, G)
        
        with open(self.priv_key_path, 'w') as f:
            f.write(str(priv_key))
        with open(self.pub_key_path, 'w') as f:
            f.write(f"{pub_key[0]},{pub_key[1]}")
            
        return priv_key, pub_key

    def load_keys(self):
        if not os.path.exists(self.pub_key_path) or not os.path.exists(self.priv_key_path):
            self.generate_keys()
        
        with open(self.priv_key_path, 'r') as f:
            priv_key = int(f.read().strip())
            
        with open(self.pub_key_path, 'r') as f:
            parts = f.read().strip().split(',')
            pub_key = (int(parts[0]), int(parts[1]))
            
        return priv_key, pub_key

    def encrypt(self, message, pub_key):
        if isinstance(message, str):
            message = message.encode('utf-8')
            
        k = random.randint(1, N - 1)
        R = point_mult(k, G)
        S = point_mult(k, pub_key)
        
        if S is None:
            raise ValueError("Shared secret computation failed (point at infinity). Try again.")
            
        # Derive AES key from shared secret x coordinate
        secret_x = S[0]
        aes_key = hashlib.sha256(str(secret_x).encode('utf-8')).digest()
        
        # AES-CBC encrypt
        cipher = AES.new(aes_key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message, AES.block_size))
        
        # Ciphertext format: R_x (hex), R_y (hex), IV + Encrypted Data (hex)
        iv_and_ct = cipher.iv + ciphertext
        return {
            "R_x": hex(R[0]),
            "R_y": hex(R[1]),
            "ciphertext": iv_and_ct.hex()
        }

    def decrypt(self, data, priv_key):
        R = (int(data["R_x"], 16), int(data["R_y"], 16))
        iv_and_ct = bytes.fromhex(data["ciphertext"])
        
        S = point_mult(priv_key, R)
        if S is None:
            raise ValueError("Decryption failed (shared secret point is at infinity).")
            
        secret_x = S[0]
        aes_key = hashlib.sha256(str(secret_x).encode('utf-8')).digest()
        
        iv = iv_and_ct[:AES.block_size]
        ct = iv_and_ct[AES.block_size:]
        
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_bytes = unpad(cipher.decrypt(ct), AES.block_size)
        return decrypted_bytes.decode('utf-8')
