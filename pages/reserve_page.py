class ReservePage:
    def __init__(self, page):
        self.page = page

    def choose_flight(self) -> float:
        rows = self.page.locator("table tbody tr")
        candidates = []
        for index in range(rows.count()):
            row = rows.nth(index)
            price_text = row.locator("td").nth(5).inner_text().strip().replace("$", "")
            candidates.append((float(price_text), index))

        if not candidates:
            raise AssertionError("No flights were listed for the selected route.")

        price, index = min(candidates)
        rows.nth(index).locator("input[type='submit']").click()
        return price
