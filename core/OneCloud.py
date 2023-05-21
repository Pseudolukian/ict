from typing import Union, List, Dict, Any
import json
import requests



class OneCloudAPI:
    """
    A class for interacting with the 1cloud API.

    Args:
        api_key (str): The API key to authenticate the requests.

    Attributes:
        api_key (str): The API key used for authentication.

    Methods:
        req(url, method="get", input_data={}):
            Makes a request to the 1cloud API server.

        server(server_id="", action="list", serv_data_to_dep={}):
            Handles various server-related actions on the 1cloud API.

        update():
            Merges server data from the 1cloud panel with the infrastructure template and updates the server.

        delete():
            Deletes servers from the 1cloud Panel according to the infrastructure template.

        infrastructure_update(infrastr_data):
            Prints the summary of the infrastructure changes and asks for user confirmation.

        get_vdc_list():
            Fetches the list of Virtual Data Centers (VDCs) from the 1cloud API.

        get_os_list():
            Fetches the list of available Operating Systems (OSs) from the 1cloud API.

        acc():
            Fetches the account information from the 1cloud API.

        project():
            Fetches the project information from the 1cloud API.

        balance() -> dict:
            Fetches the account balance information from the 1cloud API.

    Note:
        This class requires a valid API key for authentication. Make sure to provide the API key when creating an instance of the class.
    """
    def __init__(self, api_key, serv):
        self._base_url = "https://api.1cloud.ru/"
        self.api_key = api_key
        self.serv = serv

        
    def req(self, url, method = "get", input_data:Dict[str, Any] = {}):
        """
        This method makes a request to the 1cloud API server.

        Args:
            url (str): The 1cloud API url to make a request to.
            method (str, optional): The HTTP method to use for the request. 
                It can be one of the following: "get", "post", "put", "delete". Default is "get".
            input_data (dict, optional): The JSON data to include in the request body. Default is an empty dictionary.

        Returns:
            dict or str: The JSON response from the server as a dictionary for "get", "post", and "put" requests. 
                For "delete" requests, it returns the response as a string.

        Note:
            This method is intended to be used internally by other methods in this class.
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
        Handles various server-related actions on the 1cloud API, using the req() method.

        Args:
            server_id (str, optional): The ID of the server to perform an action on. Default is an empty string.
            action (str, optional): The action to perform. Can be one of the following: "list", "create", "delete", "update". Default is "list".
            serv_data_to_dep (dict, optional): The server configuration data required for the "create" and "update" actions. Default is an empty dictionary.

        Note:
            This method is capable of listing, creating, deleting, and updating servers on 1cloud.
        """
        
        def get_list() -> list[dict[str,str]]:
            """
            Retrieves the list of servers created on 1cloud.

            Returns:
                list[dict[str, str]]: A list of dictionaries, where each dictionary represents a server on 1cloud.

            Note:
                This function uses the req() method to fetch the data. 
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
            Merges server data from the 1cloud panel with the infrastructure template and updates the server.

            Note:
                The function communicates with the 1cloud API to update the server information.

            Returns:
                str: A message indicating the success of the operation, including the name of the updated server.
            """

            print(self.req(url = self._base_url + "server/" + server_id + "/", method = "put", input_data = serv_data_to_dep))
               
        
        def delete() -> str:
            """
            Deletes servers from the 1cloud Panel in accordance with the infrastructure template.

            Note:
                The function communicates with the 1cloud API to delete the server.

            Returns:
                str: A message indicating the success of the operation, including the name of the deleted server.
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
        """
        Prints the summary of the infrastructure changes and asks for user confirmation.
        The changes include the number of servers to be created, updated, and deleted.

        If the user confirms the changes, the function proceeds to create, update, and delete the servers accordingly.
        If the user does not confirm the changes, the function aborts the operation.

        Args:
            infrastr_data (Dict[str,List[Dict[str, Any]]]): A dictionary containing three keys: "Servers_to_create", 
                "Servers_to_change", and "Servers_to_delete". Each key corresponds to a list of dictionaries, 
                each representing a server.

        Note:
            The actual updates are performed based on the user's confirmation.
        """
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
        """
        Fetches the list of Virtual Data Centers (VDCs) from the 1cloud API.

        Returns:
            dict: The API response as a dictionary.
        """
        return self.req(url="https://api.1cloud.ru/dcLocation")
    
    def get_os_list(self) -> Dict[str, Any]:
        """
        Fetches the list of available Operating Systems (OSs) from the 1cloud API.

        Returns:
            dict: The API response as a dictionary.
        """
        return self.req(url="https://api.1cloud.ru/image")

    def acc(self) -> Dict[str, Any]:
        """
        Fetches the account information from the 1cloud API.

        Returns:
            dict: The API response as a dictionary containing the account information.
        """
        return self.req(url="https://api.1cloud.ru/account")
    
    def project(self) -> Dict[str, Any]:
        """
        Fetches the project information from the 1cloud API.

        Returns:
            dict: The API response as a dictionary containing the project information.
        """
        return self.req(url="https://api.1cloud.ru/project")
    
    def balance(self) ->Dict[str, Any]:
        """
        Fetches the account balance information from the 1cloud API.

        Returns:
            dict: The API response as a dictionary containing the balance information.
        """
        return dict(self.req(url="https://api.1cloud.ru/project"))["Balances"]


      
        
        
            
