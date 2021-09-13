import discord
from discord.ext import commands
from discord.utils import get

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

    '''
        Authenticates a user using their zID to ensure that they are part of UNSW
        This is only the automatic verification system, if other people want to join they can manually ask FINSOC committee members

        Asks use for their zID, creates and sends a verification code via email to the individuals UNSW email.
        Bot will use this verification code to verify the individual and grant them the VERIFIED role in the FINSOC Guild
    '''
    @commands.command(brief="This commands helps you get verified for this server")
    async def verify(self, ctx, arg=None):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send("Hello, I will help you get verified on the server.")
            await ctx.send("Please enter your zID without the z")

            def not_bot(message):
                if ctx.author == message.author and ctx.channel == message.channel:
                    return True
                else:
                    return False

            # TODO maybe be able to continue entering zid without writing .verify

            try:
                message = await self.bot.wait_for('message', check=not_bot, timeout=15.0)
                zID = message.content.strip()

                if zID.isdigit() and len(zID) == 7:
                    await ctx.send("Thanks, we will send an verification code to your UNSW email, please just reply to me with your verification code. There will be a 2 minute timer for the verification code")

                else:
                    await ctx.send("Make sure you have entered your zID correctly. Please restart process to try again.")
                    return


                print("Message Content (zID):", message.content)
                print("Message Author:", message.author)

                OTP = self.create_verification_code()

                email_successful = self.send_email(zID, OTP)

                if email_successful:
                    password = await self.bot.wait_for('message', check=not_bot, timeout=120.0)
                    if OTP == password.content.strip():
                        # grabs the UNSW finsoc server using guildID
                        guild_ID = int(os.getenv("FINSOC_GUILD_ID"))

                        myguild = self.bot.get_guild(guild_ID)
                        role = myguild.get_role(869547973095333928)

                        member = await myguild.fetch_member(password.author.id)

                        await member.add_roles(role, reason="passed verification system")
                        await ctx.send("Verified, you can now interact on the server")

                    else:
                        await ctx.send("Verification Code not accepted please repeat the process to get verified.")

                else:
                    await ctx.send("Something went wrong when sending your verification code, please try again. If this is recurring try waiting before contacting IT")

            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond. If you still want to verify your status on the server please use the verify command again. Thanks.")

            except Exception as e:
                print(e)
                await ctx.send("Something went wrong, please try again. If this keeps happening please wait then contact FINSOC IT. Thank you. :)")

        else:
            await ctx.send("This command only works in a DM, please message the bot directly to get verified.")

    # TODO we need to be able to create a blacklist that prevents people from reverification after banning
    # they will have to directly message execs to get unblacklisted might not be top priority
    def send_email(self, zID, OTP):
        try:
            server = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465, context=ssl.create_default_context())

            password = os.getenv("finsoc_bot_pass")
            server.login("unswfinsocbot@gmail.com", password)
            receiver_email = 'z' + zID + "@ad.unsw.edu.au"

            message = MIMEMultipart('alternative')

            message['From'] = "unswfinsocbot@gmail.com"
            message['To'] = receiver_email
            message['Subject'] = 'FINSOC Discord Verification'

            texts = create_email_message_text(OTP)

            msg_text = texts[0]

            html_text = texts[1]

            converted_msg_text = MIMEText(msg_text, 'plain')
            converted_html_text = MIMEText(html_text, 'html')

            message.attach(converted_msg_text)
            message.attach(converted_html_text)

            server.sendmail("unswfinsocbot@gmail.com", receiver_email, message.as_string())

            return True
        except Exception as email_exception:
            print(email_exception)
            return False
        finally:
            server.close()

    # creates the verification code that the user needs to input to verify themselves
    def create_verification_code(self):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(8))

    def create_email_message_text(self, OTP):
        msg_text = f'''
                \
                Hello,

                Below is your verification code, please reply to the bot in your DM channel to get verified.

                {OTP}

                Thank you.'''

        html_text = f'''
                \
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

        return [msg_text, html_text]


def setup(bot):
    bot.add_cog(verification(bot))