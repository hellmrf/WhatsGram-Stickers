import os
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WhatsGramSticker:
    def __init__(self):
        # Configuration
        self._chromedriver = os.path.join(os.path.dirname(__file__), "chromedriver")
        self._profile_path = os.path.join(os.path.dirname(__file__), "chromeprofile")
        self._headless = False
        
        # Starting webdriver
        self._profile = webdriver.ChromeOptions()
        self._profile.add_argument("user-data-dir=%s" % self._profile_path)
        if self._headless:
            self._profile.add_argument("headless")
        self.driver = webdriver.Chrome(self._chromedriver, chrome_options=self._profile)
        self.driver.get("https://web.whatsapp.com")
