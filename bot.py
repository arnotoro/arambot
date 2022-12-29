import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
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
    await ctx.send(get_champion_data(champion_name))

@bot.command()
async def game(ctx, summoner_name, help=""):
    summonerID = getSummonerID(summoner_name)
    championIDs = getMatch(summonerID)
    championNames = []
    for champion in championIDs:
        championNames.append(getChampionName(str(champion)))

    await ctx.send(' '.join(championNames))


bot.run(TOKEN)