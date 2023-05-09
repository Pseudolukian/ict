"""
*About ICT core*
The ICT core is heart and brain of ICT. The core managing all API and file working process.

*CorePort*
For communication with core using core port. For using core port you need:
 - from Core.Core import Core, CorePort - import Core and CorePort from Core dir
 - core_port = CorePort(APi_key="XXX", Module="Server", Command="Delete", Optional[Data]) - inincialize CorePort command
 - core = Core(core_port=core_port) - send the CorePort data to Core
 - result = core.run(core_port=core_port) - call the core.run 
 - print(result.dict()) - take and fix the result

*CorePort Commands*
Modules(str):  Commands(str):          Data(str):
Server         create                  JSON = {"Name": "testapi1", "CPU": 2, "RAM": 2048, "HDD": 40, "ImageID": "3", "DCLocatio":"", "HDDType":"SSD", "isHighPerfomance":"false", "isBackupActive":"false", "BackupPeriod":"0", "SshKeys":[]}
Server         GetStatus               Server ID
Server         GetList                 -

"""
import inspect
from .Modules import Server
from .DataStr import CorePort, CommandData


class ModuleNotFound(KeyError):
    def __str__(self):
        ErrorText = "Module not found."
        return ErrorText

class CommandNotFound(KeyError):
    def __str__(self):
        ErrorText = "Command not found."
        return ErrorText    

class Core:
    def __init__(self, APi_key:str, Module:str, Command:str, Data:str = None) -> None:
        self.Api_key = APi_key
        self.Module = Module
        self.Command = Command
        self.Data = CommandData(Data=Data)
        self.coreport = CorePort
        
        #Inicialize Modules and Commands
        self.Modules = [Server(Api_key=APi_key)]
        self.Commands = [
            method
            for module in self.Modules
            for method in dir(module)
            if not method.startswith("__") and callable(getattr(module, method))
        ]
        self.module_methods = {
            type(module).__name__: [method for method in dir(module)
            if not method.startswith("__") and callable(getattr(module, method))]
            for module in self.Modules
            }

        

    def run(self):
        if self.Module in list(self.module_methods.keys()) and self.Command in self.module_methods[self.Module]:
            
            target_module = None
            for module in self.Modules:
                if type(module).__name__ == self.Module:
                    target_module = module
                    break

            if target_module:
                method_to_call = getattr(target_module, self.Command)
                method_signature = inspect.signature(method_to_call)
                num_params = len(method_signature.parameters)

                if num_params == 0:
                    result = method_to_call()
                else:
                    result = method_to_call(self.Data.Data)

                return result
            else:
                raise ModuleNotFound
        else:
            raise CommandNotFound