import discord
from discord.ext import commands
import asyncio
import smtplib
import ssl
import os
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

            # there is currently a bug im pretty sure in which the client.wait for picks up the bots own message and uses that
            # probs need some checks or something idk not sure if its actually fixed

            # i also currently need to create an error message when the input is wrong however it shouldnt end the command i.e. we should be able to continue entering zid without writing .verify

            try:
                msg = await self.bot.wait_for('message', check=is_zID_correct, timeout=15)
                await ctx.send("Thanks, we will send an verification code to your UNSW email, please just reply to me with your verification code. There will be a 2 minute timer for the verification code")
                print(msg)
                self.send_email(msg)
                msg = await self.bot.wait_for('message', timeout=120)
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond. If you still want to verify your status on the server please use the verify command again. Thanks.")
            except Exception as e:
                print(e)
        else:
            await ctx.send("This command only works in a DM, please message the bot directly to get verified.")

    # we need to be able to create a blacklist that prevents people from reverification after banning
    # they will have to directly message execs to get unblacklisted
    # might not be top priority
    def send_email(self, zID):
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

                {self.create_verification_code()}

                Thank you.'''

            html_text = f'''\
                <html>
                    <body>
                        <p>
                            Hello,
                            <br>
                            <br>
                            Below is your verification code, please reply to the bot in your DM channel to get verified.

                            <h3>{self.create_verification_code()}</h3>

                            Thank you.
                        </p>
                    </body>
                </html>'''

            converted_msg_text = MIMEText(msg_text, 'plain')
            converted_html_text = MIMEText(html_text, 'html')

            message.attach(converted_msg_text)
            message.attach(converted_html_text)

            server.sendmail("unswfinsocbot@gmail.com", receiver_email, message.as_string())

            # password = os.getenv("finsoc_bot_pass")
            # # print(password)
            # server.login("unswfinsocbot@gmail.com", password)
            # receiver_email = 'z' + zID.content + "@student.unsw.edu.au"
            # # print(receiver_email)
            # message = '''\
            #     Subject: Test 2

            #     testing blah blah blah'''
            # server.sendmail("unswfinsocbot@gmail.com", receiver_email, message)

    def create_verification_code(self):
        pass


def setup(bot):
    bot.add_cog(verification(bot))