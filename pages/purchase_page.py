"""
Page Object for the BlazeDemo Flight Purchase form.
Integrates self-healing locators via LocatorHealer on any selector exception.
"""

from ai.locator_healer import LocatorHealer

class PurchasePage:
    def __init__(self, page):
        self.page = page
        self.healer = LocatorHealer()

    def safe_fill(self, locator: str, value: str):
        """Attempts to fill locator; on failure, triggers AI self-healing."""
        try:
            self.page.locator(locator).fill(value, timeout=5000)
        except Exception:
            print(f"Locator '{locator}' failed. Triggering AI self-healing...")
            html = self.page.content()
            healed_locator = self.healer.suggest_locator(locator, html)
            print(f"Healed Locator suggested by AI: {healed_locator}")
            self.page.locator(healed_locator).fill(value)

    def complete_purchase(self, customer: dict):
        self.safe_fill("input[id='inputName']", customer["name"])
        self.safe_fill("input[id='address']", customer["address"])
        self.safe_fill("input[id='city']", customer["city"])
        self.safe_fill("input[id='state']", customer["state"])
        self.safe_fill("input[id='zip']", customer["zip"])

        self.page.select_option("select[id='cardType']", "visa")

        self.safe_fill("input[id='creditCardNumber']", customer["card_number"])
        self.safe_fill("input[id='creditCardMonth']", customer["month"])
        self.safe_fill("input[id='creditCardYear']", customer["year"])
        self.safe_fill("input[id='nameOnCard']", customer["card_holder"])

        self.page.locator("input[value='Purchase Flight']").click()
