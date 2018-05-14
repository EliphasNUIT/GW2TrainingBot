import json, os

class Config:
    def __init__(self):
        ## general        
        config = json.load(open('./configs/config2.json'))
        self.token = config.get('token', '')
        self.id = config.get('user_id','')
        self.prefix = config.get('prefix','!')
        self.autoclean = config.get('autocleancache',False)
        ## logging
        logs_config = json.load(open('./configs/logs.json'))       
        self.arc_path = logs_config.get('arcDPSPath','')
        self.el_path = logs_config.get('gw2ElPath','')
        if os.path.exists(os.path.expandvars(self.arc_path)):
            self.arc_path = os.path.expandvars(self.arc_path)       
        if os.path.exists(os.path.expandvars(self.el_path)):
            self.el_path = os.path.expandvars(self.el_path)
        ## raidar
        raidar_config = json.load(open('./configs/raidar.json'))
        self.raidar_name = raidar_config.get('raidar','')
        self.raidar_psw = raidar_config.get('raidarpsw','')
        if self.arc_enabled:
            print("Arc functionnalities enabled")
        if self.gw2el_enabled:
            print("GW2 El functionnalities enabled")
        if self.raidar_enabled:
            print("GW2 raidar functionnalities enabled")
        pass

    def has_token(self):
        return not self.token == ""

    def diff_id(self, id: str):
        return not (id == self.id or self.id == "")

    def arc_enabled(self):
        if not self.arc_path == "":
            return os.path.exists(self.arc_path)
        return False

    def gw2el_enabled(self):
        if not self.el_path == "":
            return os.path.exists(self.el_path)
        return False

    def raidar_enabled(self):
        return not self.raidar_name == "" and not self.raidar_psw == ""

    def raidar_data(self):
        return {'username': self.raidar_name, 'password': self.raidar_psw}
    


config = Config()