from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QTextEdit, QVBoxLayout, QWidget
from PySide6.QtCore import QSize, Qt
import sys

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.press_ahead = True
        self.setWindowTitle("My App!!")
        self.resize(400, 300)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.inputField_Username = QLineEdit()
        self.inputField_Password = QLineEdit()
        self.button = QPushButton("Register account")
        self.button2 = QPushButton("Confirm")
        self.output = QTextEdit()
        self.button.clicked.connect(self.libme)
        self.button2.clicked.connect(self.register_account)

        layout.addWidget(self.inputField_Username)
        layout.addWidget(self.inputField_Password)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        layout.addWidget(self.output)
    def libme(self):
        self.username = self.inputField_Username.text()
        self.password = self.inputField_Password.text()
        if self.username:
            self.output.insertPlainText(f"\nUsername: {self.username}")
        else:
            self.output.insertPlainText("\nPlease enter username.")
            self.press_ahead = False
        if self.password:
            self.output.insertPlainText(f"\nPassword: {self.password}")
        else:
            self.output.insertPlainText("\nPlease enter password.")
            self.press_ahead = False
    def register_account(self):
        if self.press_ahead:
            result = ("REQUEST: Account", self.username, self.password)
            print(result)
            response = input()
            if response == "ACCOUNT_CREATED":
                print("Continuing.", file=sys.stderr)
            elif response == "ACCOUNT_EXISTS":
                print("Failure..", file=sys.stderr)






app = QApplication(sys.argv)
window = MyApp()
window.show()
app.exec()