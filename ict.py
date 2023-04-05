from core.Service import Service
from core.OneCloud import OneCloudAPI
import sys, json

service = Service()
one = OneCloudAPI()


if __name__ == "__main__":
    
    if sys.argv[1] == "list":
        print(f" This is first condition: {one.server()}")
    elif sys.argv[1] == "create" and len(sys.argv[2]) > 0:
        print(one.server(action=sys.argv[1], data=sys.argv[2]))    
    elif sys.argv[1] == "delete" and len(sys.argv[2]) > 0:
        print(one.server(action=sys.argv[1], data=sys.argv[2]))    