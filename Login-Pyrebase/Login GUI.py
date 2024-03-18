from pyrebase import pyrebase
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys

firebaseConfig = {
  "apiKey": "AIzaSyDG77SQa1X7TRpBKysBrnWuNGlzp1sQriw",
  "authDomain": "login-pyrebase-236aa.firebaseapp.com",
  "projectId": "login-pyrebase-236aa",
  "storageBucket": "login-pyrebase-236aa.appspot.com",
  "messagingSenderId": "423396167437",
  "appId": "1:423396167437:web:57a49528e25bc14d96aa44",
  "measurementId": "G-SFPE7TEZ1B",
  "databaseURL": "https://login-pyrebase-236aa-default-rtdb.firebaseio.com/"
}

connection = pyrebase.initialize_app(firebaseConfig)
auth = connection.auth()
db = connection.database()
class Application(QWidget):

    def __init__(self):
        super(Application, self).__init__()
        self.initialize()

    def initialize(self):

        self.setWindowTitle("LOGIN")
        self.display_widgets()

    def display_widgets(self):
        self.lbl_titulo = QLabel("Login", self)
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.lbl_titulo.setFont(QFont("Arial", 20))

        self.lned_name = QLineEdit(self)
        self.lned_name.setPlaceholderText("Nombre")
        self.lned_lastname = QLineEdit(self)
        self.lned_lastname.setPlaceholderText("Apellido")
        self.lned_age = QLineEdit(self)
        self.lned_age.setPlaceholderText("Edad")
        self.lned_email = QLineEdit(self)
        self.lned_email.setPlaceholderText("Email")
        self.lned_password = QLineEdit(self)
        self.lned_password.setPlaceholderText("Password")
        self.lned_password.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Login", self)
        self.btn_register = QPushButton("Register", self)
        self.btn_change_password = QPushButton("Change Password", self)

        self.state = QLabel(self)
        self.state.setAlignment(Qt.AlignCenter)

        hlyt_botones = QHBoxLayout()
        hlyt_botones.addWidget(self.btn_login)
        hlyt_botones.addWidget(self.btn_register)
        hlyt_botones.addWidget(self.btn_change_password)

        vlyt_principal = QVBoxLayout()
        vlyt_principal.addWidget(self.lbl_titulo)
        vlyt_principal.addWidget(self.lned_name)
        vlyt_principal.addWidget(self.lned_lastname)
        vlyt_principal.addWidget(self.lned_age)
        vlyt_principal.addWidget(self.lned_email)
        vlyt_principal.addWidget(self.lned_password)
        vlyt_principal.addLayout(hlyt_botones)
        vlyt_principal.addWidget(self.state)
        self.setLayout(vlyt_principal)

        self.btn_login.clicked.connect(self.fun_login)
        self.btn_register.clicked.connect(self.fun_register)
        self.btn_change_password.clicked.connect(self.fun_change_password)


    def fun_login(self):
        email = self.lned_email.text()
        password = self.lned_password.text()

        try:
            usuario = auth.sign_in_with_email_and_password(email,password)
            self.state.setText("Se logueó correctamente")
        except:
            self.state.setText("Los datos ingresados son incorrectos")

    def fun_register(self):
        nombre = self.lned_name.text()
        apellido = self.lned_lastname.text()
        edad = self.lned_age.text()
        email = self.lned_email.text()
        password = self.lned_password.text()

        try:
            user = auth.create_user_with_email_and_password(email,password)
            datos = {"nombre":nombre, "apellido":apellido, "edad":int(edad)}
            db.child("usuarios").child(user["localId"]).set(datos)
        except:
            self.state.setText("Este usuario ya esta registrado")

    def fun_change_password(self):
        email = self.lned_email.text()

        try:
            auth.send_password_reset_email(email)
            self.state.setText("Se ha mandado un link a su correo para reestablecer la contraseña")
        except:
            self.state.setText("Los datos ingresados son incorrectos")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())