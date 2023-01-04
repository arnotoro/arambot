import requests
import json
from dotenv import load_dotenv
import os
from jsonParse import returnChampionData

from lolalyticsWebscraper import *


load_dotenv()

RIOT_API = os.getenv('RIOT_API')


def getSummonerID(summonerName):
    api1 = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={RIOT_API}'
    res = requests.get(api1)
    summonerID = json.loads(res.text)["id"]
    return summonerID


def getMatch(summonerID):
    api = f'https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summonerID}?api_key={RIOT_API}'    
    # array to store champion ids
    championIDs = []

    res2 = requests.get(api)
    for player in json.loads(res2.text)["participants"]:
        for value in player:
            if value == 'championId':
                championIDs.append(player[value])
    return championIDs

def getChampionName(championID):
    api = f'http://ddragon.leagueoflegends.com/cdn/12.23.1/data/en_US/champion.json'
    res = requests.get(api)
    data = json.loads(res.text)["data"]
 
    for champion in data:
        if data[champion]["key"] == championID:
           return data[champion]["id"]

def updateChampionData():
    api = f'https://ddragon.leagueoflegends.com/cdn/12.23.1/data/en_US/champion.json'
    res = requests.get(api)
    data = json.loads(res.text)["data"]

    # my monkeyking need special treatment
    data["Wukong"] = data.pop("MonkeyKing")

    # print champions
    for champion in data:
        print(champion.lower())

    # iterate through the champions name, winrate and  and crete a json object for each champion
    # for champion in data:
    championData = getChampionStats(champion.lower() for champion in data)
    with open('champions/championData.json', 'w') as outfile:
            json.dump(championData, outfile, indent=4)


if __name__ == '__main__':
    updateChampionData()
