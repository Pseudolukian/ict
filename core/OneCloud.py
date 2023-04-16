import requests, json
from typing import Union




class OneCloudAPI:
    """
    This class realized working with 1cloud API server.  
    Вынести API_Key из req в __init__.
    """
    def __init__(self, api_key, serv):
        self._base_url = "https://api.1cloud.ru/"
        self.api_key = api_key
        self.serv = serv

        
    def req(self, url, method = "get", data=None):
        """
        This is inner main request method to 1cloud API server. Method receive next param:\n
        :: url -- 1cloud API url;
        ::method -- HTTP methods: get, post, put, delete;
        ::data -- Json data

        This method using by another this class methods.  
        """
        method.lower()
        api_key = self.api_key
        headers = {"Content-Type":"application/json","Authorization": "Bearer {}".format(api_key)}
        if method == "get":
            req = requests.get(url=url, headers=headers)
            return req.json()
        elif method == "delete":
            req = requests.delete(url=url, headers=headers)
            return req
        elif method == "post":
            req = requests.post(url=url, headers=headers, data = json.dumps(data))
            return req.json()
        elif method == "put":
            req = requests.put(url=url, headers=headers, data = json.dumps(data))
            return req.json()


    def server(self, action:str = "list", template:str = ""):
        """
        Method working with 1cloud api, using req() to create, deletea and update servers.
        :: action:str = list, create, delete, update.
        ::template = server config template.
        """
        def get_list() -> list[dict[str,str]]:
            """
            Function returns the list of created servers on 1cloud prod.
            Function calling req(). 
            """
            servers_list = self.req(url=self._base_url + "server", method="get")
            return servers_list
        
        def create() -> list[dict[str,str]]:
            """
            Function create the servers and returns list of panding servers without credentions to connecting Ansible.
            """
            serv_in_temp = self.serv.server_parser(template_name=template) #List of servers in template
            serv_on_dep = [] #List of servers after 1cloud API call
            serv_on_prod = [s_d["Name"] for s_d in get_list()] #List of servers on prodaction
            
            for server in serv_in_temp:
                if server["Name"] not in serv_on_prod:
                    serv_prod = self.req(url=self._base_url + "server", method="post", data=server)
                    serv_on_dep.append(serv_prod)
            
            if len(serv_on_dep) == 0:
                raise ValueError ("All server from template are created.")
            elif len(serv_on_dep) != 0:  
                return serv_on_dep

        def update() ->Union[str, list[str]]:
            """
            The function merging servers data from 1cloud panel and infrastructure template. 
            Function returns list of the updated servers name.
            """
            serv_in_temp = [] #List of servers in template
            exclude_serv_param = ["ImageID", "DCLocation","isHighPerformance"]
            serv_to_update = [] #List of servers to update
            servers_updated = []
            
            for server in self.serv.server_parser(template_name=template):
                for exc in exclude_serv_param:
                    del server[exc]
                serv_in_temp.append(server)    

            serv_on_prod = [{"ID":s_d["ID"],"Name":s_d["Name"], "CPU":s_d["CPU"], "RAM":s_d["RAM"],
                             "HDD":s_d["HDD"], "HDDType":s_d["HDDType"]} 
                            for s_d in get_list()] 
            

            for item in serv_in_temp:
                name = item.get('Name')
                for server in serv_on_prod:
                    if name == server.get('Name'):
                        if item.get('CPU') != server.get('CPU') or item.get('RAM') != server.get('RAM') or item.get('HDD') != server.get('HDD') or item.get('HDDType') != server.get('HDDType'):
                            new_server = {'ID': server.get('ID'), 'Name': name, 'CPU': item.get('CPU'), 'RAM': item.get('RAM'), 'HDD': item.get('HDD'), 'HDDType': item.get('HDDType')}
                            serv_to_update.append(new_server)

            
            for serv in serv_to_update:
                print(self.req(url= self._base_url + "server/" + str(serv["ID"]) + "/", method="put", data=serv))
                servers_updated.append(serv["Name"])

            return f"Servers was updated: {servers_updated}."    
        
        def delete() ->Union[str, list[str]]:
            """
            The function delete servers from 1cloud Panel according with infrastructure template.
            """
            serv_in_temp = self.serv.server_parser(template_name=template) #List of servers in template
            serv_on_prod = [{s_d["Name"]:s_d["ID"]} for s_d in get_list()] #List of servers on prodaction
            serv_deleted = []
            
            
            for server in serv_in_temp:
                name = server.get('Name')
                for item in serv_on_prod:
                    if name in item:
                        print(self.req(url= self._base_url + "server/" + str(item[name]) + "/", method="delete"))
                        serv_deleted.append(name)
                        
            if len(serv_deleted) !=0:
                return f"Servers {serv_deleted} was deleted."
            else:
                raise ValueError ("Nothing to delete.")
        
        if action == "list":
            return get_list()
        elif action == "create" and len(template) != 0:
            return create()
        elif action == "delete" and len(template) != 0:
            return delete()
        elif action == "update" and len(template) != 0:
            return update()


            
    def private_net(self, action = "list", data = None):
        if action == "list" and data is None:
            return self.req(url="https://api.1cloud.ru/network", method="get")
        
        elif action == "create" and data !=0:
            temp_data = self.serv.template_parser(data)
            nets_to_dep = []
        
            for key in temp_data.keys():
                if "priv_net" in temp_data[key].keys():
                    net = temp_data[key]["priv_net"]
                    net.update({"DCLocation":self.serv.vdc_data_chenger(temp_data[key]["VDC_options"]["DC"])["Tech_name"]})
                    nets_to_dep.append(net)

            for net in nets_to_dep:
                print(self.req(url=self._base_url + "network", method="post", data= json.dumps(net)))


    
    
    def vdc(self):
        return self.req(url="https://api.1cloud.ru/dcLocation")
    
    def os(self):
        return self.req(url="https://api.1cloud.ru/image")

    def acc(self):
        return self.req(url="https://api.1cloud.ru/account")
    
    def project(self):
        return self.req(url="https://api.1cloud.ru/project")
    
    def balance(self):
        return dict(self.req(url="https://api.1cloud.ru/project"))["Balances"]


      
        
        
            
