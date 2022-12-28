from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import re

def get_champion_data(champion_name):
    # TODO HEADLESS MODE
    #firefox_options = Options()
    #firefox_options.add_argument("--headless")
    driver = webdriver.Firefox()

    driver.get(f'https://lolalytics.com/lol/{champion_name}/build')
    cls = re.compile('ChampionStats.+')

    try:
        # champion stats div
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[4]/div[1]/div[2]/div[2]"))
        )
        
        # get current patch number
        getPatch = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div[4]/div/div/div"))
        )

        patch = getPatch.text
        # parse champion stats
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        results = soup.find_all('div', class_=cls)

        for result in results:
            stats = result.find_all('div')
            winrate = stats[1].text
            pickrate = stats[8].text
            banrate = stats[10].text

    finally:
        driver.quit()

        #res = f'Patch: {patch.text} \\ Winrate: {winrate}, Pickrate: {pickrate}, Banrate: {banrate}'
        print(winrate, pickrate, banrate)
        return f'Patch: {patch} \\ Champion: {champion_name.capitalize()}, Winrate: {winrate}, Pickrate: {pickrate}, Banrate: {banrate}'