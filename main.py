import discord
from discord.ext import tasks
import re
import urllib.request
import json

client = discord.Client()

Token = ""

test_channel = 707894585984024589

citycodes = {
    "さいたま": "110010",

}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(test_channel)
    await channel.send("こんにちわ")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    reg_res = re.compile(u"(.+)の天気").search(message.content)
    if reg_res:
        if reg_res.group(1) in citycodes.keys():
            citycode = citycodes[reg_res.group(1)]
            resp = urllib.request.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()
            resp = json.loads(resp.decode('utf-8'))

            channel = client.get_channel(test_channel)
            msg = "詳しくはこちらから、"
            msg += resp["link"]
            await channel.send(resp["description"]["text"])
            await channel.send(msg)


@tasks.loop(seconds=60)
async def get_weather():
    pass

client.run(Token)