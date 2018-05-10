import discord
import sys
import time
import threading
import queue
#import youtube_dl
import asyncio
TOKEN = ''
client = discord.Client()
prefix = '|'
que = queue.Queue(maxsize=5)
#global voiceConnection
@client.event
async def on_ready():
    print('----------------------Boot Info-----------------------')
    print(loginInfo())
    print('------------------------------------------------------')

@client.event
async def on_message(message):
    global player
    if message.content.startswith(prefix + 'put'):
        que.put('https://www.youtube.com/watch?v=pxAiwZlzSD8')
        print('added to que')
    elif message.content.startswith(prefix + 'play'):
        #pulls youtube link out of message... check function extractURL() for details
        youtubeLink = extractURL(message)
        que.put(youtubeLink)
        msg = discordLog.play
        await client.send_message(message.channel, msg)
        print(consoleLog.play)
    #pauses what the client(bot) is playing
    elif message.content.startswith(prefix + 'pause'):
        player.pause()
        msg = discordLog.pause
        await client.send_message(message.channel, msg)
        print(consoleLog.pause)
    #resumes what the client(bot) was playing
    elif message.content.startswith(prefix + 'resume'):
        player.resume()
        msg = discordLog.resume
        await client.send_message(message.channel, msg)			
        print(consoleLog.resume)
    elif message.content.startswith(prefix + 'skip'):
        player.stop()
        msg = discordLog.skip
        await client.send_message(message.channel, msg)
        print(consoleLog.skip)
    #stops what the client(bot) is playing
    elif message.content.startswith(prefix + 'stop'):
        player.stop()
        msg = discordLog.stop
        await client.send_message(message.channel, msg)
        print(consoleLog.stop)
    #clears everything from the queue
    elif message.content.startswith(prefix + 'clear'):
        client.loop.create_task(background_task_clear_queue())
        msg = discordLog.clear
        await client.send_message(message.channel, msg)
        print(consoleLog.clear)
    elif message.content.startswith(prefix + 'join'):
        currentChannel = client.get_channel(message.author.voice_channel.id)
        voiceConnection = await client.join_voice_channel(currentChannel)
        client.loop.create_task(my_background_task(voiceConnection))
        msg = 'What\'s up dudes :call_me::skin-tone-5:'
        await client.send_message(message.channel, msg)
    #disconnects client(bot) from voice channel
    elif message.content.startswith(prefix + 'disconnect'):
        if client.is_voice_connected(message.server):
            currentChannel = client.voice_client_in(message.server)
            await currentChannel.disconnect()
            msg = discordLog.disconnect
            await client.send_message(message.channel, msg)

def loginInfo():
    if client.is_logged_in == True:
        status ='Logged in as: ' + client.user.name + '\nWith user ID of: ' + client.user.id
        return status
    else:
        return 'Not logged in'
async def background_task_clear_queue():
    await client.wait_until_ready()
    while not que.empty():
        que.get()

async def my_background_task(voiceConnection):
    global player
    isPlaying = False
    await client.wait_until_ready()
    while voiceConnection.is_connected():
        if not que.empty() and isPlaying == False:
            print('que not empty')
            player = await voiceConnection.create_ytdl_player(que.get())
            player.start()
            #await client.send_message(message.channel, discordLog.playing + player.title)
        await asyncio.sleep(1) # task runs every 1 seconds
        try:
            isPlaying = player.is_playing()
        except:
            pass
def extractURL(msg):
	temp = msg.content.split(' ', 1)
	url = temp[1]
	return url
class discordLog:
    play = ':white_check_mark: I\'ve added your request to the queue.'
    playing = ':musical_note: Currently Playing: '
    stop = ':stop_button: I have stopped playing the song.'
    pause = ':pause_button: I have paused the song. Type "|resume" to continue where I left off.'
    resume = ':arrow_forward: I am resumming the song where we last left off.'
    clear = ':x: I have cleared the queue.'
    skip = ':track_next: I have skipped the song.'
    disconnect = ':v::skin-tone-5: Later guys.'
class consoleLog:
    play = '|play command issued: Player is playing'
    stop = '|stop command issued: Stopped playing'
    pause = '|pause command issued: Player is paused'
    resume = '|resume command issued: Player resumed'
    join = '|join command issued: Attempting to join chat'
    joined = 'Joined chat successfully'
    clear = '|clear command issued: Queue is not cleared'
    skip = '|skip command issued: Skipping song'
#client.loop.create_task(my_background_task())
client.run(TOKEN)