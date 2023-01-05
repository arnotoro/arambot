import os
import discord
import discord.ext
import asyncio

from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions

from jsonParse import returnChampionData
from lolalyticsWebscraper import *
from riotApi import *


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents,command_prefix='!')

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@bot.command()
async def ping(ctx, help="Ping the bot"):
    await ctx.send('pong')

# function to get the champion stats from local json file
@bot.command()
async def champ(ctx, champion_name, help="Get the champion stats from recent patch"):
    # create an object to store the champion data
    championData = []
    championData = returnChampionData(champion_name)
    print(championData)
    await ctx.send(f'Champion: {championData["name"].capitalize()}\nWinrate: {championData["winrate"]}\nPickrate: {championData["pickrate"]}\nBanrate: {championData["banrate"]}')

# function to get the games champion names and add reactions to the message based on the summoner name
@bot.command()
async def game(ctx, summoner_name, help="Get the champion names from the game"):
    reactionData = {}
    summonerID = getSummonerID(summoner_name)
    championIDs = getMatch(summonerID)
    blueSide = "\n".join(
        (getChampionName(str(championName))) for ind, championName in enumerate(championIDs) if ind < 5)
    redSide = "\n".join(
        (getChampionName(str(championName))) for ind, championName in enumerate(championIDs) if ind >= 5)

    message = str("**🔵 Team Blue (bot side) 🔵**\n```yaml\n" + blueSide + "```\n" + "**🔴 Team Red (top side) 🔴**\n```arm\n" + redSide + "```" + "\n*React with 🔵 if you think the blue team will win or 🔴 if you think the red team will win* \n")

    sentMessage = await ctx.send(message)
    await sentMessage.add_reaction('🔵')
    await sentMessage.add_reaction('🔴')

    await asyncio.sleep(5)
    msgAfterReactions = await ctx.channel.fetch_message(sentMessage.id)

    countBlue = msgAfterReactions.reactions[0].count
    countRed = msgAfterReactions.reactions[1].count
    if countBlue > countRed:
        await ctx.send(f'*Blue team (🔵) wins with {((countBlue-countRed)/countRed)*100:.2f}% of votes!*')
    elif countBlue < countRed:
        await ctx.send(f'*Red team (🔴) wins with {((countRed-countBlue)/countBlue)*100:.2f}% of votes!*')
    else:
        await ctx.send('''*It's a draw!*''') 

    # save results to object 
    reactionData["summonerName"] = summoner_name
    reactionData["blueSideIDs"] = championIDs[:5]
    reactionData["blueSideChampions"] = [getChampionName(str(championName)) for ind, championName in enumerate(championIDs) if ind < 5]
    reactionData["countBlueReactions"] = countBlue -1
    reactionData["redSideIDs"] = championIDs[5:]
    reactionData["redSideChampions"] = [getChampionName(str(championName)) for ind, championName in enumerate(championIDs) if ind >= 5]
    reactionData["countRedReactions"] = countRed -1

    # write results to json file
    with open('champions/reactionData.json', "a") as file:
        json.dump(reactionData, file, indent=4)

    print("Game analysis done!")

# dev testing command
@bot.command()
@has_permissions(kick_members=True)
async def update(ctx, help="Update the champion data"):
    await ctx.send('Updating champion data...')
    updateChampionData()
    await ctx.send('Champion data has been updated')

@update.error
async def update_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have the permission to do that")

bot.run(TOKEN)