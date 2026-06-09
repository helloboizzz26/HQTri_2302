class PlayFairCipher:
    @staticmethod
    def _normalize_key(key):
        normalized_key = "".join(char for char in key.upper() if char.isalpha()).replace("J", "I")
        if not normalized_key:
            raise ValueError("Khóa Playfair phải có ít nhất một chữ cái.")

        unique_key = []
        seen = set()
        for letter in normalized_key:
            if letter not in seen:
                seen.add(letter)
                unique_key.append(letter)

        return unique_key

    @staticmethod
    def _normalize_text(text):
        normalized_text = "".join(char for char in text.upper() if char.isalpha()).replace("J", "I")
        if not normalized_text:
            raise ValueError("Bản rõ hoặc bản mã Playfair phải có ít nhất một chữ cái.")

        return normalized_text

    def create_playfair_matrix(self, key):
        key_letters = self._normalize_key(key)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix = []
        seen = set()

        for letter in key_letters + list(alphabet):
            if letter not in seen:
                seen.add(letter)
                matrix.append(letter)

        return [matrix[i:i + 5] for i in range(0, len(matrix), 5)]

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col

        raise ValueError(f"Không tìm thấy ký tự {letter} trong ma trận Playfair.")

    def _prepare_pairs(self, text):
        normalized_text = self._normalize_text(text)
        pairs = []
        index = 0

        while index < len(normalized_text):
            first_letter = normalized_text[index]
            filler = "Q" if first_letter == "X" else "X"

            if index + 1 >= len(normalized_text):
                second_letter = filler
                index += 1
            else:
                second_letter = normalized_text[index + 1]
                if first_letter == second_letter:
                    second_letter = filler
                    index += 1
                else:
                    index += 2

            pairs.append(first_letter + second_letter)

        return pairs

    def _cleanup_decrypted_text(self, decrypted_text):
        cleaned_text = []
        index = 0

        while index < len(decrypted_text):
            if (
                index + 2 < len(decrypted_text)
                and decrypted_text[index] == decrypted_text[index + 2]
                and decrypted_text[index + 1] == "X"
            ):
                cleaned_text.append(decrypted_text[index])
                index += 2
            else:
                cleaned_text.append(decrypted_text[index])
                index += 1

        if cleaned_text and cleaned_text[-1] == "X":
            cleaned_text.pop()

        return "".join(cleaned_text)

    def playfair_encrypt(self, plain_text, matrix):
        encrypted_text = []

        for pair in self._prepare_pairs(plain_text):
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                encrypted_text.append(matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5])
            elif col1 == col2:
                encrypted_text.append(matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2])
            else:
                encrypted_text.append(matrix[row1][col2] + matrix[row2][col1])

        return "".join(encrypted_text)

    def playfair_decrypt(self, cipher_text, matrix):
        normalized_text = self._normalize_text(cipher_text)
        if len(normalized_text) % 2 != 0:
            normalized_text += "X"

        decrypted_text = []

        for i in range(0, len(normalized_text), 2):
            pair = normalized_text[i:i + 2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text.append(matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5])
            elif col1 == col2:
                decrypted_text.append(matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2])
            else:
                decrypted_text.append(matrix[row1][col2] + matrix[row2][col1])

        return self._cleanup_decrypted_text("".join(decrypted_text))
