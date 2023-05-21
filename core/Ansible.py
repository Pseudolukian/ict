import subprocess
import yaml



class Ansible:
    """
    Represents an Ansible instance that can start Ansible and run playbooks for hosts specified in the inventory.

    Args:
        serv (str): The name or description of the Ansible service.

    Attributes:
        serv (str): The name or description of the Ansible service.
    """
    def __init__(self, serv):
        self.serv = serv


    def start_ansible(self, inventory="./hosts.yml"):
        """
        Starts Ansible and runs playbooks for hosts specified in the inventory.

        Args:
            inventory (str, optional): Path to the Ansible inventory file. Defaults to "./hosts.yml".

        Returns: None

        Raises:
            subprocess.CalledProcessError: If the execution of the Ansible playbook fails.
        """
       # Read and parse the inventory file
        with open(inventory, 'r') as file:
            inventory_data = yaml.safe_load(file)

        # Extract groups and their playbooks
        groups = inventory_data['all']['children']

        for group_name, group_data in groups.items():
            hosts = group_data['hosts']
            for host_name, host in hosts.items():
                playbook = host['ansible_playbook']
                cmd = f"ansible-playbook -i {inventory} -l {host_name} {playbook}"
                try:
                    result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                    print(f"Ansible playbook {playbook} completed successfully for host {host_name}.")
                    print("Output:", result.stdout)
                except subprocess.CalledProcessError as error:
                    print(f"Ansible playbook {playbook} failed for host {host_name}.")
                    print("Return code:", error.returncode)
                    print("Output:", error.stdout)
                    print("Error output:", error.stderr)