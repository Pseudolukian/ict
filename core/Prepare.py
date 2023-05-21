import json
from typing import Any, List, Dict

#=========Exceptions zone=================
class VdcPubNameNotFound(KeyError):
    def __init__(self, text):
        self.text = text

class Prepare:
    """
    The Prepare class is responsible for preparing and validating data to be used in infrastructure tasks.

    It uses Pydantic models to clean and validate various types of data, including server configurations, Virtual Data Centers (VDCs), and operating system templates. The Pydantic models used include 'ServerData', 'VDC_config', 'OS_template_config', 'Config_file', 'Infrastructure_task', 'VDC_options_structure', 'Servers_options_structure', 'Server_VDC_data_saver', and 'ServerDataFilter'.

    After validation, the Prepare class methods return dictionaries ready to be used in tasks such as server deployment and infrastructure updating.

    Methods:
        conf_data_prepare: Prepares data for the configuration file.
        infra_temp_prepare_data: Prepares data for an infrastructure template.
        servers_deploy_data_prepare: Prepares data for server deployment.
        update_infra_prepare_data: Prepares data for updating the infrastructure.
    """

    def __init__(self, data_structures) -> None:
        self.data_structures = data_structures


    def conf_data_prepare(self, api_key:str, vdc_get_list:list = [], os_get_list:list = []) -> dict[str,str]:
        """
        This method uses Pydantic models to validate and prepare data for the configuration file.
        It takes three parameters: an API key, a list of Virtual Data Centers (VDCs), and a list of operating systems (OSes).
        Each list is validated and cleaned with the corresponding Pydantic model: 'VDC_config' for VDCs and 'OS_template_config' for OSes. 

        After validation, the method prepares data for the configuration file using the 'Config_file' Pydantic model and returns this data in a dictionary form.

        Args:
            api_key (str): The API key.
            vdc_get_list (list, optional): A list of VDCs to be validated and included in the configuration file. Defaults to an empty list.
            os_get_list (list, optional): A list of OSes to be validated and included in the configuration file. Defaults to an empty list.

        Returns:
            dict[str,str]: A dictionary of validated data ready for saving to the configuration file.
        """
        
        vdc_conf = self.data_structures["VDC_config"]
        vdc_list_clean = [vdc_conf(**vdc) for vdc in vdc_get_list]
        os_conf = self.data_structures["OS_template_config"]
        os_list_clean = [os_conf(**os) for os in os_get_list]
        config = self.data_structures["Config_file"]
        conf_out = config(API_key = api_key, VDC_list = vdc_list_clean, OS_list = os_list_clean)
        return conf_out.dict()
    

    def infra_temp_prepare_data(self, infrastructure_template_data:dict[str, Any]) -> dict[str, Any]:
        """
        This method prepares and validates data for an infrastructure template.
        It takes a dictionary containing key-value pairs representing each component of the infrastructure. For each key, it creates a new VDC_options_structure object for the "VDC_options" value and a new Servers_options_structure object for each "Servers" value. 
        The prepared data is then used to create an Infrastructure_template object, which is added to the root of the Infrastructure_task Pydantic model. This process repeats for each key-value pair in the input dictionary.

        Args:
            infrastructure_template_data (dict[str, Any]): A dictionary with data to prepare an infrastructure template. 

        Returns:
            dict[str, Any]: A dictionary representing a validated infrastructure template ready to be used in further tasks.
        """
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
        """
        This method prepares data for server deployment.
        It initializes an instance of the "ServerData" Pydantic model and uses it to validate and prepare each server configuration in the input list. The prepared configurations are appended to a new list, which is then returned.

        Args:
            prepare_conf_data (List[Dict[str, Any]]): A list of dictionaries, each containing server configuration data to prepare for deployment.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a validated server configuration ready for deployment.
        """

        s_data = self.data_structures["ServerData"]
        
        #========OneCloud API instance inicialization=========
        s_data = self.data_structures["ServerData"]

        #========OneCloud API instance input data=========
        servers_to_dep = []
        for server in prepare_conf_data:
            servers_to_dep.append(s_data(**server).dict())

        return servers_to_dep
    

    def update_infra_prepare_data(self, servers_on_prod:List[Dict[str, Any]], servers_in_temp:List[Dict[str, Any]]) -> Dict[str,List[Dict[str, Any]]]:
        """
        This method prepares data for updating the infrastructure. 
        It first filters out unnecessary information from the input lists of servers in production and in the template using the "ServerDataFilter" Pydantic model. It then compares the filtered lists to identify servers to be created, deleted, or changed.
        During this process, the server's Name and ID from the template and production servers are used for comparison. If a server in the template matches a server in production, but with different configurations, it is marked for change. Servers that exist in the template but not in production are marked for creation, and servers in production but not in the template are marked for deletion.
        The final output is a dictionary that contains lists of servers to be created, deleted, and changed.

        Args:
            servers_on_prod (List[Dict[str, Any]]): A list of dictionaries, each representing a server currently in production.
            servers_in_temp (List[Dict[str, Any]]): A list of dictionaries, each representing a server from the template.

        Returns:
            Dict[str,List[Dict[str, Any]]]: A dictionary with three keys: 'Servers_to_create', 'Servers_to_delete', and 'Servers_to_change'. Each key corresponds to a list of servers marked for that operation.
        """
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
        

        

            
     




        
    
