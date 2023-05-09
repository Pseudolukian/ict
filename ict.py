from Core.Core import Core

core = Core(APi_key="334725caf383e2a52eb942d53924bb24a7d87c89b74505af638b19424df32f80", Module="Server", Command="GetStatus", Data="958221")
print(core.run())