import pyodbc
import ConfigParser
import pandas as pd
import datetime
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
today = str(datetime.date.today())
def do_connect():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    server = config.get("parameters", "sqlserver")
    username = config.get("parameters", "login")
    password = config.get("parameters", "password")
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE=Dynamics;UID='+username+';PWD='+password+'')
    users_query = cnxn.cursor()
    df = pd.read_sql_query("exec FSSG_wrong_accounttype_report", cnxn, index_col=None)
    writer = pd.ExcelWriter('wrong_accounts_'+today+'.xlsx')
    df.to_excel(writer, sheet_name='account codes in GP')
    writer.sheets['account codes in GP'].column_dimensions['A'].width = 10
    writer.sheets['account codes in GP'].column_dimensions['B'].width = 50
    writer.sheets['account codes in GP'].column_dimensions['C'].width = 20
    writer.sheets['account codes in GP'].column_dimensions['D'].width = 20
    writer.save()
    users_query.close()
def do_sendemail():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    msg = MIMEMultipart()
    recipients = config.get("parameters", "recipients")
    recipients1 = recipients.split(',')
    msg['Subject'] = "Wrong accounts type in Dynamics GP (monthly report)"
    msg['From'] = "FinancialSystemsSupportGroup@NetCracker.com"
    msg['To'] = ", ".join(recipients1)
    msg.preamble = 'Multipart massage.\n'
    part = MIMEText("Hello, team. Please, pay your attention on wrong account type in Dynamics GP. This message has been sent automatically. Thanks.")
    msg.attach(part)
    part = MIMEApplication(open('wrong_accounts_'+today+'.xlsx','rb').read())
    part.add_header('Content-Disposition', 'attachment', filename='wrong_accounts_'+today+'.xlsx')
    msg.attach(part)
    smtp = SMTP("iplanet", 25)
    smtp.ehlo()
    smtp.sendmail(msg['From'], recipients1, msg.as_string())
do_connect()
do_sendemail()