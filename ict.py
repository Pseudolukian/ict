from core.Service import Service
from core.OneCloud import OneCloudAPI
from core.CLI import CLI
from core.Deploy import Deploy

service = Service()
one = OneCloudAPI(api_key=service.api_key_caller())
cli = CLI()



if __name__ == '__main__':
    cli.run()
        