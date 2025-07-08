import sys
import hashlib
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget

class WillkommenScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("gui/willkommen.ui", self)
        self.btn_anmelden.clicked.connect(self.goto_login)
        self.btn_erstellen.clicked.connect(self.goto_create)

    def goto_login(self):
        widget.setCurrentWidget(login_screen)

    def goto_create(self):
        widget.setCurrentWidget(create_screen)


class LoginScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("gui/login.ui", self)
        self.txt_passwort.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btn_login.clicked.connect(self.login_function)

    def login_function(self):
        nutzer = self.txt_nutzername.text()
        passwort = self.txt_passwort.text()

        if not nutzer or not passwort:
            self.txt_regex.setText("Bitte Felder ausfüllen.")
            return

        hashed_pw = hashlib.sha256(passwort.encode()).hexdigest()
        try:
            conn = sqlite3.connect("FGambling.db")
            cur = conn.cursor()
            cur.execute("SELECT password FROM User WHERE username = ?", (nutzer,))
            result = cur.fetchone()
            conn.close()

            if result and result[0] == hashed_pw:
                self.txt_regex.setText("")
                widget.setCurrentWidget(startseite_screen)
            else:
                self.txt_regex.setText("Falscher Nutzername oder Passwort")
        except Exception as e:
            self.txt_regex.setText("Fehler beim Zugriff auf die Datenbank.")


class CreateAccScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("gui/create.ui", self)
        self.txt_passwort.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_confirmpasswort.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btn_erstellen.clicked.connect(self.signup_function)

    def signup_function(self):
        nutzer = self.txt_nutzername.text()
        email = self.txt_email.text()
        pw1 = self.txt_passwort.text()
        pw2 = self.txt_confirmpasswort.text()

        if not nutzer or not email or not pw1 or not pw2:
            self.txt_regex.setText("Bitte fülle alle Felder aus.")
            return

        if pw1 != pw2:
            self.txt_regex.setText("Passwörter stimmen nicht überein!")
            return

        hashed_pw = hashlib.sha256(pw1.encode()).hexdigest()

        try:
            conn = sqlite3.connect("FGambling.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM User WHERE username = ?", (nutzer,))
            if cur.fetchone():
                self.txt_regex.setText("Benutzername bereits vergeben.")
                conn.close()
                return

            cur.execute("INSERT INTO User (username, password, email) VALUES (?, ?, ?)", (nutzer, hashed_pw, email))
            conn.commit()
            conn.close()
            self.txt_regex.setText("Konto erfolgreich erstellt.")
            widget.setCurrentWidget(startseite_screen)

        except Exception as e:
            self.txt_regex.setText("Fehler beim Speichern des Benutzers.")


class StartseiteScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("gui/startseite.ui", self)


app = QApplication(sys.argv)

willkommen_screen = WillkommenScreen()
login_screen = LoginScreen()
create_screen = CreateAccScreen()
startseite_screen = StartseiteScreen()

widget = QStackedWidget()
widget.addWidget(willkommen_screen)
widget.addWidget(login_screen)
widget.addWidget(create_screen)
widget.addWidget(startseite_screen)

widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()

try:
    sys.exit(app.exec_())
except Exception as e:
    print("Fehler beim Ausführen:", e)
