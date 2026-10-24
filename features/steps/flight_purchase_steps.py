import re
from behave import given, when, then
from playwright.sync_api import sync_playwright

from ai.test_data_generator import CustomerDataGenerator
from pages.home_page import HomePage
from pages.reserve_page import ReservePage
from pages.purchase_page import PurchasePage

BASE_URL = "https://blazedemo.com/"


@given("I open the BlazeDemo flight search")
def open_search(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=False)
    context.page = context.browser.new_page()
    context.page.goto(BASE_URL, wait_until="domcontentloaded")


@when("I search for flights from Paris to New York")
def search_flights(context):
    HomePage(context.page).search_flight("Paris", "New York")
    context.route = "Paris to New York"
    context.page.locator("table tbody tr").first.wait_for()


@when("I select the cheapest available flight")
def select_cheapest(context):
    context.flight_price = ReservePage(context.page).choose_flight()


@when("I complete the purchase with Cohere generated customer details")
def complete_purchase(context):
    print("Requesting synthetic customer data from Cohere...")
    context.customer = CustomerDataGenerator().generate_customer()
    print(f"Generated Customer: {context.customer['name']}, Card ending: {context.customer['card_number'][-4:]}")
    PurchasePage(context.page).complete_purchase(context.customer)
    context.page.locator("h1").wait_for()


@then("the purchase confirmation is displayed")
def confirmation(context):
    context.confirmation = context.page.locator("h1").inner_text().strip()
    assert context.confirmation == "Thank you for your purchase today!", (
        f"Unexpected confirmation: {context.confirmation}"
    )
    body = context.page.locator("body").inner_text()
    match = re.search(r"(?im)^\s*Id\s+([0-9]+)\s*$", body)
    assert match, "Confirmation page did not contain an order ID."
    context.order_id = match.group(1)


@then("the order ID is returned")
def return_order_id(context):
    assert context.order_id, "Order ID was not captured."
    print(f"\n✅ SUCCESS: Captured Order ID={context.order_id}")
