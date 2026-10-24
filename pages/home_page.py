class HomePage:
    def __init__(self, page):
        self.page = page

    def search_flight(self, origin="Paris", destination="New York"):
        self.page.select_option("select[name='fromPort']", origin)
        self.page.select_option("select[name='toPort']", destination)
        self.page.locator("input[value='Find Flights']").click()
