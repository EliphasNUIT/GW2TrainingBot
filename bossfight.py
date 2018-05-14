import discord
from discord.ext import commands
import asyncio, os, time, json
from gtts import gTTS
from config import config

class Task:
    def __init__(self, mechanic, endTime: float, lang: str):
        self.pattern: list = mechanic['speech'][:]
        #print(self.pattern)
        self.name: str = mechanic['name']
        self.timer: float = mechanic['timer']
        self.endTime: float = endTime
        self.delay: float = mechanic['delay']
        self.initial_delay: float = mechanic['initial_delay']
        self.lang: str = lang
        ## privates
        self.__usage: int = (self.endTime - self.initial_delay)//self.timer
        if 'unique' in mechanic:
            self.__usage = 1
        self.__used: int = 0
        pass

    def reset(self):
        self.__used = 0
        pass

    async def _alert(self, bot: commands.Bot, channel: discord.Channel, vc: discord.VoiceClient):
        ## voice alert
        len_pattern = len(self.pattern)
        to_speak = self.pattern[self.__used % len_pattern]
        to_speak_name = to_speak['name']
        to_speak_speech = to_speak['say']
        voice_file = './cache/' + self.lang + '_' + to_speak_name
        if not os.path.isfile(voice_file):
            tts = gTTS(text=to_speak_speech, lang=self.lang)
            tts.save(voice_file)
            print('Created voice')
        player = vc.create_ffmpeg_player(voice_file)
        player.start()
        await asyncio.sleep(5)
        player.stop()

    async def alert(self, bot: commands.Bot, channel: discord.Channel, vc: discord.VoiceClient):
        ## prepare voice alert
        await bot.wait_until_ready()
        loop = asyncio.get_event_loop()
        await asyncio.sleep(self.initial_delay)
        while self.__used < self.__usage and not bot.is_closed:
            await asyncio.sleep(self.timer - self.delay)
            loop.create_task(self._alert(bot, channel, vc))
            await asyncio.sleep(self.delay)
            self.__used += 1
        await bot.send_message(channel, 'Mécanique ' + self.name + ' terminée')
        return 'Task completed'


class BossFight:
    def __init__(self, file_name: str):
        #config file
        input_file = open('./bosses/'+file_name+'.json', encoding="utf-8")
        config = json.load(input_file)
        self.name: str = config.get('name','')
        self.listener = None
        mechanics = config.get('mechanics',[])
        self.tasks: list = []
        for mechanic in mechanics:
            self.tasks.append(Task(mechanic, config.get('timer',0), config.get('lang','en')))
        self.async_tasks: list = []
        return

    async def _listen(self, bot: commands.Bot, channel: discord.Channel, vc: discord.VoiceClient):   
        dir_path = os.path.join(config.arc_path, self.name)
        cur_time = time.time()
        done = False
        while not done:                      
            await asyncio.sleep(5)
            try:
                file_list = os.listdir(dir_path)
                file_list_path = []
                for file_name in file_list:
                    file_list_path.append(os.path.join(dir_path, file_name))     
                    ## get last created file
                    last_file = max(file_list_path, key=os.path.getctime)
                    ## check if it is an arc dps log and if it was created since last pass
                    if (last_file.endswith(".evtc") or last_file.endswith(".evtc.zip")) and os.path.getctime(last_file) - cur_time > 0:
                        await bot.send_message(channel, 'stopping ' + self.name)
                        done = True
            except ValueError:
                pass
            except Exception as e:
                print(e)
                pass
        self.stop()        
        return

    def start(self, bot: commands.Bot, channel: discord.Channel, vc: discord.VoiceClient):
        self.stop()
        loop = asyncio.get_event_loop()
        self.async_tasks = []
        ## create async tasks for mechanics
        for task in self.tasks:
            task.reset()
            self.async_tasks.append(
                loop.create_task(task.alert(bot, channel, vc)))
        ## create file create listener
        if config.arc_enabled():
            self.listener = loop.create_task(self._listen(bot, channel, vc))
        return

    def stop(self):
        for async_task in self.async_tasks:
            async_task.cancel()
        if config.arc_enabled() and not self.listener is None:
            self.listener.cancel()
        return
