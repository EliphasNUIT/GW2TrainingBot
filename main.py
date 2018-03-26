import sys
sys.path.append('./trainingCogs/')
import json
import bot

#config file
config = json.load(open('./config.json'))
token = config['token']

if not (token is None or token == ""):
    bot.doBot(token, config['user_id'], config['prefix'])
else:
    print('No token given')
