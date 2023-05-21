from unittest.mock import Mock, patch
from Core.Core import Core

#==============Inport Moke data================
from ..Moke_data import Create_server_answer
from ..Moke_data import API_KEY
from ..Moke_data import ServerData

def test_ServerCreate():
    core = Core(APi_key=API_KEY)
    
    with patch('requests.post') as mock_get:
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = Create_server_answer
        result = core.server.create(ServerData = ServerData)
        assert result == Create_server_answer