import discum
from discord_webhook import DiscordWebhook
import os
from dotenv import load_dotenv

load_dotenv()
webhookurl = os.getenv('WEB_HOOK_URL')
logintoken = os.getenv('LOGIN_TOKEN')
channeltostalk = os.getenv('CHANNEL_ID')

bot = discum.Client(token=logintoken, log=False)

@bot.gateway.command
def helloworld(resp):
    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))
    if resp.event.message:
        m = resp.parsed.auto()
        guildID = m['guild_id'] if 'guild_id' in m else None #because DMs are technically channels too
        channelID = m['channel_id']
        username = m['author']['username']
        discriminator = m['author']['discriminator']
        contents = m['content']
        fullContents = username + ": " + contents 
        if channelID == channeltostalk :
            webhook = DiscordWebhook(url=webhookurl, content=fullContents)
            response = webhook.execute()
            print("> guild {} channel {} | {}#{}: {} > {}".format(guildID, channelID, username, discriminator, contents, response))
        #print("> guild {} channel {} | {}#{}: {}".format(guildID, channelID, username, discriminator, content))

bot.gateway.run(auto_reconnect=True)