import discord
from discord.ext import commands
import asyncio

# code for verification

class verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="This commands helps you get verified for this server")
    async def verify(self, ctx, arg=None):
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

            # need to send an email now to the people
            # probably also need to move this into a separate file

            try:
                msg = await self.bot.wait_for('message', check=is_zID_correct, timeout=15)
                await ctx.send("Thanks, we will send an verification code to your UNSW email, please just reply to me with your verification code. There will be a 2 minute timer for the verification code")
                msg = await self.bot.wait_for('message', timeout=120)
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond. If you still want to verify your status on the server please use the verify command again. Thanks.")
            except Exception as e:
                print(e)
        else:
            await ctx.send("This command only works in a DM, please message the bot directly to get verified.")


def setup(bot):
    bot.add_cog(verification(bot))