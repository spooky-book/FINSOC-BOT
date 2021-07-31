import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
client = commands.Bot(command_prefix=".")
# token = os.getenv("DISCORD_BOT_TOKEN")
token = os.getenv("mytestingtoken")


@client.event
async def on_ready() :
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("Listening to .help"))
    print("I am online")

@client.command()
async def ping(ctx) :
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

@client.command(name="whoami")
async def whoami(ctx) :
    await ctx.send(f"You are {ctx.message.author.name}")

@client.command()
async def clear(ctx, amount=3) :
    await ctx.channel.purge(limit=amount)

@client.command()
async def verify(ctx, arg=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send("Hello, I will help you get verified on the server.")
        await ctx.send("Please enter your zID without the z")

        def is_zID_correct(message):
            if not(ctx.author == message.author and ctx.channel == message.channel):
                return False

            id = message.content.strip()

            if id.isdigit() and len(id) == 7:
                return True
            else:
                # ctx.send("Make sure you have entered your zID correctly")
                return False

        # there is currently a bug im pretty sure in which the client.wait for picks up the bots own message and uses that
        # probs need some checks or something idk

        # i also currently need to have an error message when the input is wrong however it shouldnt end the command i.e. we should be able to continue entering zid without writing .verify

        try:
            msg = await client.wait_for('message', check=is_zID_correct, timeout=15)
            await ctx.send("Thanks, we will send an verification code to your UNSW email, please just reply to me with your verification code. There will be a 2 minute timer for the verification code")
            msg = await client.wait_for('message', timeout=120)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond. If you still want to verify your status on the server please use the verify command again. Thanks.")
        except Exception as e:
            print(e)
    else:
        await ctx.send("This command only works in a DM, please message the bot directly to get verified.")


client.run(token)