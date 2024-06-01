import json
from bot import bot


with open("config.json") as config:
    token = json.load(config)


bot.run(token['bot']['token'])