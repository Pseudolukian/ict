from pathlib import Path
from typing import Any, Union, List, Dict
from prettytable import PrettyTable
import yaml, json, time
from datetime import datetime



#=========Exceptions zone=================
class TemplateNotFound(FileNotFoundError):
    def __init__(self, text):
        self.text = text

class ConfigFileKeyError(KeyError):
    def __init__(self, text):
        self.text = text

class Service:
    

    def __init__(self,  pre, templates_dir: Path = Path("./templates"), conf_dir: Path = Path("./data"), 
                 conf_name: str = "ict_conf.json") -> None:
        self.templates_dir = templates_dir
        self.conf_dir = conf_dir
        self.conf_name = conf_name
        self.full_path = Path(self.conf_dir,self.conf_name)
        self.pre = pre


    def api_key_caller(self) -> str:
        """
        The function opens the config file and returns the API-key.

        Returns:
            str: API-key.
        """
        
        conf = json.load(open(self.full_path, 'r'))["API_key"]
        return conf
    
    def conf_file_parser(self, config_key:str = "API_key") -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        The function pars the config file and returns value of input config key.

        Args:
            config_key (str, optional): config file key for searching. 

        Raises:
            ConfigFileKeyError: config file key not found.

        Returns:
            Union[Dict[str, Any], List[Dict[str, Any]]]: the function can returns:
            - API-key as string format;
            - OSes list as list of dicts;
            - VDCs list as list of dicts.
        """
        conf_data = json.load(open(self.full_path, 'r'))

        conf_data_keys = list(conf_data.keys())
        
        if config_key in conf_data_keys:
            return conf_data[config_key]
        
        raise ConfigFileKeyError (f"You are input {config_key} -- this is incorrect data-key. Choice one of this keys: {conf_data_keys}")

        


    def create_conf(self) -> str:
        """
        The function creates the config file and adds the API-key into the file.
        The file will not be created until the user enters the correct API-key.
        After creating the file, the function returns the API-key string.

        Returns:
            str: API-key.
        """
        api_key_input = str()
        
        while len(api_key_input) != 64:
                print("You input incorrect API-key! Try again")
                api_key_input = input("Input API-key: ")
                
        print("You input correct API-key! Now you can using ict")
        conf = self.pre.conf_data_prepare(api_key = api_key_input)
        
        with open(self.full_path, 'w') as file:
            json.dump(conf, file, indent=4)
            return api_key_input

    def update_conf(self, api_key_from_conf:str, vdc_list:list, os_list:list) -> bool:
        """
        The function takes 3 position arguments and updates the config file, as a result returns bool value.
        The data prepare class function is called in and arguments from the outer function are passed into the inner function.
        When work is finished, the function returns the bool value. 

        Args:
            api_key_from_conf (str): API-key from configuration file.
            vdc_list (list): list of VDCs for parsing and adding to conf file.   
            os_list (list): list of OSes for parsing and adding to conf file.

        Returns:
            bool: signal bool value.
        """
        out_data = self.pre.conf_data_prepare(api_key = api_key_from_conf, vdc_get_list = vdc_list, os_get_list = os_list)
        
        
        with open (self.full_path, 'w') as file:
            json.dump(out_data, file, indent=4, ensure_ascii=False)
            return True   

    def template_opener(self, template_name: str) -> dict[str, Any]:
        """
        This method take the template name and recursive search template in templates folder. 
        If template does not found, returning exception FileNotFind.
        If template find -- method return dict with template data.
        """
        template_name = template_name +".yml"
        for filepath in self.templates_dir.rglob("*"):
            if filepath.is_file() and filepath.name == template_name:
                with filepath.open("r", encoding="utf-8") as file:
                    return yaml.safe_load(file)
        raise TemplateNotFound(f"Template file '{template_name}' not found.")
    
    def infrast_temp_opener(self, infr_template_name: str) -> list[dict[str, Any]]:
        temp_data = self.template_opener(template_name = infr_template_name)
        servers_out_list = []
        for task_name, task_data in temp_data.items():
            servers = task_data.get("Servers")
            VDC = task_data.get("VDC_options")
            
            for server in servers:
                for server_name, server_data in server.items():
                    template = server_data.get("template")
                    value = server_data.get("value")
                    pull = VDC["pull"]
                    server_data = self.template_opener(template_name = template)
                    server_data["DCLocation"] = VDC["DC"]
                    
                    for val in range(value):
                        server_data_out = {"Name":server_name + str("_") + str(val +1), "CPU":server_data["CPU"],
                                           "RAM":server_data["RAM"], "HDD":server_data["HDD"], "HDDType":server_data["HDDType"],
                                           "ImageID":server_data["ImageID"],"DC_location":VDC["DC"]}
                        
                        if pull == "base":
                            server_data_out["isHighPerformance"] = "false"
                        elif pull == "hight":
                            server_data_out["isHighPerformance"] = "true"
                        
                        servers_out_list.append(server_data_out)
        
        return servers_out_list
                


    def create_hosts_file(self, servers_data_from_prod:list[dict[str,str]]) -> bool:
        """
        Create a hosts.ini file for Ansible from a list of dictionaries containing IP, user_name, and password.
        """
        groups = {}
        for entry in servers_data_from_prod:
            group_name = entry['Name'].split('_')[0]
            if group_name not in groups:
                groups[group_name] = {}

            host = {
                'ansible_host': entry['IP'],
                'ansible_user': entry['User'],
                'ansible_ssh_pass': entry['Pass'],
                'ansible_playbook': entry['playbook']
            }
            groups[group_name][entry['Name']] = host

        inventory = {'all': {'children': {}}}
        for group_name, hosts in groups.items():
            inventory['all']['children'][group_name] = {'hosts': hosts}

        with open('hosts.yml', 'w') as file:
            yaml.dump(inventory, file, default_flow_style=False)