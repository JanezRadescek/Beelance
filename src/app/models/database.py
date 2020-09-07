import mysql.connector
from dotenv import load_dotenv
import os
import configparser

groupid = os.getenv("groupid").lstrip("0")

"""
Connect the webserver to the database using the python mysql connecter. 
Change the host address depending on where the mysql server is running. To connect to the 
preconfigured docker container address use the Docker address. The default port is 3306.
"""
config = configparser.ConfigParser()
config.read('config_ex.ini')
db = mysql.connector.connect(
    user=config['dbadmin']['User'],
    password=config['dbadmin']['Password'],
    host='10.' + groupid + '.0.5',   # Docker address
    #host='0.0.0.0',    # Local address
    database=config['dbadmin']['Database']
)
    
