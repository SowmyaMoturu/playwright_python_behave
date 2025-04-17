from .base_page import Base_Page
from playwright.sync_api import Page

class Register_Page(Base_Page):

    locators = {
        "first_name": "#firstname",
        "last_name": "#lastname",
        "email": "#email_address",
        "password": "#password",
        "confirm_password": "#password-confirmation",
        "submit_button": "Create an Account"
    }
    
    def __init__(self, page: Page):
        super().__init__(page)

    def register(self, fname: str, lname: str, email: str, password: str):
        data = {
            "first_name": fname,
            "last_name": lname,
            "email": email,
            "password": password,
            "confirm_password": password
        }

        for field, value in data.items():
            self.page.locator(self.locators[field]).fill(value)
 
    def submit_form(self):
        self.page.get_by_role("button").filter(has_text=self.locators["submit_button"]).click()