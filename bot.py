import os
import discord
import discord.ext
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
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
    print(championData)
    await ctx.send(f'Champion: {championData["name"].capitalize()}\nWinrate: {championData["winrate"]}\nPickrate: {championData["pickrate"]}\nBanrate: {championData["banrate"]}')

@bot.command()
async def game(ctx, summoner_name, help=""):
    summonerID = getSummonerID(summoner_name)
    championIDs = getMatch(summonerID)
    message = str("**Team 1**\n```arm\n" + "\n".join(
        (getChampionName(str(championName))) for ind, championName in enumerate(championIDs) if ind < 5) + "```\n" + "**Team 2**\n```yaml\n" + "\n".join(
        (getChampionName(str(championName))) for ind, championName in enumerate(championIDs) if ind >= 5)+ "```")

    await ctx.send(message)

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