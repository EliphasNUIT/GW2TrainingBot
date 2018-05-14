import discord
from discord.ext import commands
import time, subprocess, shutil, requests, json, os, asyncio
from config import config

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

class AutoLogger:
    def __init__(self):      
        self.__evtcs = {}
        self.__htmls = {}       
        self.__fevtcs = {}
        self.__fhtmls = {}
        self.__task = None
        return

    def send_log(self, log: str):
        if config.raidar_enabled():
            try:
                ## get token
                response = requests.post("https://www.gw2raidar.com/api/v2/token",data=config.raidar_data())
                if str(response.status_code) != "200":
                    print(response.reason)
                    return
                token = response.json()["token"]
                headers = { 'Authorization': 'Token ' + token}
                files = {'file': open(log,'rb')}
                ## send file
                response = requests.put("https://www.gw2raidar.com/api/v2/encounters/new",files=files, headers = headers)
                if str(response.status_code) != "200":
                    print(response.reason)
                    return
            except Exception as e:
                print(e)
        return


    async def _listen(self, bot: commands.Bot, channel: discord.Channel):  
        exe_path = None          
        init_time = time.time() 
        ## get gw2 el executable
        if config.gw2el_enabled():
            testpath = config.el_path+'\\GuildWars2EliteInsights.exe'
            os.path.isfile(testpath)   
            exe_path = testpath
        while True:      
            await asyncio.sleep(15)
            directories = get_immediate_subdirectories(config.arc_path)
            for name in directories:
                ## init dictionary
                if self.__evtcs.get(name,None) is None:
                    self.__evtcs[name] = {}                
                if self.__htmls.get(name,None) is None:
                    self.__htmls[name] = {}       
                if self.__fevtcs.get(name,None) is None:
                    self.__fevtcs[name] = {}                
                if self.__fhtmls.get(name,None) is None:
                    self.__fhtmls[name] = {}
                ## get files in directory    
                log_path = os.path.join(config.arc_path, name)              
                log_list = os.listdir(log_path)
                for log in log_list:           
                    path_to_log = os.path.join(log_path, log) 
                    ctime = os.path.getctime(path_to_log)
                    ## file is arc dps log      
                    if (log.endswith(".evtc") or log.endswith(".evtc.zip")) and ctime > init_time:              
                        ##print(log)       
                        log_id = log.split('.')[0]
                        if self.__evtcs[name].get(log_id, None) is None and self.__fevtcs[name].get(log_id, None) is None:
                            self.__evtcs[name][log_id] = log
                            self.__fevtcs[name][log_id] = log
                            if not exe_path is None:
                                subprocess.run([exe_path, path_to_log])
                    ## file is gw2el log
                    if log.endswith(".html") and ctime > init_time:                                     
                        ##print(log)    
                        log_id = log.split('_')[0]                     
                        if self.__htmls[name].get(log_id, None) is None and self.__fhtmls[name].get(log_id, None) is None:
                            if "kill" in log:   
                                await bot.send_message(channel, "Success for " + name)
                                self.__fevtcs[name].pop(log_id)
                                self.__htmls[name][log_id] = log
                                ## send the log to gw2 raidar
                                self.send_log(os.path.join(log_path,self.__evtcs[name][log_id]))
                            else:
                                self.__evtcs[name].pop(log_id)
                                self.__fhtmls[name][log_id] = log
                                await bot.send_message(channel, "Failure for " + name)
                            ## send the log to the channel
                            await bot.send_file(channel, path_to_log)
        return

    async def display_success(self, bot: commands.Bot, channel: discord.Channel):    
        for name, logs in self.__htmls.items():
            if logs.values().length > 0:
                await bot.send_message(channel, name.upper() + ": ")
            for log_name in logs.values():            
                await bot.send_message(channel, log_name)

    def clean(self):
        for name, logs in self.__fevtcs.items():          
            log_path = os.path.join(config.arc_path, name)  
            for log_name in logs.values():                 
                path_to_log = os.path.join(log_path, log_name) 
                os.remove(path_to_log)
        for name, logs in self.__fhtmls.items():
            log_path = os.path.join(config.arc_path, name)  
            for log_name in logs.values():                 
                path_to_log = os.path.join(log_path, log_name) 
                os.remove(path_to_log)
        self.__fhtmls = {}
        self.__fevtcs = {} 
    
    def regroup(self):
        for name, logs in self.__evtcs.items():          
            log_path = os.path.join(config.arc_path, name)  
            for log_name in logs.values():                
                path_to_log = os.path.join(log_path, log_name) 
                shutil.move(path_to_log, os.path.join(config.arc_path,".\\.."))
        for name, logs in self.__htmls.items():
            log_path = os.path.join(config.arc_path, name)  
            for log_name in logs.values():                
                path_to_log = os.path.join(log_path, log_name) 
                shutil.move(path_to_log, os.path.join(config.arc_path,".\\.."))
        self.__htmls = {}
        self.__evtcs = {} 
                 

    def start(self, bot: commands.Bot, channel: discord.Channel):
        self.stop()
        loop = asyncio.get_event_loop()      
        self.__task = loop.create_task(self._listen(bot, channel))
        return

    def stop(self):
        if not self.__task is None:
            self.__task.cancel()
        return

