"""
The server mo

Commands and them arguments list:
 - Server.create(ServerData:ServerCreate)

"""

from .DataStr import ServerCreate, ServerStatus, ServerChange, ServerChangeAnswer, ServerRebuild, ServerAction, ServerConnectToNET, ServersList
from ..REQ import URLS, HEADERS
import requests, json



class Server:
    
    
    def __init__(self, Api_key):
        self.Api_key = Api_key
        self.url = URLS()
        self.headers = HEADERS(Api_key = self.Api_key)

    def create(self, ServerData:ServerCreate) -> ServerStatus:
        data_out = requests.post(url = self.url.server, headers = self.headers.dict(), json = ServerData.json())
        answer = ServerStatus(**json.load(data_out))
        return answer
    def delete(self, ServerID:int) -> str:
        data_out = requests.delete(url = self.url.server + str(ServerID), headers = self.headers.dict())
        answer = data_out.json()
        return answer
    def change(self, ServerID:int, ServerData:ServerChange) -> ServerChangeAnswer:
        data_out = requests.put(url = self.url.server + str(ServerID), headers = self.headers.dict(), json = ServerData.json())
        answer = ServerChangeAnswer(**json.load(data_out))
        return answer
    def rebuild(self, RebuildData:ServerRebuild) -> ServerStatus:
        data_out = requests.post(url= self.url.server + str(RebuildData.ID) + "/rebuild/", headers = self.headers.dict(), json = str(RebuildData.ImageId))
        answer = ServerStatus(**json.load(data_out))
        return answer
    def action(self, ServerActionData: ServerAction) -> ServerChangeAnswer:
        data_out = requests.post(url= self.url.server + str(ServerActionData.ID) + "/action/", headers = self.headers.dict(), json = str(ServerActionData.Type))
        answer = ServerChangeAnswer(**json.load(data_out))
        return answer
    def Net(self, ServerConnectData:ServerConnectToNET ) -> ServerChangeAnswer:
        data_out = requests.post(url= self.url.server + str(ServerConnectData.ID) + "/action/", headers = self.headers.dict(), json = ServerConnectToNET.json(exclude={"ID"}))
        answer = ServerChangeAnswer(**json.load(data_out))
        return answer
    def GetStatus(self, ServerID:int) -> ServerStatus:
        """
        The method takes 1 argument position - ServerID 

        Args:
            ServerID (int): _description_

        Returns:
            ServerStatus: _description_
        """
        data_out = requests.get(url=self.url.server + str(ServerID), headers=self.headers.dict())
        answer = ServerStatus(**data_out.json())
        return answer

    def GetList(self) -> ServersList:
        """
        The method returns a list of servers created in the project.
        """
        data_out = requests.get(url= self.url.server, headers= self.headers.dict())
        servers_data = [ServerStatus(**server) for server in data_out.json()]
        answer = ServersList(ServersList=servers_data)
        return answer





