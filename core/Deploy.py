import os, re, subprocess, yaml
from pathlib import Path


class Deploy:
    def __init__(self, serv):
        self.serv = serv

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

    def create_inventory(self, hosts_list, file_name="inventory.ini"):
        playbooks_path = Path("./templates/playbooks/")
        inventory = {}

        for host in hosts_list:
            group = host['playbook'].split('_')[0]
            if group not in inventory:
                inventory[group] = {'hosts': [], 'playbook': host['playbook']}

            inventory[group]['hosts'].append(host)

        with open(file_name, "w") as f:
            for group, data in inventory.items():
                f.write(f"[{group}]\n")
                for host in data['hosts']:
                    host_line = f"{host['Name']} ansible_host={host['IP']} ansible_user={host['User']} ansible_ssh_pass={host['Pass']}\n"
                    f.write(host_line)
                f.write("\n")
                
                group_vars_dir = "group_vars"
                os.makedirs(group_vars_dir, exist_ok=True)
                play_book_path = (playbooks_path / data['playbook']).with_suffix('.yml')
                with open(os.path.join(group_vars_dir, f"{group}.yml"), "w") as group_vars_file:
                    group_vars_file.write(f"playbook: {play_book_path}\n")
        
        return "Ok"  

    def start_ansible(self, inventory_file="inventory.ini"):
        # Получаем имена групп из inventory.ini
        groups = []
        with open(inventory_file, "r") as f:
            for line in f:
                match = re.match(r'\[(\w+)\]', line)
                if match:
                    groups.append(match.group(1))

        if not groups:
            print("Не удалось найти имена групп в файле inventory.ini")
            return

        # Запускаем ansible-playbook для каждой группы
        for group in groups:
            # Загружаем файл переменных из директории group_vars
            group_vars_file = os.path.join("group_vars", f"{group}.yml")
            with open(group_vars_file, "r") as f:
                group_vars = yaml.safe_load(f)

            playbook_path = group_vars["playbook"]

            # Запускаем ansible-playbook с путем к плейбуку и inventory.ini
            ansible_command = f"ansible-playbook -i {inventory_file} {playbook_path} --limit {group}"
            try:
                subprocess.run(ansible_command, shell=True, check=True)
                print(f"Ansible playbook для группы {group} успешно выполнен.")
            except subprocess.CalledProcessError as e:
                print(f"Ошибка при выполнении Ansible playbook для группы {group}: {e}")     
        

