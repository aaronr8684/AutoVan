import sys
import traceback
import discord
import logging
import config

delChannels = ['577171849658630163', '635873087778455583'] # IDs of channels to watch for delete (prod)
# delChannels = ['635873087778455583'] # IDs of channels to watch for delete (test)
delDelay = 43200.0 # Delay to wait before deleting message (in seconds) - PROD
# delDelay = 5.0 # Delay to wait before deleting message (in seconds) - TEST


logging.basicConfig(level=logging.INFO)

bot = discord.Client()


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    #print('Entering message loop - {} / {}'.format(message.author, message.channel.id))
    if message.author == bot.user: # Don't operate on this bot's messages
        return

    if message.channel.type != discord.ChannelType.text: # Don't respond to non-text channels (e.g. DMs, voice, group-texts)
        # TODO - Add witty response
        print("Not a text channel message")
        return

    if str(message.channel.id) in delChannels:
        try:
            await message.delete(delay=delDelay)
        except:
            print("Delete failed for {}'s message - Err: {} / {}".format(message.author, sys.exc_info()[0], sys.exc_info()[1]))
            traceback.print_tb(sys.exc_info()[2])
        else:
            print('Message queued for delete (author): {} ({})'.format(message.content, message.author))
        # print('Deleted message from {}'.format(message.author))

    if message.content.startswith('!ping'):
        await message.channel.send('Pong!')
    if message.content.startswith('!van'):
        await message.channel.send('You have been deleted!')



bot.run(config.DISCORD_API_TOKEN)
