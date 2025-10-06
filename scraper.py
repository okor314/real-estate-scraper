from playwright.sync_api import sync_playwright, Playwright
from playwright_stealth import Stealth

import os
import json
from helpFuncs import *
from extractors import *

BASE_URL = 'https://www.zillow.com/'

class Scraper:
    def __init__(self):
        self.pathToDataFile = None

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

    def scrape(self, searchQuery: str, requestsPerMin = 15, pathToSave='./data.json'):
        allApartments = []

        self.page.goto(BASE_URL)
        self.search(searchQuery)
        
        # Get apartments data from first page
        try:
            dataContainer = self.page.wait_for_selector('script#__NEXT_DATA__', state='attached', timeout=25000)
            dataFromDOM = json.loads(dataContainer.inner_text())
            data = extractData(dataFromDOM, CatalogDomExtractor)
            allApartments.extend(data)
        except:
            pass
        
        # Collect data from next pages
        try:
            while True:
                with self.page.expect_response(lambda response: fetchResponse(response), timeout=10000) as response_info:
                    response = response_info.value
                response_json = response.json()
                data = extractData(response_json, CatalogExtractor)
                allApartments.extend(data)

                if self.page.locator('a[title="Next page"]').is_disabled():
                    break
                
                self.page.wait_for_timeout(rateLimiter(requestsPerMin))
                self.page.locator('a[title="Next page"]').click()
        finally:
            with open(pathToSave, 'w') as f:
                json.dump(allApartments, f, indent=4)

                # Save path of that file to use it in detail scraping
                self.pathToDataFile = os.path.realpath(f.name)

    def run(self, *args, mode='main', **kwargs):
        with Stealth().use_sync(sync_playwright()) as playwright:
            self.browser = playwright.chromium.launch(headless=False)
            self.page = self.browser.new_page()
            self.page.route("**/*", lambda route, request: 
               route.abort() if request.resource_type in ["image", "media", "font", "stylesheet"] 
               else route.continue_()
            )

            if mode == 'main':
                self.scrape(*args, **kwargs)
            elif mode == 'detail':
                print(1)
                self.getDetailInfo(*args, **kwargs)

            self.browser.close()

    def getDetailInfo(self, urlList = None, filePath = None, pathToSave = './detail_data.json'):
        if filePath is None:
            filePath = self.pathToDataFile

        if urlList is None:
            if filePath is None:
                return None
            with open(filePath, 'r') as f:
                data = json.load(f)
            urlList = [item['url'] for item in data]
        print(urlList)
        # Now start scraping
        detailInfo = []

        for i, url in enumerate(urlList):
            try:
                self.page.goto(url, wait_until="domcontentloaded")
                dataContainer = self.page.wait_for_selector('script#__NEXT_DATA__', state='attached', timeout=25000)
                data = json.loads(dataContainer.inner_text())
                
                detailData = extractData(data, DetailDOMExtractor)
                detailInfo.append(detailData)
            except Exception as e:
                print(f'{i} failed', e)
            
            self.page.mouse.wheel(0, 1000)
            self.page.wait_for_timeout(rateLimiter(13))

        with open(pathToSave, 'w') as f:
            json.dump(detailInfo, f, indent=4)

        print('Success')
        print(len(detailInfo))

        
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
    scraper.run(mode='detail', filePath='./data.json')