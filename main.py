import sys
sys.path.append('./trainingCogs/')
from config import config
import bot

if config.has_token():
    bot.doBot()
else:
    print('No token given')
