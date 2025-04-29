import discord
import requests
import json
import unicodedata
import random
from dotenv import load_dotenv
import os

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

# Main logic
class MyClient(discord.Client):
  async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))
  
  async def on_message(self, message):
    if message.author == self.user:
      return

    # React to keywords
    normalized_content = remove_diacritics(message.content.lower())
    if any(word in normalized_content for word in KEYDUCK):
       duck_url = get_duck()
       await message.channel.send(duck_url)

    if any(word in normalized_content for word in KEYHI):
       hi_url = "https://tenor.com/view/duck-gif-8931426677329494973"
       await message.channel.send(hi_url)
    
    # Commands
    if message.content.startswith('~meme'):
      meme_url = get_meme()
      await message.channel.send(meme_url)
      
    if message.content.startswith('~help'):
      help_message = (
        "Commands:\n"
        "~meme - Sends a random meme\n"
        "~help - Displays this help message\n"
        "React to messages containing 'gęś','ges', 'kaczka', 'гусь', 'утка', 'goose', 'duck' or '🦆' with a random duck gif\n"        
        "React to messages containing 'привет','здорово', 'здравствуйте', 'hi', 'hey', 'hello', 'cześć', 'witam', '👋' with a gif\n"
      )
      await message.channel.send(help_message)

# Run the Bot
intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_BOT_TOKEN'))
