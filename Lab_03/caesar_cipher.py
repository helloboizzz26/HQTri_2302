import sys
import requests

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btnEncrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btnDecrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": self.ui.txtPlainText.toPlainText(),
            "key": self.ui.txtKey.text()
        }

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                self.ui.txtCipherText.setText(data["encrypted_text"])

                QMessageBox.information(self, "Information", "Encrypted Successfully")
            else:
                QMessageBox.warning(self, "Error", "Error while calling API")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", str(e))

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": self.ui.txtCipherText.toPlainText(),
            "key": self.ui.txtKey.text()
        }

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                self.ui.txtPlainText.setText(data["decrypted_text"])

                QMessageBox.information(self, "Information", "Decrypted Successfully")
            else:
                QMessageBox.warning(self, "Error", "Error while calling API")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())