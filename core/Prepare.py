import json
class Prepare:
    """
    The Prepare class realize logic to prepare data to other classes.
    """

    def __init__(self, data_structures) -> None:
        self.data_structures = data_structures

    def inventory_data(self, serv_data_from_infr_temp:list[dict[str,str]], serv_on_prod:list[dict[str,str]]) -> list[dict[str,str]]:
        """
        Method take infrastructure template, parse it, create list of production servers and returns the data with connect credentions for Ansible.
        """
        serv_in_temp = serv_data_from_infr_temp #List of servers in template
        serv_on_prod = [{"Name":s_p["Name"],"IP":s_p["IP"], "ID": s_p["ID"],
                         "User":s_p["AdminUserName"], "Pass":s_p["AdminPassword"]} for s_p in serv_on_prod]
        serv_to_plb_dep = []
    
        for server_in_temp in serv_in_temp:
            for server_on_prod in serv_on_prod:
                if server_in_temp['Name'] == server_on_prod['Name']:
                    server = {
                        'Name': server_on_prod['Name'],
                        'ID': server_on_prod['ID'],
                        'IP': server_on_prod['IP'],
                        'User': server_on_prod['User'],
                        'Pass': server_on_prod['Pass'],
                        'playbook': "./templates/playbooks/" + server_in_temp['playbook'] + ".yml"
                    }
                    serv_to_plb_dep.append(server)

        return serv_to_plb_dep
      

    def conf_data_prepare(self, api_key, vdc_get_list:list = [], os_get_list:list = []) -> dict[str,str]:
        
        vdc_conf = self.data_structures["VDC_config"]
        vdc_list_clean = [vdc_conf(**vdc) for vdc in vdc_get_list]
        os_conf = self.data_structures["OS_template_config"]
        os_list_clean = [os_conf(**os) for os in os_get_list]
        config = self.data_structures["Config_file"]
        conf_out = config(API_key = api_key, VDC_list = vdc_list_clean, OS_list = os_list_clean)
        return conf_out.dict()
        
    
