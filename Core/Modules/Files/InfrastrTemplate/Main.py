import yaml, json
from pathlib import Path
from .DataStr import Infrastructure_task
from typing import List, Union

class InfraTemp:
    
    def __init__(self, infratempdir:Path = Path("./Data/Templates/InfraTemplates"), infratempname:Path = Path("default")) -> None:
        self.infratemppath = infratempdir
        self.infratempname = infratempname.with_suffix(".yml")
        self.fullpath = self.infratemppath / self.infratempname
    
    def open(self) -> Union[Infrastructure_task, List[Infrastructure_task]]:
        temp_data = yaml.safe_load(open(self.fullpath, 'r'))
        tasks = []
        if len(temp_data) == 1:
            task = Infrastructure_task(__root__= temp_data)
            return task.dict_without_root()
        else:
            for k,v in temp_data.items():
                task = Infrastructure_task(__root__= {k:v}) 
                tasks.append(task.dict_without_root())
        return tasks


    def create(self):
        pass

    def change(self):
        pass

    def delete(self):
        pass

    def ServersParse(self):
        pass
        




