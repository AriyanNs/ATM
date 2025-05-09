import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QLineEdit, QMessageBox, QInputDialog
)

translations = {
    'fa': {
        'welcome': "به دستگاه ATM خوش آمدید",
        'login': "ورود",
        'register': "ثبت‌نام",
        'card_number': "شماره کارت",
        'pin': "رمز عبور",
        'success': "موفق",
        'error': "خطا",
        'already_registered': "این شماره کارت قبلاً ثبت شده است.",
        'fill_fields': "لطفاً همه فیلدها را پر کنید.",
        'login_failed': "شماره کارت یا رمز اشتباه است",
        'balance': "موجودی: {amount} تومان",
        'withdraw_success': "برداشت انجام شد",
        'insufficient_funds': "موجودی کافی نیست",
        'transfer_success': "انتقال انجام شد",
        'transfer_failed': "مشکل در انتقال وجه",
        'pin_changed': "رمز تغییر یافت",
        'select_language': "زبان خود را انتخاب کنید",
        'language_prompt': "لطفاً زبان را انتخاب کنید:",
        'main_menu': "منوی اصلی",
        'show_balance': "نمایش موجودی",
        'withdraw': "برداشت وجه",
        'transfer': "انتقال وجه",
        'change_pin': "تغییر رمز",
        'exit': "خروج",
        'amount_prompt': "مبلغ:",
        'target_card': "کارت مقصد:",
        'new_pin': "رمز جدید:",
        'withdraw_amount': "مبلغ برداشت را انتخاب کنید:",
    },
    'en': {
        'welcome': "Welcome to the ATM",
        'login': "Login",
        'register': "Register",
        'card_number': "Card Number",
        'pin': "PIN",
        'success': "Success",
        'error': "Error",
        'already_registered': "This card is already registered.",
        'fill_fields': "Please fill all fields.",
        'login_failed': "Invalid card or PIN",
        'balance': "Balance: {amount} IRR",
        'withdraw_success': "Withdrawal successful",
        'insufficient_funds': "Insufficient funds",
        'transfer_success': "Transfer successful",
        'transfer_failed': "Transfer failed",
        'pin_changed': "PIN changed",
        'select_language': "Select Language",
        'language_prompt': "Please choose a language:",
        'main_menu': "Main Menu",
        'show_balance': "Check Balance",
        'withdraw': "Withdraw",
        'transfer': "Transfer",
        'change_pin': "Change PIN",
        'exit': "Exit",
        'amount_prompt': "Amount:",
        'target_card': "Target Card:",
        'new_pin': "New PIN:",
        'withdraw_amount': "Choose amount to withdraw:",
    }
}

lang = 'fa'
_ = lambda key, **kwargs: translations[lang][key].format(**kwargs)


class User:
    def __init__(self, card_number, balance, pin):
        self.card_number = card_number
        self.balance = int(balance)
        self.pin = pin

    def to_line(self):
        return f"{self.card_number},{self.balance},{self.pin}\n"


class ATM:
    def __init__(self, user_file='users.txt'):
        self.user_file = user_file
        self.users = self.load_users()
        self.current_user = None

    def load_users(self):
        users = {}
        try:
            with open(self.user_file, 'r') as file:
                for line in file:
                    card, balance, pin = line.strip().split(',')
                    users[card] = User(card, balance, pin)
        except FileNotFoundError:
            open(self.user_file, 'w').close()
        return users

    def save_users(self):
        with open(self.user_file, 'w') as file:
            for user in self.users.values():
                file.write(user.to_line())

    def register_user(self, card_number, pin):
        if card_number in self.users:
            return False
        self.users[card_number] = User(card_number, 100000, pin)
        self.save_users()
        return True

    def login(self, card_number, pin):
        user = self.users.get(card_number)
        if user and user.pin == pin:
            self.current_user = user
            return True
        return False

    def check_balance(self):
        return self.current_user.balance

    def withdraw(self, amount):
        if self.current_user.balance >= amount:
            self.current_user.balance -= amount
            self.save_users()
            return True
        return False

    def change_pin(self, new_pin):
        self.current_user.pin = new_pin
        self.save_users()

    def transfer(self, to_card, amount):
        target = self.users.get(to_card)
        if target and self.current_user.balance >= amount:
            self.current_user.balance -= amount
            target.balance += amount
            self.save_users()
            return True
        return False


class LanguageSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Language")
        self.resize(400, 300)
        self.setStyleSheet("background-color: #eef;")

        btn_fa = QPushButton("فارسی")
        btn_en = QPushButton("English")

        btn_fa.clicked.connect(self.select_fa)
        btn_en.clicked.connect(self.select_en)

        layout = QVBoxLayout()
        label = QLabel(translations['fa']['language_prompt'])
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)
        layout.addWidget(btn_fa)
        layout.addWidget(btn_en)
        self.setLayout(layout)

    def select_fa(self):
        global lang
        lang = 'fa'
        self.go_to_start()

    def select_en(self):
        global lang
        lang = 'en'
        self.go_to_start()

    def go_to_start(self):
        self.atm = ATM()
        self.start_window = StartWindow(self.atm)
        self.start_window.show()
        self.close()


class StartWindow(QWidget):
    def __init__(self, atm):
        super().__init__()
        self.atm = atm
        self.setWindowTitle(_("main_menu"))
        self.resize(400, 300)
        self.setStyleSheet("background-color: #ddf;")

        self.login_btn = QPushButton(_("login"))
        self.register_btn = QPushButton(_("register"))

        self.login_btn.clicked.connect(self.go_login)
        self.register_btn.clicked.connect(self.go_register)

        layout = QVBoxLayout()
        label = QLabel(_("welcome"))
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(label)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)
        self.setLayout(layout)

    def go_login(self):
        self.login_window = LoginWindow(self.atm)
        self.login_window.show()
        self.close()

    def go_register(self):
        self.register_window = RegisterWindow(self.atm)
        self.register_window.show()
        self.close()


class RegisterWindow(QWidget):
    def __init__(self, atm):
        super().__init__()
        self.atm = atm
        self.setWindowTitle(_("register"))
        self.resize(400, 300)
        self.setStyleSheet("background-color: #efe;")

        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText(_("card_number"))

        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText(_("pin"))
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn = QPushButton(_("register"))
        self.btn.clicked.connect(self.register)

        self.back_btn = QPushButton("←")
        self.back_btn.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(_("register")))
        layout.addWidget(self.card_input)
        layout.addWidget(self.pin_input)
        layout.addWidget(self.btn)
        layout.addWidget(self.back_btn)
        self.setLayout(layout)

    def register(self):
        card = self.card_input.text()
        pin = self.pin_input.text()
        if card and pin:
            if self.atm.register_user(card, pin):
                QMessageBox.information(
                    self, _("success"), _("register") + " successful")
                self.login_window = LoginWindow(self.atm)
                self.login_window.show()
                self.close()
            else:
                QMessageBox.warning(self, _("error"), _("already_registered"))
        else:
            QMessageBox.warning(self, _("error"), _("fill_fields"))

    def go_back(self):
        self.start_window = StartWindow(self.atm)
        self.start_window.show()
        self.close()


class LoginWindow(QWidget):
    def __init__(self, atm):
        super().__init__()
        self.atm = atm
        self.setWindowTitle(_("login"))
        self.resize(400, 300)
        self.setStyleSheet("background-color: #ffe;")

        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText(_("card_number"))

        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setPlaceholderText(_("pin"))

        self.login_btn = QPushButton(_("login"))
        self.login_btn.clicked.connect(self.handle_login)

        self.back_btn = QPushButton("←")
        self.back_btn.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(_("login")))
        layout.addWidget(self.card_input)
        layout.addWidget(self.pin_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.back_btn)
        self.setLayout(layout)

    def handle_login(self):
        card = self.card_input.text()
        pin = self.pin_input.text()
        if self.atm.login(card, pin):
            self.main_menu = MainMenu(self.atm)
            self.main_menu.show()
            self.close()
        else:
            QMessageBox.critical(self, _("error"), _("login_failed"))

    def go_back(self):
        self.start_window = StartWindow(self.atm)
        self.start_window.show()
        self.close()


class MainMenu(QWidget):
    def __init__(self, atm):
        super().__init__()
        self.atm = atm
        self.setWindowTitle(_("main_menu"))
        self.resize(400, 400)
        self.setStyleSheet("background-color: #f0f0ff;")

        self.balance_btn = QPushButton(_("show_balance"))
        self.withdraw_btn = QPushButton(_("withdraw"))
        self.transfer_btn = QPushButton(_("transfer"))
        self.change_pin_btn = QPushButton(_("change_pin"))
        self.exit_btn = QPushButton(_("exit"))

        self.balance_btn.clicked.connect(self.show_balance)
        self.withdraw_btn.clicked.connect(self.withdraw)
        self.transfer_btn.clicked.connect(self.transfer)
        self.change_pin_btn.clicked.connect(self.change_pin)
        self.exit_btn.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.balance_btn)
        layout.addWidget(self.withdraw_btn)
        layout.addWidget(self.transfer_btn)
        layout.addWidget(self.change_pin_btn)
        layout.addWidget(self.exit_btn)
        self.setLayout(layout)

    def show_balance(self):
        balance = self.atm.check_balance()
        QMessageBox.information(self, _("show_balance"),
                                _("balance", amount=balance))

    def withdraw(self):
        options = ["10000", "20000", "50000", "100000",
                   "دستی" if lang == 'fa' else "Custom"]
        choice, ok = QInputDialog.getItem(
            self, _("withdraw"), _("withdraw_amount"), options, 0, False)
        if ok:
            if choice.isdigit():
                amount = int(choice)
            else:
                amount_str, ok = QInputDialog.getText(
                    self, _("withdraw"), _("amount_prompt"))
                if not ok or not amount_str.isdigit():
                    return
                amount = int(amount_str)
            if self.atm.withdraw(amount):
                QMessageBox.information(
                    self, _("success"), _("withdraw_success"))
            else:
                QMessageBox.warning(self, _("error"), _("insufficient_funds"))

    def transfer(self):
        to_card, ok1 = QInputDialog.getText(
            self, _("transfer"), _("target_card"))
        amount_str, ok2 = QInputDialog.getText(
            self, _("transfer"), _("amount_prompt"))
        if ok1 and ok2 and amount_str.isdigit():
            if self.atm.transfer(to_card, int(amount_str)):
                QMessageBox.information(
                    self, _("success"), _("transfer_success"))
            else:
                QMessageBox.warning(self, _("error"), _("transfer_failed"))

    def change_pin(self):
        new_pin, ok = QInputDialog.getText(self, _("change_pin"), _("new_pin"))
        if ok and new_pin:
            self.atm.change_pin(new_pin)
            QMessageBox.information(self, _("success"), _("pin_changed"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    selector = LanguageSelector()
    selector.show()
    sys.exit(app.exec())
