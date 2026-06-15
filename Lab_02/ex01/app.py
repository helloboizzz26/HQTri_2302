from flask import Flask, render_template, request

from cipher.Transposition import TranspositionCipher
from cipher.caesar import CaesarCipher
from cipher.playfair import PlayFairCipher
from cipher.railfence import RailFenceCipher
from cipher.vigenere import VigenereCipher

app = Flask(__name__, template_folder="cipher/templates")

caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()
playfair_cipher = PlayFairCipher()
railfence_cipher = RailFenceCipher()
transposition_cipher = TranspositionCipher()


def _template_context(**values):
    context = {
        "encrypt_result": None,
        "decrypt_result": None,
        "error_message": None,
        "input_plain_text": "",
        "input_key_plain": "",
        "input_cipher_text": "",
        "input_key_cipher": "",
        "matrix_rows": None,
    }
    context.update(values)
    return context


def _render_page(template_name, status_code=200, **values):
    return render_template(template_name, **_template_context(**values)), status_code


def _parse_int(raw_value, field_name, minimum=None):
    try:
        value = int(raw_value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field_name} phải là số nguyên.") from error

    if minimum is not None and value < minimum:
        raise ValueError(f"{field_name} phải lớn hơn hoặc bằng {minimum}.")

    return value


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/caesar")
def caesar():
    return _render_page("caesar.html")


@app.route("/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    text = request.form.get("inputPlainText", "")
    key_raw = request.form.get("inputKeyPlain", "")

    try:
        key = _parse_int(key_raw, "Khóa")
        encrypted_text = caesar_cipher.encrypt_text(text, key)
        return _render_page(
            "caesar.html",
            input_plain_text=text,
            input_key_plain=key_raw,
            encrypt_result=encrypted_text,
        )
    except ValueError as error:
        return _render_page(
            "caesar.html",
            status_code=400,
            input_plain_text=text,
            input_key_plain=key_raw,
            error_message=str(error),
        )


@app.route("/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    text = request.form.get("inputCipherText", "")
    key_raw = request.form.get("inputKeyCipher", "")

    try:
        key = _parse_int(key_raw, "Khóa")
        decrypted_text = caesar_cipher.decrypt_text(text, key)
        return _render_page(
            "caesar.html",
            input_cipher_text=text,
            input_key_cipher=key_raw,
            decrypt_result=decrypted_text,
        )
    except ValueError as error:
        return _render_page(
            "caesar.html",
            status_code=400,
            input_cipher_text=text,
            input_key_cipher=key_raw,
            error_message=str(error),
        )


@app.route("/vigenere")
def vigenere():
    return _render_page("vigenere.html")


@app.route("/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    text = request.form.get("inputPlainText", "")
    key = request.form.get("inputKeyPlain", "")

    try:
        encrypted_text = vigenere_cipher.vigenere_encrypt(text, key)
        return _render_page(
            "vigenere.html",
            input_plain_text=text,
            input_key_plain=key,
            encrypt_result=encrypted_text,
        )
    except ValueError as error:
        return _render_page(
            "vigenere.html",
            status_code=400,
            input_plain_text=text,
            input_key_plain=key,
            error_message=str(error),
        )


@app.route("/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    text = request.form.get("inputCipherText", "")
    key = request.form.get("inputKeyCipher", "")

    try:
        decrypted_text = vigenere_cipher.vigenere_decrypt(text, key)
        return _render_page(
            "vigenere.html",
            input_cipher_text=text,
            input_key_cipher=key,
            decrypt_result=decrypted_text,
        )
    except ValueError as error:
        return _render_page(
            "vigenere.html",
            status_code=400,
            input_cipher_text=text,
            input_key_cipher=key,
            error_message=str(error),
        )


@app.route("/playfair")
def playfair():
    return _render_page("playfair.html")


@app.route("/playfair/encrypt", methods=["POST"])
def playfair_encrypt():
    text = request.form.get("inputPlainText", "")
    key = request.form.get("inputKeyPlain", "")
    matrix_rows = None

    try:
        matrix_rows = playfair_cipher.create_playfair_matrix(key)
        encrypted_text = playfair_cipher.playfair_encrypt(text, matrix_rows)
        return _render_page(
            "playfair.html",
            input_plain_text=text,
            input_key_plain=key,
            encrypt_result=encrypted_text,
            matrix_rows=matrix_rows,
        )
    except ValueError as error:
        return _render_page(
            "playfair.html",
            status_code=400,
            input_plain_text=text,
            input_key_plain=key,
            error_message=str(error),
            matrix_rows=matrix_rows,
        )


@app.route("/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    text = request.form.get("inputCipherText", "")
    key = request.form.get("inputKeyCipher", "")
    matrix_rows = None

    try:
        matrix_rows = playfair_cipher.create_playfair_matrix(key)
        decrypted_text = playfair_cipher.playfair_decrypt(text, matrix_rows)
        return _render_page(
            "playfair.html",
            input_cipher_text=text,
            input_key_cipher=key,
            decrypt_result=decrypted_text,
            matrix_rows=matrix_rows,
        )
    except ValueError as error:
        return _render_page(
            "playfair.html",
            status_code=400,
            input_cipher_text=text,
            input_key_cipher=key,
            error_message=str(error),
            matrix_rows=matrix_rows,
        )


@app.route("/railfence")
def railfence():
    return _render_page("railfence.html")


@app.route("/railfence/encrypt", methods=["POST"])
def railfence_encrypt():
    text = request.form.get("inputPlainText", "")
    key_raw = request.form.get("inputKeyPlain", "")

    try:
        key = _parse_int(key_raw, "Số rail", minimum=2)
        encrypted_text = railfence_cipher.rail_fence_encrypt(text, key)
        return _render_page(
            "railfence.html",
            input_plain_text=text,
            input_key_plain=key_raw,
            encrypt_result=encrypted_text,
        )
    except ValueError as error:
        return _render_page(
            "railfence.html",
            status_code=400,
            input_plain_text=text,
            input_key_plain=key_raw,
            error_message=str(error),
        )


@app.route("/railfence/decrypt", methods=["POST"])
def railfence_decrypt():
    text = request.form.get("inputCipherText", "")
    key_raw = request.form.get("inputKeyCipher", "")

    try:
        key = _parse_int(key_raw, "Số rail", minimum=2)
        decrypted_text = railfence_cipher.rail_fence_decrypt(text, key)
        return _render_page(
            "railfence.html",
            input_cipher_text=text,
            input_key_cipher=key_raw,
            decrypt_result=decrypted_text,
        )
    except ValueError as error:
        return _render_page(
            "railfence.html",
            status_code=400,
            input_cipher_text=text,
            input_key_cipher=key_raw,
            error_message=str(error),
        )


@app.route("/transposition")
def transposition():
    return _render_page("transposition.html")


@app.route("/transposition/encrypt", methods=["POST"])
def transposition_encrypt():
    text = request.form.get("inputPlainText", "")
    key_raw = request.form.get("inputKeyPlain", "")

    try:
        key = _parse_int(key_raw, "Khóa", minimum=1)
        encrypted_text = transposition_cipher.encrypt(text, key)
        return _render_page(
            "transposition.html",
            input_plain_text=text,
            input_key_plain=key_raw,
            encrypt_result=encrypted_text,
        )
    except ValueError as error:
        return _render_page(
            "transposition.html",
            status_code=400,
            input_plain_text=text,
            input_key_plain=key_raw,
            error_message=str(error),
        )


@app.route("/transposition/decrypt", methods=["POST"])
def transposition_decrypt():
    text = request.form.get("inputCipherText", "")
    key_raw = request.form.get("inputKeyCipher", "")

    try:
        key = _parse_int(key_raw, "Khóa", minimum=1)
        decrypted_text = transposition_cipher.decrypt(text, key)
        return _render_page(
            "transposition.html",
            input_cipher_text=text,
            input_key_cipher=key_raw,
            decrypt_result=decrypted_text,
        )
    except ValueError as error:
        return _render_page(
            "transposition.html",
            status_code=400,
            input_cipher_text=text,
            input_key_cipher=key_raw,
            error_message=str(error),
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
