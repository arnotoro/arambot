from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

def searchChampion(driver, championName):
    #driver.get(f'https://lolalytics.com/lol/{championName}/build')
    driver.get(f'https://www.metasrc.com/5v5/champion/{championName}')
    # regex to find champion stats div
    cls = re.compile(r'_fcip6v.*')
    # create an object to store champion stats
    championStats = {}
    try:
        # # champion stats div
        # WebDriverWait(driver, 5).until(
        #     EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[4]/div[1]/div[2]/div[2]"))
        # )

        # get champion stats div
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div[2]/div/div[1]/div/div[1]/div/div[2]/div[3]/div[1]"))
        )
        
        # # get current patch number
        # getPatch = WebDriverWait(driver, 5).until(
        #     EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div[4]/div/div/div"))
        # )

        # patch = getPatch.text
        # parse champion stats
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # find cls in soup and save values inside divs named _dxv0e1
        results = soup.find_all('div', class_=cls)

        #TODO: find a way to iterate through the results and get the values inside the divs
        print(results)
        # for result in results:
        #     stats = result.find_all('div')
        #     print(stats)
        #     #store champion stats in object
        #     # championStats['name'] = championName
        #     # championStats['winrate'] = stats[1].text
        #     # championStats['pickrate'] = stats[8].text
        #     # championStats['banrate'] = stats[10].text

    except:
        print('Error')
    finally:
        return championStats

def getChampionStats(championList):
    driver = webdriver.Firefox()
    championStatList = []
    for champion in championList:
        championStatList.append(searchChampion(driver, champion))
    print(championStatList)
    driver.quit()

    return championStatList

# main
if __name__ == '__main__':
    # create an list
    champs = []
    driver = webdriver.Firefox()
    # insert aatrox into the list
    champs.append('aatrox')
    searchChampion(driver, champs[0])