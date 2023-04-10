from pathlib import Path
from typing import Any, Union
from prettytable import PrettyTable
import yaml, json, time
from datetime import datetime





class Service:
    

    def __init__(self, templates_dir: Path = Path("./templates"), 
                 conf_dir: Path = Path("./data"), conf_name: str = "ict_conf.json") -> None:
        self.templates_dir = templates_dir
        self.conf_dir = conf_dir
        self.conf_name = conf_name
        self.full_path = Path(self.conf_dir,self.conf_name)

    def conf_worker(self) -> Union[str, dict[str, str | int]]:
        """
        Description:
        This method check the config file for availeble in dir, availeble file size and 
        availeble the API_key field in config file.

        Mechanics:
         - Checking the availeble dir -> bool: raise FileNotFoundError
         - Checking the availeble file -> bool: raise FileNotFoundError
         - Checking the size of fiel -> condition: print and loop  
        
        
        Return: 
        Full data of config file. 
        """
        file = Path(self.full_path)
    
        try:
            if not self.conf_dir.is_dir():
                raise FileNotFoundError(f"Dir {self.conf_dir} not found.")
            elif not self.full_path.is_file():
                raise FileNotFoundError(f"File {self.conf_name} not found in {self.conf_dir}.")
            elif file.stat().st_size == 0:
                print(f"File is empty! API_key field will add to file.")
                API_input = str()
                while len(API_input) != 64:
                    API_input = input("Please, input API_key:")
                with open(file, "w") as f:
                    json.dump({"Config":[{"API_key": API_input}]},f)
                    return f"API_key was added!"

            out = dict(json.load(open(file)))
            return out
        
        except FileNotFoundError as e: raise e
               

    def conf_refresher(self):
        """
        Не реализован механизм обновления информации с учётом даты. Сейчас метод чекает только длину файла и всё.
        """
        from core.OneCloud import OneCloudAPI
        
        conf = Path(self.full_path)
        date = datetime.now()
        date_string = date.strftime("%d.%m")
        
        if len(self.conf_worker()) >0:
            config = dict(json.load(open(conf)))
            api = OneCloudAPI(api_key= self.conf_worker()["API_key"])
            
            os_list = []
            vdc_list = []
            os_data_upload = api.os()
            vdc_data_upload = api.vdc()
                
            for os in os_data_upload: os_list.append({os["Name"]:os["ID"]})
            for vdc in vdc_data_upload: vdc_list.append({vdc["ShortTitle"]:
                                {"Public_name": vdc["Title"], 
                                "Tech_name":vdc["TechTitle"],"Low_pool":vdc["IsEnableLowPool"],
                                "Hight_pool":vdc["IsEnableHighPool"]}})
            
            config["Config"].append({"date_stamp":date_string})
            config["Config"].append({"servers":os_list})
            config["Config"].append({"vdc":vdc_list})
        
            with open(conf, "w") as file:
                json.dump(config, file, ensure_ascii=False)
        
            return "Refresh Ok!"

    def api_key_caller(self):
        api_key = str()
        
        for el in self.conf_worker()["Config"]:
            for k,v in el.items():
                if k == "API_key":
                    api_key = v    
        return api_key   
        
    def vdc_data_chenger(self, publick_name: str) -> dict[str, str | bool]:
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
        template_name = template_name +".yml"
        for filepath in self.templates_dir.rglob("*"):
            if filepath.is_file() and filepath.name == template_name:
                with filepath.open("r", encoding="utf-8") as file:
                    return yaml.safe_load(file)
        raise FileNotFoundError(f"Template file '{template_name}' not found in '{self.templates_dir}' and its subdirectories.")
    
    def server_parser(self, template_name: str) -> list:
        servers_data = []
        temp_data = self.template_parser(template_name)
        
        for task in temp_data.keys():
            for server in temp_data[task]["servers"]:
                server_data = self.template_parser(temp_data[task]["servers"][server]["template"])
                
                for time in range(temp_data[task]["servers"][server]["value"]):
                    serv_copy = server_data.copy() 
                    serv_copy.update({"Name":server + "_" + str(time + 1)})
                    DC_temp_data = temp_data[task]["VDC_options"]
                    DC = self.vdc_data_chenger(DC_temp_data["DC"])
                    serv_copy.update({"DCLocation":DC["Tech_name"]})
                    if DC_temp_data["pull"] == "hight" and DC["Hight_pool"] is True:
                        serv_copy.update({"isHighPerformance":"True"})
                    elif DC_temp_data["pull"] == "base" and DC["Low_pool"] is True:
                        serv_copy.update({"isHighPerformance":"False"})
                    servers_data.append(serv_copy) 

        return servers_data


    def create_hosts_file(self, data):
        """
        Create a hosts.ini file for Ansible from a list of dictionaries containing IP, user_name, and password.
        """
        with open('hosts.ini', 'w') as f:
            for item in data:
                f.write("[{}]\n".format(item["IP"]))
                f.write("{} ansible_user={} ansible_password={}\n".format(item["IP"], item["user_name"], item["password"]))
        return f"Hosts file created."        


    def printer(self, data):
        
        def same_keys(dicts: list[dict]) -> bool:
            keys = set(dicts[0].keys())
            return all(filter(lambda d: set(d.keys()) == keys, dicts))
        
        if type(data) is list and same_keys(dicts = data):
            table = PrettyTable()
            table.field_names = list(data[0].keys())
            for i, d in enumerate(data):
                table.add_row(list(d.values()))
            print(table)

        elif type(data) is dict:
            table = PrettyTable()
            table.field_names = list(data.keys())
            for i, d in enumerate(data):
                table.add_row(list(d.values()))
            print(table)


    def logger(self, task_type, data):
        log_path = Path(".", "log.json")
        def_structure = {"Tasks":[{"Server":[]}, {"Nets":[]}]}

        def opener():
            with open(log_path) as f:
                log_data = json.load(f)
            return log_data["Tasks"]

        def creator():
            with open(log_path, "w") as log:
                json.dump(def_structure, log) 

        def editor():
            log_data = opener()
            if task_type == "Server":
                server_tasks = log_data[0]["Server"]
                server_tasks.append(data)
            elif task_type == "Net":
                net_tasks = log_data[1]["Nets"]
                net_tasks.append(data)
            with open(log_path, "w") as log:
                json.dump({"Tasks": log_data}, log)

        if log_path.is_file() and log_path.stat().st_size > 0:
            editor()
        else:
            creator()
            while not log_path.is_file():
                time.sleep(1)
            editor()  

   
            
            

            



