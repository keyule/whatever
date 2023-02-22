import discum
from discord import SyncWebhook
import os
from dotenv import load_dotenv

load_dotenv()
webhookurl = os.getenv('WEB_HOOK_URL')
logintoken = os.getenv('LOGIN_TOKEN')
channeltostalk = os.getenv('CHANNEL_ID')

bot = discum.Client(token=logintoken, log=False)

webhook = SyncWebhook.from_url(webhookurl)

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
        if channelID == channeltostalk :
            #print(m)
            if len(m['embeds']) > 0:
                for i in range(len(m['embeds'])):
                    content = m['embeds'][i]

                    embed = discord.Embed(title="", description="")
                    embed.title = content['title']
                    embed.url = content['url']
                    embed.colour = content['color']
                    embed.description = content['description']
                    embed.set_thumbnail(url=content['thumbnail']['url'])
                    embed.set_image(url=content['image']['url'])
                    embed.set_footer(text=content['footer']['text'], icon_url=content['footer']['icon_url'])
                    embed.set_author(name=content['author']['name'], url=content['author']['url'])

                    if 'fields' in content.keys():
                        for field in content['fields']:
                            name = field['name']
                            value = field['value']
                            embed.add_field(name=name, value=value, inline=field['inline'])

                    webhook.send(embed=embed, username=username)

            if contents != "":
                webhook.send(content=contents, username=username)

            if len(m['attachments']) > 0:
                for attachment in m['attachments']:
                    webhook.send(attachment['url'], username=username)

            print("> guild {} channel   {} | {}#{}: {}".format(guildID, channelID, username, discriminator, contents))

bot.gateway.run(auto_reconnect=True)