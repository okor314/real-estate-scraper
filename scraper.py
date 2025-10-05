from playwright.sync_api import sync_playwright, Playwright
from playwright_stealth import Stealth

BASE_URL = 'https://www.zillow.com/'

class Scraper:
    def __init__(self):
        pass

    def search(self, searchQuery: str):
        search_bar = self.page.locator('//input[@role="combobox"]')
        search_bar.clear()
        search_bar.type(searchQuery, delay=100)
        search_bar.press('Enter')
        self.skipPopUp()

    def skipPopUp(self):
        try:
            skipBtn = self.page.wait_for_selector('//button[text()="Skip this question"]', timeout=3000)
            skipBtn.click()
        except:
            pass

    def scrape(self, searchQuery: str):
        self.page.goto(BASE_URL)
        self.search(searchQuery)

    def run(self, searchQuery):
        with Stealth().use_sync(sync_playwright()) as playwright:
            self.browser = playwright.chromium.launch(headless=False)
            self.page = self.browser.new_page()

            self.scrape(searchQuery)

            self.browser.close()

class Filter:
    def __init__(self):
        self.statusType = 'ForRent'
        self.minPrice: int | None = None
        self.maxPrice: int | None = None
        self.minBedrooms: int = 0
        self.minBathrooms: int = 0

    def setFilterParameters(self, **kwargs):
        for attrName, attrValue in kwargs.items():
            setattr(self, attrName, attrValue)

if __name__ == '__main__':
    scraper = Scraper()
    scraper.run('Portland, ME')