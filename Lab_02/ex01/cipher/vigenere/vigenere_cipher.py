class VigenereCipher:
    @staticmethod
    def _validate_key(key: str) -> str:
        if not isinstance(key, str) or not key.strip():
            raise ValueError("Khóa không được để trống.")

        normalized_key = key.strip()
        if not normalized_key.isascii() or not normalized_key.isalpha():
            raise ValueError("Khóa chỉ được chứa chữ cái A-Z.")

        return normalized_key.upper()

    @staticmethod
    def _is_ascii_letter(char: str) -> bool:
        return char.isascii() and char.isalpha()

    def vigenere_encrypt(self, plain_text, key):
        normalized_key = self._validate_key(key)
        encrypted_text = []
        key_index = 0

        for char in plain_text:
            if self._is_ascii_letter(char):
                key_shift = ord(normalized_key[key_index % len(normalized_key)]) - ord("A")

                if char.isupper():
                    encrypted_text.append(chr((ord(char) - ord("A") + key_shift) % 26 + ord("A")))
                else:
                    encrypted_text.append(chr((ord(char) - ord("a") + key_shift) % 26 + ord("a")))

                key_index += 1
            else:
                encrypted_text.append(char)

        return "".join(encrypted_text)

    def vigenere_decrypt(self, encrypted_text, key):
        normalized_key = self._validate_key(key)
        decrypted_text = []
        key_index = 0

        for char in encrypted_text:
            if self._is_ascii_letter(char):
                key_shift = ord(normalized_key[key_index % len(normalized_key)]) - ord("A")

                if char.isupper():
                    decrypted_text.append(chr((ord(char) - ord("A") - key_shift) % 26 + ord("A")))
                else:
                    decrypted_text.append(chr((ord(char) - ord("a") - key_shift) % 26 + ord("a")))

                key_index += 1
            else:
                decrypted_text.append(char)

        return "".join(decrypted_text)
