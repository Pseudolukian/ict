import requests, json




class OneCloudAPI:
    from core.Service import Service
    serv = Service()
    """
    This class realized working with 1cloud API server.  
    """

    def req(self, url, method = "get", data=None):
        """
        This is inner main request method to 1cloud API server. Method receive next param:\n
        :: url -- 1cloud API url;
        ::method -- HTTP methods: get, post, put, delete;
        ::data -- Json data

        This method using by another this class methods.  
        """
        method.lower()
        api_key = self.serv.conf_worker()["Config"][0]["API_key"]
        headers = {"Content-Type":"application/json","Authorization": "Bearer {}".format(api_key)}
        if method == "get":
            req = requests.get(url=url, headers=headers)
            return req.json()
        elif method == "delete":
            req = requests.delete(url=url, headers=headers)
            return req.json()
        elif method == "post":
            req = requests.post(url=url, headers=headers, data = data)
            return req.json()


    def server(self, action = "list", data = None):
        from core.Service import Service
        serv = Service()
        """
        Method return HTTP request to 1cloud API server. 
        Сервера удаляются, но выпадает ошибка.
        """

        if action == "list" and data == None:
            servers_list = [{serv["Name"]: [{"ID":serv["ID"]}, {"IP":serv["IP"]}]} for serv in self.req(url="https://api.1cloud.ru/server")]
            return servers_list
        
        elif action == "delete" and data !=0:
            serv_in_temp_names = [serv["Name"] for serv in self.serv.infrastr_temp_pars(data)]
            serv_on_prod = [{serv["Name"]:serv["ID"]} for serv in self.server()]

            servers_on_delete = [server.get(name) for name in serv_in_temp_names for server in serv_on_prod if name in server]
            
            for s_del in servers_on_delete:
                self.req(url=f"https://api.1cloud.ru/server/{s_del}", method="delete")
                print(f"Server ID {s_del} delete.")
        
        elif action == "create" and data !=0:
            servers_in_temp = self.serv.infrastr_temp_pars(data)
            serv_on_prod = self.server()
            serv_to_deploy = []
            
            for server in servers_in_temp:
                if server['Name'] not in [next(iter(x)) for x in serv_on_prod]:
                    serv_to_deploy.append(server)
            
            for dep in serv_to_deploy:
                print(self.req(url="https://api.1cloud.ru/server/", method="post", data=json.dumps(dep)))
            return     
            
    def net(self, type = "private", action = "list", data = None):
        net_priv_cre_req = {"Name":"testNetworkAPI","DCLocation":"SdnSpb", "IsDHCP":"true","Gateway":"10.0.0.1", "LinkedServers":[]}

        if type =="private" and action == "list":
            return self.req(url="https://api.1cloud.ru/network")
        
        elif type =="public" and action == "list":
            return self.req(url="https://api.1cloud.ru/publicnetwork")
        elif type == "private" and action == "create":
            return self.req(url="https://api.1cloud.ru/network", method = "post", data = net_priv_cre_req)

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


      
        
        
            
