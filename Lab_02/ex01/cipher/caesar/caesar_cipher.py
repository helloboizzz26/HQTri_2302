from .alphabet import ALPHABET


class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET

    def _shift_char(self, char: str, key: int) -> str:
        upper_char = char.upper()
        if upper_char not in self.alphabet:
            return char

        letter_index = self.alphabet.index(upper_char)
        output_index = (letter_index + key) % len(self.alphabet)
        output_letter = self.alphabet[output_index]
        return output_letter if char.isupper() else output_letter.lower()

    def encrypt_text(self, text: str, key: int) -> str:
        encrypted_text = []

        for letter in text:
            encrypted_text.append(self._shift_char(letter, key))

        return "".join(encrypted_text)

    def decrypt_text(self, text: str, key: int) -> str:
        return self.encrypt_text(text, -key)
