import argparse

class CLI:
    def __init__(self, serv, one, pre, ans):
        self.parser = argparse.ArgumentParser(description='Описание вашей программы')
        self.serv = serv
        self.one = one
        self.pre = pre
        self.ans = ans

        subparsers = self.parser.add_subparsers(title='Команды', dest='command')

        #===================Server commands zone======================
        server_parser = subparsers.add_parser('server', help='Работа с серверами')
        server_subparsers = server_parser.add_subparsers(title='Действия с серверами', dest='server_command')

        #Server create
        server_create_parser = server_subparsers.add_parser('create', help='Создание сервера из шаблона')
        server_create_parser.add_argument('template', help='Название шаблона для создания сервера')

        #Server delete
        server_delete_parser = server_subparsers.add_parser('delete', help='Удаление серверов по шаблону')
        server_delete_parser.add_argument('template', help='Название шаблона для удаления сервера')

        #Server update
        server_update_parser = server_subparsers.add_parser('update', help='Изменение серверов по шаблону')
        server_update_parser.add_argument('template', help='Название шаблона для изменения сервера')

        #Get server list
        server_update_parser = server_subparsers.add_parser('list', help='Изменение серверов по шаблону')

        #===================private_net commands zone======================
        private_net_parser = subparsers.add_parser('private_net', help='Работа с сетями')
        private_net_subparsers = private_net_parser.add_subparsers(title='Действия с сетями', dest='private_net_command')

        #private_net create
        private_net_create_parser = private_net_subparsers.add_parser('create', help='Создание приватной сети из шаблона')
        private_net_create_parser.add_argument('template', help='Название шаблона для создания сети')

        #private_net delete
        private_net_delete_parser = private_net_subparsers.add_parser('delete', help='Удаление сети по шаблону')
        private_net_delete_parser.add_argument('template', help='Название шаблона для удаления сети')

        #private_net update
        private_net_update_parser = private_net_subparsers.add_parser('update', help='Изменение сети по шаблону')
        private_net_update_parser.add_argument('template', help='Название шаблона для изменения сети')

        #Get private_net list
        private_net_update_parser = private_net_subparsers.add_parser('list', help='Изменение сети по шаблону')


        #=====================Infra commands zone====================
        infra_parser = subparsers.add_parser('infra', help='Работа с инфраструктурой')
        infra_subparsers = infra_parser.add_subparsers(title='Действия с инфраструктурой', dest='infra_command')

        infra_create_parser = infra_subparsers.add_parser('create', help='Создание инфраструктуры из шаблона')
        infra_create_parser.add_argument('template', help='Название шаблона для создания инфраструктуры')

        infra_delete_parser = infra_subparsers.add_parser('delete', help='Удаление инфраструктуры')
        infra_delete_parser.add_argument('template', help='Название шаблона для удаления инфраструктуры')

        infra_update_parser = infra_subparsers.add_parser('update', help='Изменение инфраструктуры')
        infra_update_parser.add_argument('template', help='Название шаблона для изменения инфраструктуры')

        infra_update_parser = infra_subparsers.add_parser('deploy', help='Изменение инфраструктуры')
        infra_update_parser.add_argument('template', help='Название шаблона для изменения инфраструктуры')
       
        
        # Список шаблонов
        self.templates = {
            'test': 'Это шаблон тестового сервера или инфраструктуры'
        }

    def server_handler(self, args):
        if args.server_command == 'create':
            print(f'Создание сервера(ров) из шаблона: {args.template}')
            print(self.one.server(action="create", template=args.template))
            # Создание сервера из шаблона
        elif args.server_command == 'delete':
            print(f'Удаление серверов по шаблону: {args.template}')
            print(self.one.server(action="delete", template=args.template))
            # Удаление серверов по шаблону
        elif args.server_command == 'update':
            print(f'Изменение серверов по шаблону: {args.template}')
            print(self.one.server(action="update", template=args.template))
            # Изменение серверов по шаблону
        elif args.server_command == 'list':    
            print(self.one.server())


    def private_net_handler(self, args):
        if args.private_net_command == 'create':
            print(f'Создание сети из шаблона: {args.template}')
            print(self.one.private_net(action="create", data=args.template))
            # Создание сервера из шаблона
        elif args.private_net_command == 'delete':
            print(f'Удаление сети по шаблону: {args.template}')
            
            # Удаление серверов по шаблону
        elif args.private_net_command == 'update':
            print(f'Изменение сети по шаблону: {args.template}')
            # Изменение серверов по шаблону
        elif args.private_net_command == 'list':    
            print(f'Список изолированных сетей')
            print(self.one.private_net())   

    def infra_handler(self, args):
        # Создание инфраструктуры из шаблона
        if args.infra_command == 'create':
            print(f'Создание инфраструктуры из шаблона: {args.template}')
            
        # Удаление инфраструктуры из шаблона
        elif args.infra_command == 'delete':
            print(f'Удаление инфраструктуры по шаблону: {args.template}')
            
        # Изменение инфраструктуры по шаблону
        elif args.infra_command == 'update':
            print(f'Изменение инфраструктуры по шаблону: {args.template}')

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
        return self.parser.parse_args()

    def run(self):
        args = self.parse_args()
        if args.command == 'server':
            self.server_handler(args)
        elif args.command == "private_net":
            self.private_net_handler(args)    
        elif args.command == 'infra':
            self.infra_handler(args)
        elif args.command == 'deploy':
            self.infra_handler(args)    
        else:
            print('Неизвестная команда')
