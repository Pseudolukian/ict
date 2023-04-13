from core.Service import Service
from core.OneCloud import OneCloudAPI
from core.CLI import CLI
from core.Deploy import Deploy
import sys

service = Service()
one_cloud_api = OneCloudAPI(api_key=service.api_key_caller(), serv = service)
deploy = Deploy(serv = service)
cli = CLI(serv = service, one = one_cloud_api, dep = deploy)

if __name__ == '__main__':
    cli.run()
        