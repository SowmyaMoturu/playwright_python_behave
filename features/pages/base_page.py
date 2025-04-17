from playwright.sync_api import Page

class Base_Page:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url, timeout=60000)

    def drag_and_drop(self, source_selector, target_selector):
        try:
            self.page.drag_and_drop(source_selector, target_selector)
        except Exception as e:
            print(f"Error during drag and drop: {e}")
    
    def select_dropdown_option(self, selector: str, option: str, by: str = "value"):
        try:
            dropdown = self.page.locator(selector)
            if by == "value":
                dropdown.select_option(value=option)
            elif by == "label":
                dropdown.select_option(label=option)
            elif by == "index":
                dropdown.select_option(index=int(option))
            else:
                raise ValueError("Invalid 'by' parameter. Use 'value', 'label', or 'index'.")
        except Exception as e:
            print(f"Error selecting dropdown option '{option}' by '{by}': {e}")