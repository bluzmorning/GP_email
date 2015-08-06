import pyodbc
import ConfigParser
import pandas as pd
def do_connect():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    server = config.get("parameters", "sqlserver")
    username = config.get("parameters", "login")
    password = config.get("parameters", "password")
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE=Dynamics;UID='+username+';PWD='+password+'')
    users_query = cnxn.cursor()
    df = pd.read_sql_query("exec AccountsPostingType", cnxn)
    writer = pd.ExcelWriter('foo.xlsx')
    df.to_excel(writer, sheet_name='bar')
    writer.save()
    users_query.close()
do_connect()