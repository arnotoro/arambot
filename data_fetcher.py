import json

def returnChampionData(championName):
    # create an object to store the champion data
    championData = {}
    with open('championData.json', "r") as f:
        data = json.loads(f.read())
        # go through the data and find the champion name and three stats and insert them into the championData object
        for champion in data:
            if data[champion]["id"] == championName:
                championData["id"] = data[champion]["id"]
                championData["winrate"] = data[champion]["winrate"]
                championData["pickrate"] = data[champion]["pickrate"]
                championData["banrate"] = data[champion]["banrate"]
                break
    return championData