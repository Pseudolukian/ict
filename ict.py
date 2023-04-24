from core.Service import Service
from core.OneCloud import OneCloudAPI
from core.CLI import CLI
from core.Ansible import Ansible
from core.Prepare import Prepare
from core.data_structures.Config_file_structure import *
from pathlib import Path
from time import time

config_dir = Path("./data/")
config_name = "ict_conf.json"
config_path = config_dir / config_name

api_key_input = str()

prep = Prepare(data_structures = {"VDC_config":VDC_config, "OS_template_config":OS_template_config, "Config_file":Config_file})
service = Service(pre = prep, conf_dir = config_dir, conf_name = config_name) 
one_cloud_api = OneCloudAPI(api_key=api_key_input, serv = service)
ansible = Ansible(serv = service)
cli = CLI(serv = service, one = one_cloud_api, ans = ansible , pre = prep)


if __name__ == '__main__':
    if config_path.is_file() is False:
        api_key_input = service.create_conf()
        one_cloud_api.api_key = api_key_input
        while not config_path.is_file() is True:
            time.sleep(1)
        service.update_conf(api_key_from_conf = api_key_input, vdc_list = one_cloud_api.get_vdc_list(), os_list = one_cloud_api.get_os_list())
    else:
        api_key_input = service.api_key_caller()
        one_cloud_api.api_key = api_key_input
        cli.run()