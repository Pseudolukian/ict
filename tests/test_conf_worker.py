import json, os, sys, secrets, random, string
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest

sys.path.insert(0, str(Path("../core")))

from Service import Service

test_dir_names = ''.join(random.choice(string.ascii_letters) for _ in range(6))
test_file_names = ''.join(random.choice(string.ascii_letters) for _ in range(10))
test_set_data = [(test_dir_names, test_file_names, secrets.token_hex(32)) for _ in range(5)]


@pytest.mark.parametrize("temp_conf_dir, temp_conf_name, api_key", test_set_data)
def test_conf_worker(monkeypatch, temp_conf_dir, temp_conf_name, api_key):
    
    #Создание тестовых директорий и файлов
    with TemporaryDirectory() as temp_dir:
        test_temp_conf_dir = Path(temp_dir, temp_conf_dir)
        test_temp_conf_name = temp_conf_name

        
        obj = Service(conf_dir = test_temp_conf_dir, conf_name = test_temp_conf_name)

        # Подмена функции input() для ввода тестового API-ключа
        test_api_key = api_key
        monkeypatch.setattr("builtins.input", lambda _: test_api_key)

        #Tests zone
        assert obj.conf_worker() is True
        assert obj.full_path.is_file()
        with obj.full_path.open("r") as f:
            data = json.load(f)
            assert data["Config"][0]["API_key"] == test_api_key
    