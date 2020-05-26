from selenium import webdriver

from app.plugins.adultscraperx.internel import config


class BrowserTools:
    browser = None
    display = None

    def getBrowser(self):

        if config.BROWSER_DRIVE is 'firefox':
            from selenium.webdriver.firefox.options import Options
            firefox_opt = Options()
            firefox_opt.headless = True
            self.browser = webdriver.Firefox(options=firefox_opt)
        if config.BROWSER_DRIVE is 'chrome':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            self.browser = webdriver.Chrome(chrome_options=chrome_options)

        return self.browser

    def closeBrowser(self):
        self.browser.close()
