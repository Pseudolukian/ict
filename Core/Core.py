from .Modules import Server, InfraTemp
from .DataStr import APIKEY

from typing import Optional
from pathlib import Path


class Core:
    
    def __init__(self, Api_key:APIKEY) ->None:
        self.Api_key = Api_key
        self.server = Server(Api_key = Api_key)

    def GetServerList(self):
        return self.server.GetList()
    def GetServerStatus(self, ServerID:str):
        return self.server.GetStatus(ServerID=ServerID)
    def ServerCreate(self, server_data):
        return self.server.create(ServerData=server_data)
    
    def InfraTempOpen(self, InfraTempDir:Path = None, InfraTempName:Path = None):
        if InfraTempDir is None or InfraTempName is None:
            infra = InfraTemp()
            temp = infra.open()
            return temp
        elif InfraTempDir is None and InfraTempName is not None:
            infra = InfraTemp( infratempname = InfraTempName)
            temp = infra.open()
            return temp
        elif InfraTempDir is not None and InfraTempName is not None: 
            infra = InfraTemp(infratempdir = InfraTempDir, infratempname = InfraTempName)
            temp = infra.open()
            return temp

    def ServersParseTemp(temp_data):
        return temp_data



