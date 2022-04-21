import os
import requests as req
from discord.ext import commands
from keep_alive import keep_alive
from datetime import datetime as dt
from bs4 import BeautifulSoup as soup

bot = commands.Bot(command_prefix="@", description="The description")

def get_pic(url):
  data = req.get(url)
  parser = soup(data.text, 'html.parser')
  try:
    rel_url = parser.find('img')['src']
    result = f"https://apod.nasa.gov/{rel_url}"
  except:
    result = ""
  
  return result

'''def current_img():
  now = dt.now()
  now = now.strftime("%y%m%d")
  url = f"https://apod.nasa.gov/apod/ap{now}.html"
  result = get_pic(url)
  
  return result'''

def scrape(date):
  date = dt.strptime(date, '%d-%m-%Y').strftime("%y%m%d")
  url = f"https://apod.nasa.gov/apod/ap{date}.html"
  pic_url = get_pic(url)
  return pic_url

@bot.event
async def  on_ready():
    print("ready")
      
        

@bot.command()
async def today(ctx):
  now = dt.now()
  now = now.strftime("%d-%m-%Y")
  pic = scrape(now)
  if len(pic) > 0:
    await ctx.send(pic)
  else:
    await ctx.send(f"""***APOD is yet to be updated today!***""")
  

@bot.command()
async def archive(ctx):
  date = ctx.message.content.split()[1]
  pic = scrape(date)
  if len(pic) > 0:
    await ctx.send(pic)
  else:
    await ctx.send(f"""***APOD was not found for {date}!***""")

BOT_KEY = os.environ['BOT_KEY']
keep_alive()
bot.run(BOT_KEY)
