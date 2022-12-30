import json

def returnChampionData(championName):
    # create an object to store the champion data
    championData = {}
    with open('championData.json', "r") as f:
        data = json.loads(f.read())
        # go through the data and find the champion name and three stats and insert them into the championData object
        for champion in data:
            if champion["name"] == championName:
                championData["name"] = champion["name"]
                championData["winrate"] = champion["winrate"]
                championData["pickrate"] = champion["pickrate"]
                championData["banrate"] = champion["banrate"]
                break
    return championData