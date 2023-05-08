from .Modules import Server
from .DataStr import CorePort


class Core:
    def __init__(self, core_port: CorePort) -> None:
        self.core_port = core_port
        self.server = Server(Api_key=self.core_port.APi_key)

    def run(self, core_port: CorePort):
        if core_port.Module == "Server":
            method = getattr(self.server, core_port.Command)
            if core_port.Data is not None:
                return method(core_port.Data)
            else:
                return method()

