import requests, json




class OneCloudAPI:
    from core.Service import Service
    serv = Service()
    """
    This class realized working with 1cloud API server.  
    Вынести API_Key из req в __init__.
    """
    def __init__(self, api_key):
        self._base_url = "https://api.1cloud.ru/"
        self.api_key = api_key

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
            req = requests.post(url=url, headers=headers, data = data)
            return req.json()
        elif method == "put":
            req = requests.put(url=url, headers=headers, data = data)
            return req.json()


    def server(self, action = "list", data = None):
        from core.Service import Service
        serv = Service()
        """
        Method return HTTP request to 1cloud API server. 
        Сервера удаляются, но выпадает ошибка.
        """
        except_param_list = ["LinkedSshKeys","LinkedNetworks","HostName",
                            "AdminUserName","AdminPassword","ImageFamily",
                            "DateCreate","IsPowerOn","PrimaryNetworkIp","Image",
                            "IsHighPerformance", "IP"]

        except_param_create = except_param_list                    
        
        servers_list = []

        if action == "list" and data == None:
            for server in self.req(url = self._base_url + "server"):
                for exc in except_param_list:
                    del server[exc]
                servers_list.append(server)
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
            servers_predep = []
            
            for server in servers_in_temp:
                if server['Name'] not in [next(iter(x)) for x in serv_on_prod]:
                    serv_to_deploy.append(server)
            
            for dep in serv_to_deploy:
                serv_pre_dep = self.req(url="https://api.1cloud.ru/server/", method="post", data=json.dumps(dep))
                servers_predep.append(serv_pre_dep)

            for i in range(len(servers_predep)):
                for exc in except_param_create:
                    del servers_predep[i][exc]
                    servers_predep[i] = servers_predep[i]

            for pre_serv in servers_predep:
                serv.logger(task_type="Server", data=pre_serv)       
            
            return servers_predep     
        


        elif action == "update" and data !=0:
            
            pass

            
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


      
        
        
            
