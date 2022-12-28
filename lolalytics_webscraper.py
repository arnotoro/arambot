from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def get_champion_data(champion_name):
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    
    driver.get(f'https://lolalytics.com/lol/{champion_name}/build')
    cls = re.compile('ChampionStats_stats.+')

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

        #res = f'Patch: {patch.text} \n Winrate: {winrate}, Pickrate: {pickrate}, Banrate: {banrate}'
        return f'Patch: {patch} \\ Winrate: {winrate}, Pickrate: {pickrate}, Banrate: {banrate}'