# Demoblaze Laptops RAG Test

This standalone test opens Demoblaze in a visible Chromium window, selects the Laptops category, collects laptop names and prices across pagination, persists the workbook at `artifacts/demoblaze_laptops.xlsx`, reloads those rows as RAG context, asks Cohere to find the cheapest laptop, and validates the exact JSON keys and numeric values.

## Running the Test

```bash
# 1. Install Playwright browser binaries
python -m playwright install chromium

# 2. Run the test with pytest
pytest tests/test_demoblaze_laptops_rag.py -s -v
```
