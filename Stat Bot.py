import discord
from discord.ext import commands
from datetime import datetime
from datetime import timedelta
from scipy.stats import gaussian_kde
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import norm
import statistics as stat
from cycler import cycler
from matplotlib.colors import hsv_to_rgb

import nest_asyncio
nest_asyncio.apply()


TOKEN="Bot Token Here"


intents = discord.Intents().all()
bot = commands.Bot(command_prefix='-',intents=intents)

SHOWN=15
OTHER=True

async def get_data():
    
    earliest=datetime.now() - timedelta(days=60)
    messagedata=[]
    for server in bot.guilds:
        for channel in server.text_channels:
                messages = [message async for message in channel.history(limit=None,after=earliest)]
                for m in messages:
                    if m.author!=bot.user and not m.author.bot:
                        messagedata.append([m.channel.name,str(m.created_at)[:19],m.author.name,m.content])
    return messagedata


async def data():
    times=[]
    users=[]
    usertimes=[]
    dates=[]
    userdates=[]
    channels=[]
    userchannels=[]

    messagedata=await get_data()
        
    for row in messagedata:
        try:
            if row[0]!='bot-commands':    
                t=(datetime.strptime(row[1].split(" ")[1].split(".")[0], '%H:%M:%S'))
                day=(datetime.strptime(row[1].split(" ")[0], '%Y-%m-%d'))
                times.append(float(datetime.strftime(t,'%H'))+float(datetime.strftime(t,'%M'))/60)
                dates.append(day)
                if row[0] not in channels:
                    channels.append(row[0])
                if row[2] not in users:
                    users.append(row[2])
                    usertimes.append([times[-1]])
                    userdates.append([dates[-1]])
                    userchannels.append([row[0]])
                else:
                    usertimes[users.index(row[2])].append(times[-1])
                    userdates[users.index(row[2])].append(dates[-1])
                    userchannels[users.index(row[2])].append(row[0])
                    
        except:
            print("error for",row)
                          
    u=sorted(zip([len(i) for i in usertimes],users,usertimes,userdates,userchannels),reverse=True)
    
    if OTHER:
    
        users = [b for a,b,c,d,e in u][0:SHOWN]
        usertimes=[c for a,b,c,d,e in u]
        userdates=[d for a,b,c,d,e in u]
        userchannels=[e for a,b,c,d,e in u]
        
        f=[item for sublist in usertimes[SHOWN:] for item in sublist]
        usertimes=usertimes[0:SHOWN]
        usertimes.append(f)
        f=[item for sublist in userdates[SHOWN:] for item in sublist]
        userdates=userdates[0:SHOWN]
        userdates.append(f)
        f=[item for sublist in userchannels[SHOWN:] for item in sublist]
        userchannels=userchannels[0:SHOWN]
        userchannels.append(f)
        
        users.append("other")
    
    else:
        users = [b for a,b,c,d,e in u]
        usertimes=[c for a,b,c,d,e in u]
        userdates=[d for a,b,c,d,e in u]
        userchannels=[e for a,b,c,d,e in u]
    
    print("gathered history at ",datetime.now())
    return users,times,dates,usertimes,userdates,channels,userchannels

async def stats():
    users,times,dates,usertimes,userdates,channels,userchannels=await data()
    total=len(times)
    top=[users[0:SHOWN],[len(i) for i in usertimes[0:SHOWN]]]
    return total, top


async def wordsdata(allwords,allwords1,allwords2):

    messagedata=await get_data()

    words=[]
    for row in messagedata:
        if row!=[]:
            if row[0]!='bot-commands':
                for i in range(len(row[3].split(" "))):
                    word=row[3].split(" ")[i]
                    if ''.join([i if i.isalpha() else " " for i in word])!="":
                        words.append(''.join([i if i.isalpha() else " " for i in word]).lower())

    wordfrequencies=[words.count(words[i]) for i in range(len(words)) if (words[i] not in words[0:i])]
    words=[words[i] for i in range(len(words)) if (words[i] not in words[0:i])]
    
    wordfrequencies2=[wordfrequencies[words.index(i)] for i in words if len(i)>5]
    words2=[i for i in words if len(i)>5]
    
    z=sorted(zip(wordfrequencies2,words2),reverse=True)

    relativefreq=[(sum(allwords2)/sum(wordfrequencies))*wordfrequencies[i]/(allwords2[allwords1.index(words[i])]) if words[i] in allwords1 else 0 for i in range(len(words)) ]
    
    z=sorted(zip(relativefreq,words),reverse=True)
    
    relativefreq=[x for x,y in z]
    words=[y for x,y in z]
    print("gathered words at   ",datetime.now())
    
    return words[0:10],relativefreq[0:10]


    
    
async def graphs():
    users,times,dates,usertimes,userdates,channels,userchannels= await data()

    colours = [hsv_to_rgb([(i * 0.618033988749895) % 1.0, 0.7, 0.7]) for i in range(1000)]

    fig, ax = plt.subplots(figsize=(20,10))
    ax.set_ylabel('Density')
    ax.set_xlabel('Time (hour)')
    ax.set_prop_cycle(cycler('color', colours))
    xs = np.linspace(0,24,1000)
    upper=np.linspace(24,48,1000)
    lower=np.linspace(-24,0,1000)
    previous=np.linspace(0,0,1000)
    for i in range(len(users)):    
            density = sum(norm(xi,0.4).pdf(xs) for xi in usertimes[i])+sum(norm(xi,0.4).pdf(upper) for xi in usertimes[i])+sum(norm(xi,0.4).pdf(lower) for xi in usertimes[i])
            d=previous+density/len(times)
            ax.fill_between(xs,d,previous,label=users[i])
            previous=d

    ax.legend(loc='upper left')
    plt.xticks(np.arange(0, 24, 2)) 
    plt.savefig("Times.png")
    plt.show()
    plt.close()
    
    fig2, ax2 = plt.subplots(figsize=(20,10))
    ax2.set_ylabel('Density')
    ax2.set_xlabel('Time (hour)')
    ax2.set_prop_cycle(cycler('color', colours))
    ax2.hist(usertimes, 24, density=True, histtype='bar', stacked=True, label=users)
    ax2.legend(loc='upper left')
    density = gaussian_kde(times,bw_method=0.1)
    plt.plot(xs,density(xs),color='black')
    plt.xticks(np.arange(0, 24, 2))            
    plt.savefig("Hist.png")
    plt.show()
    plt.close()
    
    fig3, ax3 = plt.subplots(figsize=(20,10))
    ax3.set_ylabel('Messages')
    ax3.set_xlabel('Date')
    ax3.set_prop_cycle(cycler('color', colours))
    
    
    days=np.array([int(j) for j in mdates.date2num(dates)])
    x=np.linspace(min(days),max(days),int(max(days)-min(days)+1))
    xdates = [mdates.num2date(i) for i in x]
    previous=np.linspace(0,0,int(max(days)-min(days)+1))
    count=np.array([np.count_nonzero(days == j) for j in x])
    divisor=np.array([np.count_nonzero(days == i) for i in x])/max(count)
    plt.plot(xdates,count,color='black')
    rollingcount=[stat.mean(count[k:k+15]) for k in range(len(count))]
    plt.plot(xdates,rollingcount,color='red')
    divisor=np.array([i if i!=0 else 0.0001 for i in divisor])
    
    for i in range(len(users)):
        d=np.array([int(j) for j in mdates.date2num(userdates[i])])
        density=np.array([np.count_nonzero(d == j) for j in x])/divisor
        rdensity=[len(count[k:k+15])*stat.mean(np.array(density[k:k+15])*np.array(count[k:k+15]))/sum(count[k:k+15]) for k in range(len(density))]
        d2=previous+rdensity
        ax3.fill_between(x,d2,previous,label=users[i])
        previous=d2
        
    ax3.legend(loc='upper left')
    plt.savefig("Dates.png")
    plt.show()
    plt.close()
    
    fig4, ax4 = plt.subplots(figsize=(20,10))
    ax4.set_ylabel('Messages')
    ax4.set_xlabel('Top 8 Channels')
    ax4.set_prop_cycle(cycler('color', colours))
    
    
    u=sorted(zip([sum([i.count(j) for i in userchannels]) for j in channels],channels),reverse=True)
    channels = [b for a,b in u][:8]
    for i in range(len(userchannels)):
        userchannels[i]=[userchannels[i].count(j) for j in channels][:8]
    index = range(len(channels))
    previous=np.linspace(0,0,len(channels))
    for i in range(len(users)):
        plt.bar(index,userchannels[i],bottom=previous,label=users[i])
        previous+=np.array(userchannels[i])
        
    plt.xticks(index, channels,rotation=45)
    ax4.legend(loc='upper right')
    plt.savefig("Channels.png")
    plt.show()
    plt.close()
    
    print("graphs generated at ",datetime.now())
    
    total=len(times)
    top=[users[0:SHOWN],[len(i) for i in usertimes[0:SHOWN]]]
    return total, top
    


@bot.event
async def on_ready():
    print ("Bot Restarting")
    await bot.wait_until_ready()
    
    await main_loop()


async def main_loop():
    await bot.wait_until_ready()
    newdensitymessage=None
    newhistmessage=None
    newdatesmessage=None
    newchannelsmessage=None

    print("looping")
    while True:

        newchannel = bot.get_channel(1273302614989344811)

        total,top = await graphs()

        
        f=np.vstack((np.array([i for i in top[0]]),np.array([i for i in top[1]]))).T  
        f2=("\n").join([str(i[0])+": "+str(i[1]) for i in f])
        
        if newdensitymessage!=None:
            await newdensitymessage.delete()
        newdensitymessage = await newchannel.send(file=discord.File('Times.png'))
        if newhistmessage!=None:
            await newhistmessage.delete()
        newhistmessage = await newchannel.send(file=discord.File('Hist.png'))
        if newdatesmessage!=None:
            await newdatesmessage.delete()
        newdatesmessage = await newchannel.send(file=discord.File('Dates.png'))
        if newchannelsmessage!=None:
            await newchannelsmessage.delete()
        newchannelsmessage = await newchannel.send(file=discord.File('Channels.png'))
        
        print("*All data as of 1 year ago*\nTotal messages sent: "+str(total)+"\n\nTop messagers:\n"+f2+"\n\nLast Updated: "+str(datetime.now())[:-10]+"\n"+newdensitymessage.attachments[0].url+" "+newhistmessage.attachments[0].url+" "+newdatesmessage.attachments[0].url+" "+newchannelsmessage.attachments[0].url)
        print("new data at         ",datetime.now())




bot.run(TOKEN)


