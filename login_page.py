from selenium_wrapper import SeleniumWrapper


class Login(SeleniumWrapper):
    txt_username = {"id":"login_field"}
    txt_password = {"id": "password"}
    btn_sign_in = {"name": "commit"}

    def perform_login(self, username, password):
        self.driver.get("https://github.com/login")
        self.send_text(username, self.txt_username)
        self.send_text(password, self.txt_password)
        self.element_click(self.btn_sign_in)
