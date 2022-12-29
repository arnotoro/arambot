import requests
import json

def getSummonerID(summonerName):
    api1 = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key=RGAPI-052be87f-343a-4b38-baa5-72ade8533fe9'
    res = requests.get(api1)
    summonerID = json.loads(res.text)["id"]
    return summonerID


def getMatch(summonerID):
    api = f'https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summonerID}?api_key=RGAPI-052be87f-343a-4b38-baa5-72ade8533fe9'    
    

    res2 = requests.get(api)
    for player in json.loads(res2.text)["participants"]:
        for value in player:
            if value == 'championId':
                print(player[value])


def main():
    sumID = getSummonerID('tpupper')
    getMatch(sumID)



main()



