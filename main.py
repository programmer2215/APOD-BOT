import os
import requests as req
from discord.ext import commands
from keep_alive import keep_alive
from datetime import datetime as dt
from bs4 import BeautifulSoup as soup

bot = commands.Bot(command_prefix="@", description="The description")


def get_pic(date, url, info):
    data = req.get(url)
    parser = soup(data.text, 'html.parser')
    try:
        rel_url = parser.find('img')['src']
        title = parser.find('b').text
        result = (url, f"https://apod.nasa.gov/{rel_url}",
                  f"**[{date}] {title}**\n")
        if info:
            expln = parser.findAll('p')[2].text
            expln = expln[:expln.index("Tomorrow's picture:")]
        else:
            expln = ''
        result = result + (expln, )
    except:
        result = ()

    return result


'''def current_img():
  now = dt.now()
  now = now.strftime("%y%m%d")
  url = f"https://apod.nasa.gov/apod/ap{now}.html"
  result = get_pic(url)
  
  return result'''


def scrape(date, info=False):
    formatted_date = date
    date = dt.strptime(date, '%d-%m-%Y').strftime("%y%m%d")
    url = f"https://apod.nasa.gov/apod/ap{date}.html"

    return get_pic(formatted_date, url, info)


@bot.event
async def on_ready():
    print("ready")


@bot.command()
async def today(ctx):
    msg = ctx.message.content.split()
    info = False
    if 'info' in msg:
        info = True
    now = dt.now()
    now = now.strftime("%d-%m-%Y")

    url, pic, title, expln = scrape(now, info)
    if len(pic) > 0:
        await ctx.send(url)
        await ctx.send(pic)
        await ctx.send(title)
        if expln:
            await ctx.send(expln)

    else:
        await ctx.send(f"""***APOD is yet to be updated today!***""")


@bot.command()
async def archive(ctx):
    msg = ctx.message.content.split()
    date = msg[1]
    info = False
    if 'info' in msg:
        info = True
    url, pic, title, expln = scrape(date, info)
    if len(pic) > 0:
        await ctx.send(url)
        await ctx.send(pic)
        await ctx.send(title)
        if expln:
            await ctx.send(expln)
    else:
        await ctx.send(f"""***APOD was not found for {date}!***""")


BOT_KEY = os.environ['BOT_KEY']
keep_alive()
bot.run(BOT_KEY)
