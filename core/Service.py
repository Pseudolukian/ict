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
    """
    The Service class provides methods for managing a configuration file and templates in a service application. 
    It can open, parse, and update configuration files, as well as locate and open templates. 
    It also provides methods for creating hosts files for use with Ansible.

    Attributes:
        templates_dir (Path): Path to the directory containing templates.
        conf_dir (Path): Path to the directory containing the configuration file.
        conf_name (str): Name of the configuration file.
        full_path (Path): Full path to the configuration file.
        pre: A reference to an external data preparation function used in some methods.

    Methods:
        api_key_caller: Retrieves the API-key from the configuration file.
        conf_file_parser: Parses the configuration file and returns the value of the given key.
        create_conf: Creates a new configuration file and adds the API-key to it.
        update_conf: Updates the configuration file with new information.
        template_opener: Searches for and opens a specified template.
        infrast_temp_opener: Prepares server specifications for 1cloud API.
        create_hosts_file: Creates a hosts.ini file for Ansible from the given server data.
    """
    

    def __init__(self,  pre, templates_dir: Path = Path("./templates"), conf_dir: Path = Path("./data"), 
                 conf_name: str = "ict_conf.json") -> None:
        self.templates_dir = templates_dir
        self.conf_dir = conf_dir
        self.conf_name = conf_name
        self.full_path = Path(self.conf_dir,self.conf_name)
        self.pre = pre


    def api_key_caller(self) -> str:
        """
        This method opens the config file located at the default templates directory (__init__.full_path).
    
        Returns:
            str: The API-key retrieved from the config file.
        """
        
        conf = json.load(open(self.full_path, 'r'))["API_key"]
        return conf
    
    def conf_file_parser(self, config_key:str = "API_key") -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        The function parses the config file and returns the value of the input config key.

        Args:
            config_key (str, optional): Config file key for searching.

        Raises:
            ConfigFileKeyError: If the config file key is not found.

        Returns:
            Union[Dict[str, Any], List[Dict[str, Any]]]: The function can return:
            - API-key in string format;
            - OSes list as a list of dictionaries;
            - VDCs list as a list of dictionaries.
        """
        conf_data = json.load(open(self.full_path, 'r'))

        conf_data_keys = list(conf_data.keys())
        
        if config_key in conf_data_keys:
            return conf_data[config_key]
        
        raise ConfigFileKeyError (f"You are input {config_key} -- this is incorrect data-key. Choice one of this keys: {conf_data_keys}")

        


    def create_conf(self) -> str:
        """
        This function creates the config file and adds the API-key into the file.
        The file will not be created until the user enters a valid API-key.
        After the file is created, the function returns the API-key as a string.

        Returns:
            str: The API-key.
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
        This function takes three positional arguments, updates the config file, and returns a Boolean value.
        It calls a data preparation function within it, passing the arguments from the outer function into the inner function.
        When the work is finished, it returns a Boolean value.

        Args:
            api_key_from_conf (str): API-key from the configuration file.
            vdc_list (list): List of VDCs to be parsed and added to the configuration file.   
            os_list (list): List of OSes to be parsed and added to the configuration file.

        Returns:
            bool: A signal Boolean value. If the operation was successful, it returns True. Otherwise, it returns False.
        """
        out_data = self.pre.conf_data_prepare(api_key = api_key_from_conf, vdc_get_list = vdc_list, os_get_list = os_list)
        
        
        with open (self.full_path, 'w') as file:
            json.dump(out_data, file, indent=4, ensure_ascii=False)
            return True   

    def template_opener(self, template_name: str) -> dict[str, Any]:
        """
        This method takes the template name and recursively searches for the template in the templates folder. 
        If the template is not found, it raises a TemplateNotFound error.
        If the template is found, the method returns a dictionary with the template data.

        Args:
            template_name (str): The name of the template to search for.

        Raises:
            TemplateNotFound: If the template is not found in the templates folder.

        Returns:
            dict[str, Any]: A dictionary containing the template data if the template is found.
        """
        template_name = template_name +".yml"
        for filepath in self.templates_dir.rglob("*"):
            if filepath.is_file() and filepath.name == template_name:
                with filepath.open("r", encoding="utf-8") as file:
                    return yaml.safe_load(file)
        raise TemplateNotFound(f"Template file '{template_name}' not found.")
    
    def infrast_temp_opener(self, infr_template_name: str) -> list[dict[str, Any]]:
        """
        This method receives one positional argument -- the name of the infrastructure template without an extension. 
        The method returns a list of servers with their specs, ready for use with the 1cloud API.

        Args:
            infr_template_name (str): Name of the infrastructure template without an extension. 

        Returns:
            list[dict[str, Any]]: List of servers with their specs ready for use with the 1cloud API.
        """
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
        This function creates a 'hosts.yml' inventory file for Ansible using a list of dictionaries that contain server data.
        The data includes server IP, username, password, and playbook information. Servers are grouped based on the prefix
        in their names (everything before the first underscore '_'). 

        Args:
            servers_data_from_prod (list[dict[str, str]]): A list of dictionaries. Each dictionary represents a server
                                                        and contains the following keys: 'IP', 'User', 'Pass', 'Name',
                                                        and 'playbook'. 

        Returns:
            bool: True if the file was created successfully, False otherwise.

        Raises:
            FileNotFoundError: If the file could not be written.
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