"""
End-to-End Demoblaze Laptop Scraping, Excel Persistence, and Cohere RAG Validation.
"""

import os
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from ai.error_analyzer import ErrorAnalyzer
from ai.laptops_rag import LaptopQuestionAnswerer, read_laptops_excel, write_laptops_excel
from pages.laptops_page import LaptopsPage

OUTPUT_FILE = BASE_DIR / "artifacts" / "demoblaze_laptops.xlsx"


def test_find_cheapest_demoblaze_laptop():
    analyzer = ErrorAnalyzer()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            print("Scraping laptop catalog from Demoblaze...")
            scraped_laptops = LaptopsPage(page).collect_laptops()
            print(f"Scraped {len(scraped_laptops)} laptops.")

            print(f"Persisting catalog to Excel: {OUTPUT_FILE}")
            write_laptops_excel(scraped_laptops, OUTPUT_FILE)

            print("Reloading rows from Excel to build RAG context...")
            excel_laptops = read_laptops_excel(OUTPUT_FILE)

            print("Querying Cohere RAG to identify cheapest laptop...")
            answer = LaptopQuestionAnswerer(
                api_key=os.getenv("COHERE_API_KEY")
            ).cheapest_laptop(excel_laptops)

            print("\n==============================")
            print(f"✅ RAG Validated Cheapest Laptop: {answer}")
            print("==============================\n")

        except Exception as error:
            page_text = page.locator("body").inner_text()
            report = analyzer.analyze(str(error), page_text)

            print("\n===== AI ERROR ANALYSIS =====")
            print(report)
            print("==============================\n")
            raise

        finally:
            browser.close()


if __name__ == "__main__":
    test_find_cheapest_demoblaze_laptop()
