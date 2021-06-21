from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Driver:

    def __init__(self):
        self.create_driver()

    def create_driver(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("dom.disable_beforeunload", True)
        profile.set_preference("browser.tabs.warnOnClose", False)

        options = Options()

        gecko_path = './gecko_driver/geckodriver'

        self.driver = webdriver.Firefox(executable_path=gecko_path, firefox_profile = profile, options=options)

    def get_page_source(self):
        return self.driver.page_source

    def follow_link(self, link):
        self.driver.get(link)

    def shutdown(self):
        self.driver.quit()
        self.driver = None

    def find_element_by_class_name(self, name):
        return self.driver.find_element_by_class_name(name)

    def wait_element(self, id):
        WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.ID, id)))
