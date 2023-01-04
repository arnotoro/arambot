import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from data_fetcher import returnChampionData
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

# function to get the champion stats from local json file
@bot.command()
async def champ(ctx, champion_name, help="Get the champion stats from recent patch"):
    championData = {}
    championData = returnChampionData(champion_name)
    await ctx.send(f'Champion: {championData["id"]}\nWinrate: {championData["winrate"]}\nPickrate: {championData["pickrate"]}\nBanrate: {championData["banrate"]}')

# function to get the games champion names and add reactions to the message based on the summoner name
@bot.command()
async def game(ctx, summoner_name, help="Get the champion names from the game"):
    summonerID = getSummonerID(summoner_name)
    championIDs = getMatch(summonerID)
    championNames = []
    for champion in championIDs:
        championNames.append(getChampionName(str(champion)))
    message = await ctx.send(' '.join(championNames))
    # tested
    await message.add_reaction('🔵')
    await message.add_reaction('🔴')

bot.run(TOKEN)