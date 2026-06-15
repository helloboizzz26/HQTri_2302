import math


class TranspositionCipher:
    @staticmethod
    def _validate_key(key):
        if key < 1:
            raise ValueError("Khóa phải lớn hơn hoặc bằng 1.")

        return key

    def encrypt(self, text, key):
        key = self._validate_key(key)
        encrypted_text = ""

        for col in range(key):
            pointer = col
            while pointer < len(text):
                encrypted_text += text[pointer]
                pointer += key

        return encrypted_text

    def decrypt(self, text, key):
        key = self._validate_key(key)
        num_columns = math.ceil(len(text) / float(key))
        num_rows = key
        num_shaded_boxes = (num_columns * num_rows) - len(text)

        decrypted_text = [""] * num_columns
        row, col = 0, 0

        for symbol in text:
            decrypted_text[col] += symbol
            col += 1

            if col == num_columns or (
                col == num_columns - 1 and row >= num_rows - num_shaded_boxes
            ):
                col = 0
                row += 1

        return "".join(decrypted_text)
