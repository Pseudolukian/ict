from Core.Core import Core, CorePort
import json

core_port = CorePort(APi_key="334725caf383e2a52eb942d53924bb24a7d87c89b74505af638b19424df32f80", Module="Server", Command="GetList")
core = Core(core_port=core_port)
result = core.run(core_port=core_port)
print(result.dict())

