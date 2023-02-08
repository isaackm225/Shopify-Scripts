from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import os
from os import path
import time

class Bot():
    def __init__(self):
        """set ressources urls"""
        self.path = path.abspath(os.curdir) #folder path
        self.bg_remover = "https://removal.ai/"
        self.upscaler = "https://www.upscale.media/upload"
        self.img_suffix = (".jpeg",".png",".jpg")

    def remove_bg(self):
        options = webdriver.ChromeOptions()
        for img in os.listdir():
            if img.lower().endswith(self.img_suffix):
                print(f"removing bg for: {img}")
                with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
                    driver.maximize_window()
                    wait = WebDriverWait(driver, timeout=30, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException,ElementNotSelectableException,NoSuchElementException])
                    driver.get(self.bg_remover)
                    form = driver.find_element(By.CLASS_NAME, "form-control")
                    form.send_keys(f"{self.path}/{img}")
                    btn = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,"Download")))
                    btn.click()
                    time.sleep(5)
                os.remove(img)

    def upscale(self):
        options = webdriver.ChromeOptions()
        for img in os.listdir():
            if img.lower().endswith(self.img_suffix):
                print(f"processing: {img}")
                with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
                    driver.maximize_window()
                    wait = WebDriverWait(driver, timeout=30, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException,ElementNotSelectableException,NoSuchElementException])
                    driver.get(self.upscaler)
                    form = wait.until(EC.presence_of_element_located((By.ID, "uploadImage")))
                    form.send_keys(f"{self.path}/{img}")
                    select_element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div[3]/div[2]/div/div[2]/div/div/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/select")))
                    select = Select(select_element)
                    select.select_by_value("4x")
                    #working on toggling to enheance pic quality
                    #toggle_div = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "hIlDCJ")))
                    #toggle = toggle_div.find_element(By.TAG_NAME, "input")
                    #driver.execute_script("arguments[0].setAttribute('checked','checked')",toggle)
                    btn = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/div[1]/div[3]/div[2]/div/div[2]/div/div/div[3]/div[1]/div[2]/div[2]/div[2]/button")))
                    btn.click()
                    time.sleep(10)
                os.remove(img)

if __name__=="__main__":
    "debugging code note that the bot removes the file after processing"
    bot = Bot()
    #bot.remove_bg() #uncomment and run to test
    bot.upscale() #uncomment and run to test
    