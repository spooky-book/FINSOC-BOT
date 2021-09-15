import discord
from discord.ext import commands
from dotenv import load_dotenv
from extensions.gmail import create_gmail_service
import os

load_dotenv()
client = commands.Bot(command_prefix=".")
token = os.getenv("DISCORD_BOT_TOKEN")
# token = os.getenv("mytestingtoken")

extensions=["verify"]

# loads in the extensions that we have made into the bot
if __name__ == "__main__":
    for extension in extensions:
        client.load_extension(f"extensions.{extension}")

@client.event
async def on_ready() :
    await client.change_presence(status = discord.Status.active, activity = discord.Game("Crash the Stock Market"))
    print("I am online")

@client.command()
async def ping(ctx) :
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

@client.command(brief="Tells you who you are")
async def whoami(ctx) :
    await ctx.send(f"You are {ctx.message.author.name}")

# @client.command()
# async def clear(ctx, amount=3) :
#     await ctx.channel.purge(limit=amount)


client.run(token)