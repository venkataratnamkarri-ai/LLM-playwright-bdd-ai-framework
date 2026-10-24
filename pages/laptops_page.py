"""
Page Object for scraping laptop details from Demoblaze.
"""

from __future__ import annotations
import re
from decimal import Decimal, InvalidOperation
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class LaptopsPage:
    URL = "https://www.demoblaze.com/"
    PRODUCT_CARD = "#tbodyid .card"

    def __init__(self, page):
        self.page = page

    def collect_laptops(self) -> list[dict]:
        """Navigate to Laptops category and extract product names and prices across pages."""
        self.page.goto(self.URL, wait_until="domcontentloaded")
        category = self.page.get_by_role("link", name="Laptops", exact=True)
        category.wait_for(state="visible")

        with self.page.expect_response(
            lambda response: "bycat" in response.url.lower(),
            timeout=15000,
        ):
            category.click()

        laptops: list[dict] = []
        seen_pages: set[tuple[str, ...]] = set()

        while True:
            cards = self.page.locator(self.PRODUCT_CARD)
            try:
                cards.first.wait_for(state="visible", timeout=10000)
            except PlaywrightTimeoutError:
                break

            page_laptops = []
            for card in cards.all():
                name = card.locator(".card-title a").inner_text().strip()
                price_text = card.locator(".card-block h5").inner_text().strip()
                page_laptops.append({
                    "Name": name,
                    "Price": self._parse_price(price_text),
                })

            signature = tuple(item["Name"] for item in page_laptops)
            if not signature or signature in seen_pages:
                break
            seen_pages.add(signature)
            laptops.extend(page_laptops)

            if len(page_laptops) < 9:
                break

            next_button = self.page.locator("#next2")
            if next_button.count() == 0 or not next_button.is_visible() or not next_button.is_enabled():
                break

            previous_text = self.page.locator("#tbodyid").inner_text()
            next_button.click()
            try:
                self.page.wait_for_function(
                    "(previous) => { const node = document.querySelector('#tbodyid'); "
                    "return node && node.innerText !== previous; }",
                    previous_text,
                    timeout=10000,
                )
            except Exception:
                break

        if not laptops:
            raise RuntimeError("No laptops found in the Demoblaze Laptops category.")

        unique = {laptop["Name"]: laptop for laptop in laptops}
        return list(unique.values())

    @staticmethod
    def _parse_price(text: str) -> float:
        match = re.search(r"\d[\d,]*(?:\.\d+)?", text)
        if not match:
            raise ValueError(f"Could not parse laptop price: {text!r}")
        try:
            return float(Decimal(match.group(0).replace(",", "")))
        except (InvalidOperation, ValueError):
            raise ValueError(f"Could not parse laptop price: {text!r}") from None
