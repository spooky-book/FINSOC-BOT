import discord
from discord.ext import commands

import asyncio
import smtplib
import ssl
import os
import secrets
import string

from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# code for verification
class verification(commands.Cog):
    def __init__(self, bot):
        load_dotenv()
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

            def is_OTP_correct(message):
                if not(ctx.author == message.author and ctx.channel == message.channel):
                    return False
                else:
                    return True

            # there is currently a bug im pretty sure in which the client.wait for picks up the bots own message and uses that
            # probs need some checks or something idk not sure if its actually fixed

            # i also currently need to create an error message when the input is wrong however it shouldnt end the command i.e. we should be able to continue entering zid without writing .verify

            try:
                ID = await self.bot.wait_for('message', check=is_zID_correct, timeout=15.0)
                await ctx.send("Thanks, we will send an verification code to your UNSW email, please just reply to me with your verification code. There will be a 2 minute timer for the verification code")
                print(ID.content)
                print(ID)

                OTP = self.create_verification_code()

                await self.send_email(ID, OTP)
                password = await self.bot.wait_for('message', timeout=120.0)

                if OTP == password.content.strip():
                    # insert verification code here
                    await ctx.send("Verified, you can now interact on the server")
                else:
                    await ctx.send("Verification Code not accepted please repeat the process to get verified.")


            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond. If you still want to verify your status on the server please use the verify command again. Thanks.")
            except Exception as e:
                print(e)
        else:
            await ctx.send("This command only works in a DM, please message the bot directly to get verified.")

    # we need to be able to create a blacklist that prevents people from reverification after banning
    # they will have to directly message execs to get unblacklisted
    # might not be top priority
    def send_email(self, zID, OTP):
        with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465, context=ssl.create_default_context()) as server:
            password = os.getenv("finsoc_bot_pass")
            server.login("unswfinsocbot@gmail.com", password)
            receiver_email = 'z' + zID.content + "@ad.unsw.edu.au"

            message = MIMEMultipart('alternative')

            message['From'] = "unswfinsocbot@gmail.com"
            message['To'] = receiver_email
            message['Subject'] = 'FINSOC Discord Verification'

            msg_text = f'''\
                Hello,

                Below is your verification code, please reply to the bot in your DM channel to get verified.

                {OTP}

                Thank you.'''

            html_text = f'''\
                <html>
                    <body>
                        <p>
                            Hello,
                            <br>
                            <br>
                            Below is your verification code, please reply to the bot in your DM channel to get verified.

                            <h3>{OTP}</h3>

                            Thank you.
                        </p>
                    </body>
                </html>'''

            converted_msg_text = MIMEText(msg_text, 'plain')
            converted_html_text = MIMEText(html_text, 'html')

            message.attach(converted_msg_text)
            message.attach(converted_html_text)

            server.sendmail("unswfinsocbot@gmail.com", receiver_email, message.as_string())

    # creates the verification code that the user needs to input to verify themselves
    def create_verification_code(self):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(8))


def setup(bot):
    bot.add_cog(verification(bot))