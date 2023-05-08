from unittest.mock import Mock, patch
from Core.Core import Core, CorePort

#==============Inport Moke data================
from ..Moke_data import GetServerListWithData
from ..Moke_data import GetServerListWithoutData
from ..Moke_data import API_KEY


def test_GetServerListWithData():
    core_port = CorePort(APi_key=API_KEY, Module="Server", Command="GetList")
    core = Core(core_port=core_port)
    
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = GetServerListWithData
        result = core.run(core_port=core_port)
        assert result != 0

def test_GetServerListWithoutData():
    core_port = CorePort(APi_key=API_KEY, Module="Server", Command="GetList")
    core = Core(core_port=core_port)
    
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = GetServerListWithoutData
        result = core.run(core_port=core_port)
        assert result != 0      