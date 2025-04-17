from .base_page import Base_Page
from playwright.sync_api import Page

class Login_Page(Base_Page):

    locators = {
        "email": "#email",
        "password": "#pass",
        "submit": "#send2"
    }
    
    def __init__(self, page: Page):
        super().__init__(page)

    def login(self, email: str, password: str):
        self.page.locator(self.locators["email"]).fill(email)
        self.page.locator(self.locators["password"]).fill(password)
        self.page.locator(self.locators["submit"]).click()