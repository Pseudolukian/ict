from typing import Union, List, Dict, Any
import json
import requests



class OneCloudAPI:
    """
    This class realized working with 1cloud API server.  
    Вынести API_Key из req в __init__.
    """
    def __init__(self, api_key, serv):
        self._base_url = "https://api.1cloud.ru/"
        self.api_key = api_key
        self.serv = serv

        
    def req(self, url, method = "get", input_data:Dict[str, Any] = {}):
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
            req = requests.get(url = url, headers = headers, timeout = 5)
            return req.json()
        elif method == "delete":
            req = requests.delete(url = url, headers = headers, timeout = 5)
            return req.text
        elif method == "post":
            req = requests.post(url = url, headers = headers, data = json.dumps(input_data), timeout = 10)
            return req.json()
        elif method == "put":
            req = requests.put(url = url, headers = headers, data = json.dumps(input_data), timeout = 10)
            return req.json()


    def server(self, server_id:str = "", action:str = "list", serv_data_to_dep:Dict[str, Any] = {}):
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
        
        def create() -> str:
            """
            Function create the servers and returns list of panding servers without credentions to connecting Ansible.
            """
            
            print(self.req(url = self._base_url + "server", method = "post", input_data = serv_data_to_dep))

        def update() -> str:
            """
            The function merging servers data from 1cloud panel and infrastructure template. 
            Function returns list of the updated servers name.
            """

            print(self.req(url = self._base_url + "server/" + server_id + "/", method = "put", input_data = serv_data_to_dep))
               
        
        def delete() -> str:
            """
            The function delete servers from 1cloud Panel according with infrastructure template.
            """

            print(self.req(url = self._base_url + "server/" + str(serv_data_to_dep) + "/", method = "delete"))
            
        
        if action == "list":
            return get_list()
        elif action == "create" and len(serv_data_to_dep) != 0:
            return create()
        elif action == "delete" and len(serv_data_to_dep) != 0:
            return delete()
        elif action == "update" and len(serv_data_to_dep) != 0:
            return update()


    def infrastructure_update(self, infrastr_data:Dict[str,List[Dict[str, Any]]]):
        #================Print information set up========================
        point = "#"
        placeholder = "="
        label = "Infrastructure info"
        header = "The following changes will be made to the infrastructure:"
        place_holder_len = int(((len(header)-len(label))-2)/2)
        print(point, placeholder*place_holder_len, label, placeholder*place_holder_len, point)
        print()
        print(header)
        print(" "*4, "- Servers to be created:", len(infrastr_data["Servers_to_create"]))
        print(" "*4, "- Servers to be updated:", len(infrastr_data["Servers_to_change"]))
        print(" "*4, "- Servers to be deleted:", len(infrastr_data["Servers_to_delete"]))
        print()
        print(point, placeholder*place_holder_len, placeholder*len(label), placeholder*place_holder_len, point)
        choice = input("You a confirm information (Y/N): ")
        
        #================Main logic==================================#
        if choice == "Y":
            for server_category, category_data in infrastr_data.items():
                if server_category == "Servers_to_create":
                    if len(category_data) != 0:
                        for server in category_data:
                            #print("Server to create:", server)
                            print(self.server(action = "create", serv_data_to_dep = server))
                elif server_category == "Servers_to_change":
                    if len(category_data) != 0:
                        for server_data in category_data:
                            print(server_data)
                            print(self.server(action = "update", serv_data_to_dep = server_data, server_id = server_data["ID"]))
                elif server_category == "Servers_to_delete":
                    if len(category_data) != 0:
                        for server_id in category_data:
                            #print("Server to delete:",id)
                            print(self.server(action = "delete", serv_data_to_dep = server_id))
        elif choice == "N":
            print("Abort infrastructure changing!")                    
      
    def get_vdc_list(self):
        return self.req(url="https://api.1cloud.ru/dcLocation")
    
    def get_os_list(self):
        return self.req(url="https://api.1cloud.ru/image")

    def acc(self):
        return self.req(url="https://api.1cloud.ru/account")
    
    def project(self):
        return self.req(url="https://api.1cloud.ru/project")
    
    def balance(self):
        return dict(self.req(url="https://api.1cloud.ru/project"))["Balances"]


      
        
        
            
