import os
from pathlib import Path
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.utils.display import Display
from ansible import context
from ansible.cli import CLI
from argparse import Namespace


class Deploy:
    from core.Service import Service
    from core.OneCloud import OneCloudAPI
    serv = Service()
    one = OneCloudAPI(api_key=serv.api_key_caller())

    def prepare_data(self, template):
        
        serv_in_temp = self.serv.server_parser(template_name=template) #List of servers in template
        serv_on_prod = [{"Name":s_p["Name"],"IP":s_p["IP"], "ID": s_p["ID"],
                         "User":s_p["AdminUserName"], "Pass":s_p["AdminPassword"]} for s_p in self.one.server(action="list")]
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
                        'playbook': server_in_temp['playbook']
                    }
                    serv_to_plb_dep.append(server)

        return serv_to_plb_dep

    def deploy(self, servers):
        # Настройка Ansible
        loader = DataLoader()
        inventory = InventoryManager(loader=loader, sources=['/path/to/your/inventory.ini'])
        variable_manager = VariableManager(loader=loader, inventory=inventory)
        display = Display()

        # Инициализация контекста
        context.CLIARGS = Namespace(
            connection='smart',
            forks=10,
            listhosts=None,
            listtasks=None,
            listtags=None,
            syntax=None,
            start_at_task=None,
            tags=[],
            skip_tags=[],
            module_path=None,
            check=False,
            diff=False,
            extra_vars=[]
        )

        for server in servers:
            playbook_path = Path('./templates/instances') / (server["playbook"] + ".yml")
            if not os.path.exists(playbook_path):
                print(f"[ERROR] The playbook {playbook_path} does not exist.")
                continue

            # Настройка и выполнение плейбука
            pb = PlaybookExecutor(
                playbooks=[str(playbook_path)],
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                passwords=dict(vault_pass="secret"),
            )

            # Установка дополнительных переменных для плейбука
            extra_vars = {
                "target": server["Name"],
                "ansible_user": server["User"],
                "ansible_ssh_pass": server["Pass"],
                "ansible_host": server["IP"],
            }
            variable_manager._extra_vars = extra_vars

            # Запуск плейбука
            result = pb.run()
            if result == 0:
                print(f"[SUCCESS] Playbook {playbook_path} executed successfully.")
            else:
                print(f"[ERROR] Playbook {playbook_path} failed with result code {result}.")

