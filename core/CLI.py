import argparse

class CLI:
    """
    Initializes the CLI object.

        Arguments:
        - serv: The service object used for infrastructure operations.
        - one: The object used for server-related operations.
        - pre: The object used for data preparation.
        - ans: The object used for Ansible-related operations.
    """
    def __init__(self, serv, one, pre, ans):
        self.parser = argparse.ArgumentParser(description='Описание вашей программы')
        self.serv = serv
        self.one = one
        self.pre = pre
        self.ans = ans

        subparsers = self.parser.add_subparsers(title='Команды', dest='command')

        #=====================Infra commands zone====================
        infra_parser = subparsers.add_parser('infra', help='Работа с инфраструктурой')
        infra_subparsers = infra_parser.add_subparsers(title='Действия с инфраструктурой', dest='infra_command')

        infra_create_parser = infra_subparsers.add_parser('update', help='Создание инфраструктуры из шаблона')
        infra_create_parser.add_argument('template', help='Название шаблона для создания инфраструктуры')

        infra_create_parser = infra_subparsers.add_parser('deploy', help='Создание инфраструктуры из шаблона')
        infra_create_parser.add_argument('template', help='Название шаблона для создания инфраструктуры')

       
        # Список шаблонов
        self.templates = {
            'test': 'Это шаблон тестового сервера или инфраструктуры'
        }

    

    def infra_handler(self, args):
        """
        Handles infrastructure-related commands.

        Arguments:
        - args (argparse.Namespace): Command line arguments.

        Returns: None
        """
        if args.infra_command == 'update':
            
            temp_data = self.serv.infrast_temp_opener(infr_template_name = args.template) #1. Take a infrastructure template data
            servers_on_prod = self.one.server() #2. Take a servers data from production
            servers_in_temp = self.pre.servers_deploy_data_prepare(prepare_conf_data = temp_data) #3. Take a servers data from infrastructure template file.
            servers_to_prod = self.pre.update_infra_prepare_data(servers_on_prod = servers_on_prod, servers_in_temp = servers_in_temp) #4. Prepare servers data to deploy.
            print(self.one.infrastructure_update(infrastr_data = servers_to_prod))
            
    
            #print(self.one.server(action = "create", serv_data_to_dep = prepare_infra_data))
        
        # Деплой Playbook
        elif args.infra_command == 'deploy':
            print(f'Деплой Playbook: {args.template}')
            data_from_temp = self.serv.server_parser(template_name = args.template)
            data_from_prod = self.one.server(action = "list")
            prepare_invent_data = self.pre.inventory_data(serv_data_from_infr_temp = data_from_temp, 
                                    serv_on_prod = data_from_prod)
            self.serv.create_hosts_file(servers_data_from_prod = prepare_invent_data)
            
            print(self.ans.start_ansible())
            
            

    def parse_args(self):
        """
        Parses the command line arguments.

        Returns:
            argparse.Namespace: Parsed command line arguments.
        """
        return self.parser.parse_args()

    def run(self):
        """
        Executes the CLI application based on the command provided.

        Returns: None
        """
        args = self.parse_args()
        if args.command == 'infra':
            self.infra_handler(args)
        elif args.command == 'deploy':
            self.infra_handler(args)    
        else:
            print('Неизвестная команда')
