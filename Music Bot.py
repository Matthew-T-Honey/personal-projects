import nest_asyncio
nest_asyncio.apply()

import discord
from discord.ext import commands
import random
import asyncio
from pytubefix import YouTube, request
import urllib.request
import string
import json
from youtube_search import YoutubeSearch
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


TOKEN="Bot Token Here"


intents = discord.Intents().all()
bot = commands.Bot(command_prefix='-',intents=intents)

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="3aefa9bf214b40c48b93fd68e08aa017", client_secret="7003caa215284f4bbd5eb747387ae86e"))

player=None
status=None
looping=False
vc=None
tc=None

f=open("queue.txt","w")
f.write("")
f.close()

def get_length(length):
    return (str(length//60)+":"+str(length%60).zfill(2) if length<3600 else str(length//3600)+":"+str((length%3600)//60).zfill(2)+":"+str(length%60).zfill(2))

def get_queue():
    f=open("queue.txt","r")
    l=f.readlines()
    f.close()
    queue=[q[:-1] for q in l]
    return queue

async def addtoqueue(link,voicechannel,index=9999):
    f=open("queue.txt","r")
    l=f.readlines()
    f.close()
    l.insert(index,link+"\n")
    f=open("queue.txt","w")
    f.writelines(l)
    f.close()
    if index==0 or len(l)==1:
        await playsong(link,voicechannel)
    else:
        await updateplayer()

async def playnext(voicechannel):
    global player,status,looping,vc,tc
    f=open("queue.txt","r")
    l=f.readlines()
    f.close()
    if len(l)<2 and not looping:
        if len(bot.voice_clients)>0:
            await bot.voice_clients[0].disconnect()
        f=open("queue.txt","w")
        f.write("")
        f.close()
        if player!=None:
            await player.delete()
        player=None
        status=None
        looping=False
        vc=None
        tc=None
    else:
        f=open("queue.txt","w")
        f.writelines(l[1:])
        if looping:
            f.write(l[0])
        f.close()
        if len(l)==1:
            await playsong(l[0][:-1],voicechannel)
        else:
            await playsong(l[1][:-1],voicechannel)

async def playsong(link,voicechannel):
    global status,vc,tc
    attempts=0
    while True:
        try:
            status="Download 0%"
            await updateplayer()
            
            yt = YouTube(link)
            
            stream=yt.streams.filter(only_audio=True).first()
            filesize = stream.filesize
            
            with open('music.mp4', 'wb') as f:
                stream = request.stream(stream.url)
                downloaded = 0
                while True:
                    if status=="Cancelling Download":
                        break
                    chunk = next(stream, None)
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        percentage=round(100*downloaded/filesize,2)
                        if status!="Cancelling Download":
                            status = f'Downloading {percentage}%'
                    else:
                        audio=discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source='music.mp4'),0.1)
                        break
                    await updateplayer()
            
            if status!="Cancelling Download":
                if len(bot.voice_clients)==0:
                    voice = await voicechannel.connect()
                else:
                    voice=bot.voice_clients[0]
                    if voice.channel!=voicechannel:
                        voice = await voicechannel.connect()
                if voice.is_playing():
                    voice.stop()
                
                voice.play(audio)
                vc=voicechannel
                status="Playing Music"
                
            else:
                status="Download Cancelled"
            await updateplayer()
            break
        except Exception as e2:
            log=bot.get_channel(924621513448124426)
            await log.send(e2)
            status="Download Cancelled"
            attempts+=1
            if attempts>2:
                await tc.send("```Error Playing Song, Playing next```",delete_after=10)
                await playnext(voicechannel)
                break
            else:
                await tc.send("```Error Playing Song, Retrying```",delete_after=10)
                
    
async def updateplayer():
    global player,status,looping,vc,tc
    queue=get_queue()
    if queue!=[]:
        titles=[]
        lengths=[]
        for q in queue:
            try:
                titles.append(YouTube(q).title)
                lengths.append(YouTube(q).length)
            except:
                titles.append("Cannot get title")
                lengths.append(0)
        #videos=[YouTube(q) for q in queue]
        embed=discord.Embed(title="Music Player", color=0x0cdae9)
        if len(queue)>0:
            embed.add_field(name="Currently Playing:", value="["+titles[0]+"]("+queue[0]+") ("+get_length(lengths[0])+")", inline=False)
        if len(queue)==1:
            embed.add_field(name="Next up:", value="Nothing in queue", inline=False)
        if len(queue)==2:
            embed.add_field(name="Next up:", value="1. ["+titles[1]+"]("+queue[1]+") ("+get_length(lengths[1])+")", inline=False)
        if len(queue)==3:
            embed.add_field(name="Next up:", value="1. ["+titles[1]+"]("+queue[1]+") ("+get_length(lengths[1])+")\n2. ["+
                        titles[2]+"]("+queue[2]+") ("+get_length(lengths[2])+")", inline=False)
        if len(queue)==4:
            embed.add_field(name="Next up:", value="1. ["+titles[1]+"]("+queue[1]+") ("+get_length(lengths[1])+")\n2. ["+
                        titles[2]+"]("+queue[2]+") ("+get_length(lengths[2])+")\n3. ["+
                        titles[3]+"]("+queue[3]+") ("+get_length(lengths[3])+")", inline=False)
        if len(queue)==5:
            embed.add_field(name="Next up:", value="1. ["+titles[1]+"]("+queue[1]+") ("+get_length(lengths[1])+")\n2. ["+
                        titles[2]+"]("+queue[2]+") ("+get_length(lengths[2])+")\n3. ["+
                        titles[3]+"]("+queue[3]+") ("+get_length(lengths[3])+")\n4. ["+
                        titles[4]+"]("+queue[4]+") ("+get_length(lengths[4])+")", inline=False)
        if len(queue)>5:
            embed.add_field(name="Next up:", value="1. ["+titles[1]+"]("+queue[1]+") ("+get_length(lengths[1])+")\n2. ["+
                        titles[2]+"]("+queue[2]+") ("+get_length(lengths[2])+")\n3. ["+
                        titles[3]+"]("+queue[3]+") ("+get_length(lengths[3])+")\n4. ["+
                        titles[4]+"]("+queue[4]+") ("+get_length(lengths[4])+")\nAnd "+str(len(queue)-5)+" More", inline=False)
        embed.add_field(name="Channel:", value=vc, inline=True)
        embed.add_field(name="Looping:", value=looping, inline=True)
        embed.add_field(name="Status", value=status, inline=True)
        embed.add_field(name="Commands:", value="Play: Play a song/add to the queue\nPlay now: Stop current song and play this at the top of the queue\nRemove x: Remove song x from the queue", inline=False)
                
        if player==None:
            player = await tc.send(embed=embed)
        else:
            await player.edit(embed=embed)

@bot.event
async def on_message(message):
    global tc,status,vc,looping,player
    if message.author!=bot.user:
        if not message.author.bot:
            if message.content.lower()=="debug":
                print(tc,vc,status,looping)
                print(player)
                print(get_queue())
            if message.content.lower()=="reset":
                if player!=None:
                    await player.delete()
                    player=None
                status=None
                looping=False
                vc=None
                tc=None
                f=open("queue.txt","w")
                f.write("")
                f.close()
                if len(bot.voice_clients)>0:
                    voice=bot.voice_clients[0]
                    voice.stop()
                    await voice.disconnect()
                await message.add_reaction('✅')
            if message.author.voice!=None:
    
                if tc==None or tc==message.channel:
                    try:
                        if tc==None:
                            tc=message.channel
                        voicechannel=message.author.voice.channel
                        if message.content[:8].lower()=="play now":
                            if message.content[9:33]=="https://open.spotify.com":
                                url=message.content[5:]
                                playlist = spotify.playlist(url)
                                for item in playlist['tracks']['items']:
                                    if 'track' in item:
                                        track = item['track']
                                    else:
                                        track = item
                                    name=track['name']
                                    artist=track['artists'][0]['name']
                                    result=YoutubeSearch(artist+" - "+name, max_results=1).to_dict()
                                    link="https://www.youtube.com{}".format(result[0]['url_suffix'])
                                    await addtoqueue(link,voicechannel, index=playlist['tracks']['items'].index(item))
                                                    
                            elif message.content[9:14].lower()=="https":
                                link=message.content.split(" ")[1]
                                await addtoqueue(link,voicechannel,index=0)
                            else:
                                result=YoutubeSearch(message.content[5:], max_results=1).to_dict()
                                link="https://www.youtube.com{}".format(result[0]['url_suffix'])
                                await addtoqueue(link,voicechannel,index=0)
                            await message.delete()
                            print("Playing Music now")
                        elif message.content[:4].lower()=="play":

                            if message.content[5:29]=="https://open.spotify.com":
                                url=message.content[5:]
                                playlist = spotify.playlist(url)
                                for item in playlist['tracks']['items']:
                                    if 'track' in item:
                                        track = item['track']
                                    else:
                                        track = item
                                    name=track['name']
                                    artist=track['artists'][0]['name']
                                    result=YoutubeSearch(artist+" - "+name, max_results=1).to_dict()
                                    link="https://www.youtube.com{}".format(result[0]['url_suffix'])
                                    await addtoqueue(link,voicechannel)
                                                    
                            elif message.content[5:10].lower()=="https":
                                link=message.content.split(" ")[1]
                                await addtoqueue(link,voicechannel)
                            else:
                                result=YoutubeSearch(message.content[5:], max_results=1).to_dict()
                                link="https://www.youtube.com{}".format(result[0]['url_suffix'])
                                await addtoqueue(link,voicechannel)
                            await message.delete()
                            
                            print("Playing Music/Adding to queue") 
                        elif message.content.lower()[:6]=="remove":
                            f=open("queue.txt","r")
                            l=f.readlines()
                            f.close()
                            if int(message.content[7:])>=len(l):
                                message.channel.send("```No item in that queue position```",delete_after=10)
                            elif int(message.content[7:])!=0:
                                l.pop(int(message.content[7:]))
                                f=open("queue.txt","w")
                                f.writelines(l)
                                f.close()
                                await updateplayer()
                            await message.delete()
                        elif message.content.lower()=="random":
                            found=False
                            while not found:
                                try:
                                    found=True
                                    API_KEY = 'AIzaSyBoTkl-95i-YadVImgNVcXZWQfJsl1xfA4'
                                    random1 = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
                                    
                                    urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}".format(API_KEY,1,random1)
                                    webURL = urllib.request.urlopen(urlData)
                                    data = webURL.read()
                                    encoding = webURL.info().get_content_charset('utf-8')
                                    results = json.loads(data.decode(encoding))
                                    
                                    for data in results['items']:
                                        videoId = (data['id']['videoId'])
                                    
                                    yt = "https://www.youtube.com/watch?v="+videoId
                                    await addtoqueue(yt,voicechannel)
                                    await message.delete()
                                except:
                                    print("Could not play")
                                    found=False
                        elif message.content.lower()=="skip":
                            if status[:8]=="Download":
                                status="Cancelling Download"
                                await updateplayer()
                            while status!="Download Cancelled" and status!="Playing Music":
                                await updateplayer()
                            voice=bot.voice_clients[0]
                            voicechannel=voice.channel
                            await message.channel.send(content="Playing next",delete_after=10)
                            await playnext(voicechannel)
                            print("Skipping to Next")
                            await message.delete()
                        elif message.content.lower()=="pause" or message.content.lower()=="resume":
                            while status[:8]=="Download":
                                await asyncio.sleep(0.1)
                            voice=bot.voice_clients[0]
                            if voice.is_paused():
                                voice.resume()
                                status="Playing Music"
                                await message.channel.send(content="Resume",delete_after=10)
                            else:
                                voice.pause()
                                status="Paused"
                                await message.channel.send(content="Paused",delete_after=10)
                            await message.delete()
                            print("Pause/playing")
                        elif message.content.lower()=="stop":
                            if status[:8]=="Download":
                                status="Cancelling Download"
                                await updateplayer()
                            while status!="Download Cancelled" and status!="Playing Music":
                                await updateplayer()
                            await message.channel.send(content="Stopped",delete_after=10)
                            bot.voice_clients[0].stop()
                            await bot.voice_clients[0].disconnect()
                            
                            f=open("queue.txt","w")
                            f.write("")
                            f.close()
                            await player.delete()
                            player=None
                            status=None
                            looping=False
                            vc=None
                            tc=None
                            print("Stopping")
                            await message.delete()
                        elif message.content.lower()=="loop":
                            looping = not looping
                            await message.channel.send(content="Toggled Looping",delete_after=10)
                            print("Looping")
                            await message.delete()
                        elif message.content.lower()=="queue":
                            embed=discord.Embed(title="Music Queue", color=0x0cdae9)
                            queue=get_queue()
                            s=""
                            for i in range(len(queue)):
                                s=s+"\n"+str(i)+". ["+YouTube(queue[i]).title+"]("+queue[i]+")"
                            embed.add_field(name="Queue", value=s)
                            await message.channel.send(embed=embed,delete_after=10)
                            print("Showing Queue")
                            await message.delete()         
                        await updateplayer()
                    except Exception as e:
                        await message.channel.send("```Unexpected Error```",delete_after=10)
                        log=bot.get_channel(924621513448124426)
                        await log.send(e)
                    if vc==None:
                        tc=None
     

@bot.event
async def on_voice_state_update(member, before, after):
    global vc,tc,status,looping,player
    if member!=bot.user:
        f=open("queue.txt","r")
        l=f.readlines()
        f.close()
        if vc!=None:
            if len(vc.members)==1 and len(l)!=0:
                f=open("queue.txt","w")
                f.write("")
                f.close()
                voice=bot.voice_clients[0]
                voice.stop()
                await voice.disconnect()
                await player.delete()
                player=None
                status=None
                looping=False
                vc=None
                tc=None
                print("Left")


    else:
        f=open("queue.txt","r")
        l=f.readlines()
        f.close()
        if len(l)!=0 and before.channel==vc and after.channel!=vc and vc!=None:
            
            if after.channel!=None and len(after.channel.members)>1:
                vc=after.channel
                await updateplayer()
            else:
                f=open("queue.txt","w")
                f.write("")
                f.close()
                voice=bot.voice_clients[0]
                voice.stop()
                await voice.disconnect()
                await player.delete()
                player=None
                status=None
                looping=False
                vc=None
                tc=None
                print("Kicked")
        
@bot.event
async def on_ready():
    print("Bot Restarting")
    await bot.wait_until_ready()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name="your voice calls"))
    while True:
        await main_loop()

async def main_loop():
    global status
    await bot.wait_until_ready()

    print("looping")
    while True:
        if len(bot.voice_clients)>0:
            voice=bot.voice_clients[0]
            if status=="Playing Music" and (not voice.is_playing()) and (not voice.is_paused()):
                voicechannel=voice.channel
                print("Playing next")
                await playnext(voicechannel)
        await asyncio.sleep(0.1)

bot.run(TOKEN)

