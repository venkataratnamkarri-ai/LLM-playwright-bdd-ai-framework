"""
Pytest Autonomous Flight Booking Test with AI Modules.
Demonstrates:
1. Synthetic Customer Data Generation with Cohere.
2. Page Object Model (POM) navigation on BlazeDemo.
3. Semantic verification of purchase completion using AssertionEngine.
4. On failure: automated root-cause failure analysis via ErrorAnalyzer.
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from pages.home_page import HomePage
from pages.reserve_page import ReservePage
from pages.purchase_page import PurchasePage
from ai.test_data_generator import CustomerDataGenerator
from ai.error_analyzer import ErrorAnalyzer
from ai.assertion_engine import AssertionEngine

BASE_URL = "https://blazedemo.com/"


def test_book_flight():
    print("Generating synthetic checkout data via Cohere AI...")
    ai_data = CustomerDataGenerator()
    customer = ai_data.generate_customer()
    print(f"Customer Name: {customer['name']}")

    analyzer = ErrorAnalyzer()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            print(f"Navigating to {BASE_URL}...")
            page.goto(BASE_URL)

            HomePage(page).search_flight()
            ReservePage(page).choose_flight()
            PurchasePage(page).complete_purchase(customer)

            # AI Semantic Assertion
            assertion_engine = AssertionEngine()
            page_text = page.locator("body").inner_text()
            ai_result = assertion_engine.verify_purchase_success(page_text)

            assert ai_result == "Thank you for your purchase today!", (
                f"Unexpected AI assertion: {ai_result}"
            )
            print("\n==============================")
            print(f"✅ Purchase Verified: {ai_result}")
            print("==============================\n")

        except Exception as e:
            page_text = page.locator("body").inner_text()
            report = analyzer.analyze(str(e), page_text)

            print("\n===== AI ERROR ANALYSIS =====")
            print(report)
            print("==============================\n")
            raise

        finally:
            browser.close()


if __name__ == "__main__":
    test_book_flight()
