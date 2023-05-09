from unittest.mock import Mock, patch
from Core.Core import Core

#==============Inport Moke data================
from ..Moke_data import GetServerListWithData
from ..Moke_data import GetServerListWithoutData
from ..Moke_data import API_KEY


def test_GetServerListWithData():
    core = Core(APi_key=API_KEY, Module="Server", Command="GetServerList")
    
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = GetServerListWithData
        result = core.run()
        assert result.dict()["ServersList"] == GetServerListWithData