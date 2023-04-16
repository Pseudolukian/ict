
class Prepare:
    """
    The Prepare class realize logic to prepare data to other classes.
    """

    def __init__(self) -> None:
        pass

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