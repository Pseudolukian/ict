from core.Service import Service
from core.OneCloud import OneCloudAPI
from core.CLI import CLI
from core.Ansible import Ansible
from core.Prepare import Prepare

service = Service()
one_cloud_api = OneCloudAPI(api_key=service.api_key_caller(), serv = service)
ansible = Ansible(serv = service)
prep = Prepare()
cli = CLI(serv = service, one = one_cloud_api, ans = ansible , pre = prep)

if __name__ == '__main__':
    cli.run()
        