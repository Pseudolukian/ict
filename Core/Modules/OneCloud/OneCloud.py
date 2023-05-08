from .Server.Main import Server
"""
SysFunc is central part of core ICT.
"""



class SysFunc:
    def __init__(self, Api_key) -> None:
        self.server = Server(Api_key)


    def run(self, SF_Module, Command, Module_Data=None):
        if SF_Module == "server":
            method = getattr(self.server, Command)
            if Module_Data is not None:
                return method(Module_Data)
            else:
                return method()


SF = SysFunc(Api_key="334725caf383e2a52eb942d53924bb24a7d87c89b74505af638b19424df32f80")

if __name__ == "__main__":
    SF.run(SF_Module="server", Command="GetList")




    

    
