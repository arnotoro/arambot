import requests
import json
from dotenv import load_dotenv
import os
from jsonParse import returnChampionData

from lolalytics_webscraper import get_champion_data 


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
    # return championIDs
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
    # change names of the champions lower case
    for champion in data:
        data[champion]["id"] = data[champion]["id"].lower()
        if " " in data[champion]["id"]:
            data[champion]["id"] = data[champion]["id"].replace(" ", "")
        # check for dots in name
        if "." in data[champion]["id"]:
            data[champion]["id"] = data[champion]["id"].replace(".", "")
        # check for apostrophes in name
        if "'" in data[champion]["id"]:
            data[champion]["id"] = data[champion]["id"].replace("'", "")

    # iterate through the champions name, winrate and  and crete a json object for each champion
    for champion in data:
        # create a json object for each champion
        championData = get_champion_data(data[champion]["id"])
        print(championData)
        # write the json object to a file
        with open('championData.json', 'a') as outfile:
            json.dump(championData, outfile)


if __name__ == '__main__':
    #sumID = getSummonerID('LateNightSoloQEZ')
    #champIDs = getMatch(sumID)

    #iterate through the array of champion ids and print the champion name
    #for championID in champIDs:
        #print(getChampionName(str(championID)))
    #updateChampionData()
    # object to store the champion data
    champ = 'ahri'
    # create a list to store the champion data
    championData = []
    # call the function to return the champion data
    championData = returnChampionData(champ)
    print(championData)