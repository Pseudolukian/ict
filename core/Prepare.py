import json
from typing import Any, List, Dict

#=========Exceptions zone=================
class VdcPubNameNotFound(KeyError):
    def __init__(self, text):
        self.text = text

class Prepare:
    """
    The Prepare class realize logic to prepare data to other classes.
    """

    def __init__(self, data_structures) -> None:
        self.data_structures = data_structures


    def conf_data_prepare(self, api_key:str, vdc_get_list:list = [], os_get_list:list = []) -> dict[str,str]:
        """
        The function takes 3 positional arguments, calling Pydantic models for preparing data for the config file.
        For validation and data preparation, the following Pydantic models are used:
        - VDC_config;
        - OS_template_config;
        - Config_file.
        
        The function returns validated data for saving it into the config file.     
    
        Args:
            api_key (str): API-key string;
            vdc_get_list (list): List of actual VDCs;  
            os_get_list (list): List of actual OSes. 

        Returns:
            dict[str,str]: Validated and ready-to-save data for the configuration file.
        """
        
        vdc_conf = self.data_structures["VDC_config"]
        vdc_list_clean = [vdc_conf(**vdc) for vdc in vdc_get_list]
        os_conf = self.data_structures["OS_template_config"]
        os_list_clean = [os_conf(**os) for os in os_get_list]
        config = self.data_structures["Config_file"]
        conf_out = config(API_key = api_key, VDC_list = vdc_list_clean, OS_list = os_list_clean)
        return conf_out.dict()
    

    def infra_temp_prepare_data(self, infrastructure_template_data:dict[str, Any]) -> dict[str, Any]:
        task = self.data_structures["Infrastructure_task"]()
        for key, value in infrastructure_template_data.items():
            vdc_options_data = value.get("VDC_options", {})
            vdc_options = self.data_structures["VDC_options_structure"](**vdc_options_data)

            servers_data = value.get("Servers", [])
            servers = []

            for server in servers_data:
                for server_key, server_value in server.items():
                    server_options = self.data_structures["Servers_options_structure"](**server_value)
                    servers.append({server_key: server_options})

            infra_str = self.data_structures["Infastructure_template"](Servers=servers, VDC_options=vdc_options)
            task.__root__[key] = infra_str
        
        return task.dict_without_root()
    
    def servers_deploy_data_prepare(self, prepare_conf_data:List[Dict[str,Any]]) -> str:
        #========OneCloud API instance inicialization=========
        s_data = self.data_structures["ServerData"]

        #========OneCloud API instance input data=========
        servers_to_dep = []
        for server in prepare_conf_data:
            servers_to_dep.append(s_data(**server).dict())

        return servers_to_dep
    

    def update_infra_prepare_data(self, servers_on_prod:List[Dict[str, Any]], servers_in_temp:List[Dict[str, Any]]) -> Dict[str,List[Dict[str, Any]]]:
        #======Pre-processing: filtering data for right compare
        server_vdc_data_saver = self.data_structures["Server_VDC_data_saver"] #Inicialize Pydantic model: Server_VDC_data_saver
        servers_vdc_data = [server_vdc_data_saver(**vdc).dict() for vdc in servers_in_temp] #Save VDC and Image ID info
        data_filter = self.data_structures["ServerDataFilter"] #Inicialize Pydantic model: ServerDataFilter
        servers_on_prod = [data_filter(**server).dict() for server in servers_on_prod] #Exclude not needing info from servers on prod
        servers_in_temp = [data_filter(**server).dict() for server in servers_in_temp] #Exclude not needing info from servers in temp
        
        servers_to_change = []

        #======Find dif between server in temp and servers on prod
        for server_temp in servers_in_temp:
            for server_prod in servers_on_prod:
                if server_temp['Name'] == server_prod['Name']:
                    server_temp["ID"] = server_prod["ID"] #This way needing for right compare servers from template and prod
                    if server_temp != server_prod:
                        servers_to_change.append(server_temp)
                        break

        servers_to_create = [server for server in servers_in_temp if server not in servers_on_prod]
        servers_to_delete = [server for server in servers_on_prod if server not in servers_in_temp]            

        #======Post-processing: exclude similary names from servers_to_change and servers_to_delete                
        for ch_server in servers_to_change:
            for index, del_serv in enumerate(servers_to_delete):
                if ch_server["Name"] == del_serv["Name"]:
                    servers_to_delete.pop(index)
            for index, cr_serv in enumerate(servers_to_create):
                if ch_server["Name"] == cr_serv["Name"]:
                    servers_to_create.pop(index)

        servers_to_delete = [server["ID"] for server in servers_to_delete] #Post-processing exclude all keys except ID key

        for index, server in enumerate(servers_to_create):
            for vdc in  servers_vdc_data:
                if server["Name"] == vdc["Name"]:
                    del server["ID"]
                    server.update(vdc)
                    servers_to_create[index] = server


        out_servers_data_to_dep = {"Servers_to_create": servers_to_create, "Servers_to_delete":servers_to_delete, "Servers_to_change":servers_to_change}
        
        return out_servers_data_to_dep
        

        

            
     




        
    
