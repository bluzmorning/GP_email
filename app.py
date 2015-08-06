import pyodbc
import base64
import ConfigParser
def do_connect():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    server = config.get("parameters", "sqlserver")
    username = config.get("parameters", "login")
    password = config.get("parameters", "password")
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE=Dynamics;UID='+username+';PWD='+password+'')
    users_query = cnxn.cursor()
    users_query.execute("select USERID from SY01400")
    data_users = users_query.fetchall()
    users_query.close()
    print data_users
do_connect()