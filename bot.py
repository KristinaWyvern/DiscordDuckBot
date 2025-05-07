import discord
import requests
import json
import unicodedata
import random
import asyncio 
from decouple import config

# Constants
KEYDUCK = ['gęś','ges', 'kaczka', 'гусь', 'утка', 'goose', 'duck','🦆']
KEYHI = ['привет','здорово', 'здравствуйте', 'hi', 'hey', 'hello', 'cześć', 'witam', '👋']

# Helper Functions
def remove_diacritics(input_str):
      return ''.join(
        c for c in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(c) != 'Mn'
      )

def get_meme():
  response = requests.get('https://meme-api.com/gimme')
  json_data = json.loads(response.text)
  return json_data['url']

def get_duck():
  duck_pictures = [
        "https://tenor.com/view/duck-gif-6689560339757652623",
        "https://tenor.com/view/duck-ducks-confused-surprised-what-gif-1845535727828628932",
        "https://tenor.com/view/duck-duck-trap-duck-flip-gif-24652643",
        "https://tenor.com/view/what's-up-sup-duck-quack-hey-gif-2657054459091102296",
        "https://tenor.com/view/disgoosting-animals-bare-tree-media-bird-birds-gif-8761194034239194940",
        "https://tenor.com/view/goose-waddle-dance-gif-12438880182445092140",
        "https://tenor.com/view/duckinhand-duck-duckpfp-gif-25731273",
        "https://tenor.com/view/ducks-donaldduck-squad-friends-blendin-gif-11516261869844822737",
        "https://tenor.com/view/duck-gif-21314869",
        "https://tenor.com/view/duck-run-coffee-speed-bird-hot-gif-24392565",
        "https://tenor.com/view/im-coming-duck-viralhog-on-my-way-ill-be-there-in-a-sec-gif-12033051474654911259"
    ]
  return random.choice(duck_pictures)

hi_url = "https://tenor.com/view/duck-gif-8931426677329494973"

async def react_keyword(massage,keywords, url):
      normalized_content = remove_diacritics(massage.content.lower())
      if any(word in normalized_content for word in keywords):
         urls = url
         await massage.channel.send(urls)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'{client.user} is up and running!')     

@client.event
async def on_message(message):
    if message.author == client.user:
      return  
    
    await react_keyword(message,KEYDUCK, get_duck())
    await react_keyword(message,KEYHI,hi_url)

bot = discord.Bot()
@bot.event
async def on_ready():
	print(f'{bot.user} is up and running!')     

@bot.event
async def on_message(message):
    if message.author == bot.user:
     return
    
    await bot.process_commands(message)

@bot.command()
async def help(ctx):
	help_message= (
        "Commands:\n"
        "/meme - Sends a random meme\n"
        "/helps - Displays this help message\n"
        "React to messages containing 'gęś','ges', 'kaczka', 'гусь', 'утка', 'goose', 'duck' or '🦆' with a random duck gif\n"        
        "React to messages containing 'привет','здорово', 'здравствуйте', 'hi', 'hey', 'hello', 'cześć', 'witam', '👋' with a gif\n"
      )
	await ctx.respond(help_message)

@bot.command()
async def meme(ctx):
	meme_url = get_meme()
	await ctx.respond(meme_url)

loop = asyncio.get_event_loop()
loop.create_task(client.start(config('TOKEN')))
loop.create_task(bot.start(config('TOKEN')))
loop.run_forever()