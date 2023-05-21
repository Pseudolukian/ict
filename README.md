# What is 1cloud ict?
1cloud ict is a terminal utility for managing 1cloud servers, deploying project code to servers, and setting up environments on them. Ict follows two basic principles:

Idempotency in operation - actions over servers are not repeated when multiple access to the infrastructure file is made;
Infrastructure file - this is the only correct source of data for ict.
When working through ict, all changes in the state of 1cloud servers are made through the infrastructure file. Meanwhile, the user can make any changes to the state of servers through the 1cloud web panel, but when accessing the infrastructure file next time, the state of the servers will be brought into line with it.

# How does ict work?
Whenever the infra update command is executed, ict compares the quantity, statuses, and states of servers in the 1cloud Panel with the parameters and servers in the infrastructure file, when discrepancies are found, ict brings the state of servers in the 1cloud Panel to the state of servers in the infrastructure file.

When executing the infra deploy command, ict again performs a comparison of the state of servers in the 1cloud Panel with what is indicated in the infrastructure file. If there are no discrepancies, an Ansible inventory file will be created and executed, if discrepancies are there, ict will notify about this and request confirmation for changes in the state of servers in the 1cloud Panel. After that, the process of creating and executing an Ansible inventory file will be carried out.

# What can ict do?
Ict can create and delete 1cloud virtual servers, as well as change their configuration. Ict can connect to servers via SSH and work with their environment: deploy project code to the server, configure environments, and much more. For this, it uses Ansible.

In real time, ict collects server load statistics. It does this by parsing node_exporter data, which is automatically installed after creating a server using Ansible.

## What needs to be remade/completed/done:
 - Integrate Pydantic into the Ansible workflow 🚨 High
 - Write docstrings for all functions, classes, modules, packages 🚨 High
 - Cover code with tests 🚨 High
 - Write a playbook for installing node_exporter 🟠 Medium
 - Write a daemon collecting stats from servers 🟠 Medium
 - Consider how to implement group server management: stop, start, reboot 🟠 Medium
 - Learn about code coverage 🟠 Medium
 - Consider how to implement networking 🟢 Normal
 - Develop a rollback system 🟢 Normal
 - Develop an alert system 🟢 Normal
 - Develop a scheduling system 🟢 Normal

## Release notes:
### Beta_01
- Introduced Pydantic models in all processes related to working with infrastructure templates and 1cloud API
- Redid the logic of working with the infrastructure file. Now there is only one command infra update temp_name
### Alpha_10:
- Created a tests directory;
- Began writing tests for the ready-made functions;
- Started a new section for maintaining a list of tests;
- Refactored Self.conf_worker();
### Alpha_09:
- Removed the Deploy class, distributing it to the Sevice, Prepare and Ansible classes;
- Created a new Anible class;
- Created a new Prepare class;
- Redid the logic of the hosts file. Now it is in yaml format, and the links to playbooks are also in it in the form of variables.
### Alpha_08:
- Moved to Codespaces: set up a container with Python3.11
- Moved the project to Python 3.11
- Created a Dev branch
### Alpha_07:
- Removed cyclic dependencies. Now class instances are passed as arguments.