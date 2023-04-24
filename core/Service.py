from pathlib import Path
from typing import Any, Union
from prettytable import PrettyTable
import yaml, json, time
from datetime import datetime





class Service:
    

    def __init__(self,  pre, templates_dir: Path = Path("./templates"), conf_dir: Path = Path("./data"), 
                 conf_name: str = "ict_conf.json") -> None:
        self.templates_dir = templates_dir
        self.conf_dir = conf_dir
        self.conf_name = conf_name
        self.full_path = Path(self.conf_dir,self.conf_name)
        self.pre = pre


    def api_key_caller(self) -> str:
        
        conf = json.load(open(self.full_path, 'r'))["API_key"]
        return conf

     

    def create_conf(self) -> str:
        api_key_input = str()
        
        while len(api_key_input) != 64:
                print("You input incorrect API-key! Try again")
                api_key_input = input("Input API-key: ")
                
        print("You input correct API-key! Now you can using ict")
        conf = self.pre.conf_data_prepare(api_key = api_key_input)
        
        with open(self.full_path, 'w') as file:
            json.dump(conf, file, indent=4)
            return api_key_input

    def update_conf(self, api_key_from_conf, vdc_list, os_list):
        out_data = self.pre.conf_data_prepare(api_key = api_key_from_conf, vdc_get_list = vdc_list, os_get_list = os_list)
        
        with open (self.full_path, 'w') as file:
            json.dump(out_data, file, indent=4, ensure_ascii=False)
            return True   
    
        
    
    
    def vdc_data_chenger(self, publick_name: str) -> dict[str, str | bool]:
        """
        This method take the publick VDC name and return the dict with tech name, low and hight pool data.
        """
        data = json.load(open(self.full_path))["Config"]
        vdcs = []
        
        for item in data:
            if "vdc" in item:
                vdcs = item["vdc"]        
        
        for vdc in vdcs:
            for key, value in vdc.items():
                if value["Public_name"] == publick_name:
                    
                    return {"Tech_name": value["Tech_name"], 
                            "Low_pool": value["Low_pool"], 
                            "Hight_pool": value["Hight_pool"]} 
                


    def template_parser(self, template_name: str) -> dict[str, Any]:
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
        raise FileNotFoundError(f"Template file '{template_name}' not found in '{self.templates_dir}' and its subdirectories.")
    
    def server_parser(self, template_name: str) -> list[dict[str,str]]:
        """
        Method take the template name, call template_parser(template_name) and formed the list of servers ready to send it to OneCloud.
        """
        servers_data = []
        temp_data = self.template_parser(template_name)
        
        for task in temp_data.keys():
            for server in temp_data[task]["servers"]:
                playbook = temp_data[task]["servers"][server]["playbook"]
                server_data = self.template_parser(temp_data[task]["servers"][server]["template"])
                
                for time in range(temp_data[task]["servers"][server]["value"]):
                    serv_copy = server_data.copy()
                    serv_copy.update({"Name":server + "_" + str(time + 1)})
                    serv_copy.update({"playbook":playbook})
                    DC_temp_data = temp_data[task]["VDC_options"]
                    DC = self.vdc_data_chenger(DC_temp_data["DC"])
                    serv_copy.update({"DCLocation":DC["Tech_name"]})
                    if DC_temp_data["pull"] == "hight" and DC["Hight_pool"] is True:
                        serv_copy.update({"isHighPerformance":"True"})
                    elif DC_temp_data["pull"] == "base" and DC["Low_pool"] is True:
                        serv_copy.update({"isHighPerformance":"False"})
                    servers_data.append(serv_copy) 

        return servers_data


    def create_hosts_file(self, servers_data_from_prod:list[dict[str,str]]) ->bool:
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