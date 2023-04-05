from pathlib import Path
from typing import Any, Union
import yaml, json
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
        api = OneCloudAPI()
        conf = Path(self.full_path)
        date = datetime.now()
        date_string = date.strftime("%d.%m")
        
        if len(self.conf_worker()) >0:
            config = dict(json.load(open(conf)))
            api_key = json.load(open(conf))["Config"][0]
            
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
    
    def infrastr_temp_pars(self, template_name: str) -> list:
        servers_data = []
        temp_data = self.template_parser(template_name)
        
        for task in temp_data.keys():
            serv = self.template_parser(temp_data[task]["servers"]["template"])
            vdc_data = self.vdc_data_chenger(temp_data[task]["VDC_options"]["DC"])
            serv.update({"DCLocation":vdc_data["Tech_name"]})
            
            if temp_data[task]["VDC_options"]["pull"] == "hight":
                serv.update({"isHighPerformance":"true"})
            else:
                serv.update({"isHighPerformance":"false"})

            
            for time in range(temp_data[task]["servers"]["value"]):
                serv_copy = serv.copy()
                serv_copy.update({"Name":temp_data[task]["servers"]["name"] + "_" + str(time + 1)})
                servers_data.append(serv_copy)
        
        return servers_data