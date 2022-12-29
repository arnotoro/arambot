import requests
import json
from dotenv import load_dotenv
import os 


load_dotenv()

RIOT_API = os.getenv('RIOT_API')


def getSummonerID(summonerName):
    api1 = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={RIOT_API}'
    res = requests.get(api1)
    summonerID = json.loads(res.text)["id"]
    return summonerID


def getMatch(summonerID):
    api = f'https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summonerID}?api_key={RIOT_API}'    
    

    res2 = requests.get(api)
    for player in json.loads(res2.text)["participants"]:
        for value in player:
            if value == 'championId':
                print(player[value])


def main():
    sumID = getSummonerID('tpupper')
    getMatch(sumID)



main()



