from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

def getChampionData(driver, championName):
    driver.get(f'https://lolalytics.com/lol/{championName}/build')
    cls = re.compile('ChampionStats.+')
    # create an object to store champion stats
    championStats = {}
    try:
        # champion stats div
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[4]/div[1]/div[2]/div[2]"))
        )
        
        # get current patch number
        getPatch = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div[4]/div/div/div"))
        )

        patch = getPatch.text
        # parse champion stats
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        results = soup.find_all('div', class_=cls)
        for result in results:
            stats = result.find_all('div')
            #store champion stats in object
            championStats['name'] = championName
            championStats['winrate'] = stats[1].text
            championStats['pickrate'] = stats[8].text
            championStats['banrate'] = stats[10].text

    except:
        print('Error')
    finally:
        print(stats[1].text, stats[8].text, stats[10].text)
        return championStats

def initDriver(championList):
    driver = webdriver.Firefox()
    championStatList = []
    for champion in championList:
        championStatList.append(getChampionData(driver, champion))
    print(championStatList)
    driver.quit()

    return championStatList