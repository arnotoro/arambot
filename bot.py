import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from jsonParse import returnChampionData
from lolalytics_webscraper import *
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

@bot.command()
async def champ(ctx, champion_name, help="Get the champion stats from recent patch"):
    # create an object to store the champion data
    championData = []
    championData = returnChampionData(champion_name)
    await ctx.send(f'Champion: {championData["name"].capitalize()}\nWinrate: {championData["winrate"]}\nPickrate: {championData["pickrate"]}\nBanrate: {championData["banrate"]}')

@bot.command()
async def game(ctx, summoner_name, help=""):
    summonerID = getSummonerID(summoner_name)
    championIDs = getMatch(summonerID)
    championNames = []
    for champion in championIDs:
        championNames.append(getChampionName(str(champion)))
    await ctx.send(' '.join(championNames))

# @bot.command()
# async def update(ctx, help="Update the champion data"):
#     updateChampionData()
#     await ctx.send('Champion data has been updated')


bot.run(TOKEN)