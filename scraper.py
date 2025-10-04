from playwright.sync_api import sync_playwright, Playwright
from playwright_stealth import Stealth

BASE_URL = 'https://www.zillow.com/'

class Scraper:
    def __init__(self, playwright: Playwright, searchQuery: str):
        self.browser = playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()

        self.scrape(searchQuery)

        self.browser.close()


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
    # with Stealth().use_sync(sync_playwright()) as playwright:
    #     Scraper(playwright, 'Montgomery, AL')

    f = Filter()
    d = {
        'statusType': 'ForSale',
        'minBedrooms': 2
    }
    print(f.statusType, f.maxPrice, f.minBedrooms)
    f.setFilterParameters(**d)
    print(f.statusType, f.maxPrice, f.minBedrooms)