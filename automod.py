import discord
from discord.ext import commands
from bossfight import BossFight
import asyncio
import os
import time


class AutomaticMode:
    def __init__(self, path: str):
        self.bosses = {}
        self.path: str = path
        self.__task = None
        self.__locked_path = {
            "file": None,
            "size": 0
        }
        self.__locked_boss: BossFight = None
        return

    def add(self, bossFight: BossFight):
        self.bosses[bossFight.name] = bossFight
        return

    async def _listen(self, bot: commands.Bot, channel: discord.Channel, vc: discord.VoiceClient):
        while True:
            cur_time = time.time()
            if self.__locked_path['file'] is None:
                await asyncio.sleep(1)
                for value in self.bosses.values():
                    dir_path = os.path.join(self.path, value.name)
                    file_list = os.listdir(dir_path)
                    file_list_path = []
                    for file_name in file_list:
                        file_list_path.append(os.path.join(dir_path,file_name))
                    print('for ' + value.name + ' ' + str(file_list))
                    try:
                        last_file = max(file_list_path, key=os.path.getctime)
                        if os.path.getctime(last_file) - cur_time > 0:
                            self.__locked_boss = value
                            self.__locked_boss.start(
                                bot, channel, vc)
                            self.__locked_path = {
                                "file": last_file,
                                "size": os.path.getsize(last_file)
                            }
                            await bot.send_message(channel,'starting ' + self.__locked_boss.name)
                            break
                    except ValueError:
                        pass
                    except Exception as e:                       
                        print(e)
                        pass
            else:            
                await asyncio.sleep(5)
                old_size = self.__locked_path['size']
                try:
                    current_size = os.path.getsize(self.__locked_path['file'])
                    if current_size == old_size:                
                        await bot.send_message(channel,'stopping ' + self.__locked_boss.name)
                        self.__locked_boss.stop()
                        self.__locked_boss = None
                        self.__locked_path = {
                            "file": None,
                            "size": 0
                        }
                    else:
                        self.__locked_path['size'] = current_size
                    pass 
                except Exception:
                    await bot.send_message(channel,'stopping ' + self.__locked_boss.name)
                    self.__locked_boss.stop()
                    self.__locked_boss = None
                    self.__locked_path = {
                        "file": None,
                        "size": 0
                    }
                    pass
                

    def start(self, bot: commands.Bot, channel: discord.Channel, vc: discord.VoiceClient):
        loop = asyncio.get_event_loop()
        self.__task = loop.create_task(self._listen(bot,channel,vc))
        return

    def stop(self):
        if not self.__task is None:
            self.__task.cancel()
            pass
        return
