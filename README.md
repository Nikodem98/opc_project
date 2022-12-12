# OPC database
Simple implementation of docker postgre database with python subscripion client and rest API.

## How to run it?
1. Download docker and git
2. Clone git repository 
```bash
$ git clone https://github.com/Nikodem98/opc_project.git
```
3. In the terminal enter the root folder of the project and type the command:
```bash
$ docker-compose up
```
4. Now, you need to wait for database system to run (PostreSQL database is running at this point. Use http://localhost:5001 to connect.).
5. In the terminal enter the cilent-app folder of the project and type the command:
```bash
$ python main.py
```