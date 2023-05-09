from unittest.mock import Mock, patch
from Core.Core import Core


#==============Inport Moke data================
#=====Input data=====
from ..Moke_data import API_KEY
from ..Moke_data import ServerID
#=====Output data data=====
from ..Moke_data import GetServerStatus


def test_GetServerStatus():
    core = Core(APi_key=API_KEY, Module="Server", Command="GetStatus", Data=ServerID)
    
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = GetServerStatus
        result = core.run()
        assert result != 0