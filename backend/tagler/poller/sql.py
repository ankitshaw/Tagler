import pyodbc
from sqlalchemy import create_engine
from sqlalchemy import desc, select, Table
from sqlalchemy import MetaData, Table, String, Column, Text, DateTime, Boolean, text
from datetime import datetime

class SqlPoller:
    def __init__(self, conn_string:str, server: str=None, port: int=None, driver: str=None, database: str=None, username: str=None, password: str=None):
        if conn_string:
            self.engine = create_engine(conn_string)
            self.conn = self.engine.connect()
        else: 
            self.conn = pyodbc.connect('DRIVER={'+driver+'};SERVER='+server+':'+str(port)+';DATABASE='+database+';UID='+username+';PWD='+ password)
            self.cursor = self.conn.cursor()
        self.reset_data()
    
    def poll(self):
        #self.cursor.execute(self.query)
        #self.cursor.fetchall()
        return self.conn.execute(self.new_log_query)

    def poll_feedback(self):
        print(self.not_tag_query)
        return self.conn.execute(self.not_tag_query)
    
    def poll_train(self):
        return self.conn.execute(self.train_query)
    
    def set_query_details(self, table:str, trainTable:str, batchSize:int, logColumn:str, statusColumn: str, healColumn: str):
        self.table = table
        self.batchSize = batchSize
        self.logColumn = logColumn
        self.statusColumn = statusColumn
        self.healColumn = healColumn
        self.trainTable = trainTable
        #self.query = "SELECT TOP " + str(batchSize) + " " + logColumn + " FROM " + table + " Where " + statusColumn + " = Not Processed"
        #self.query = "SELECT TOP " + str(self.batchSize) + " * " + "FROM " + self.table + " Where " + statusColumn + " = ''"
        self.new_log_query = text("SELECT * FROM " + self.table + " Where " + self.statusColumn + " = '' ORDER BY date(entry_time)  DESC LIMIT " + str(self.batchSize))
        self.not_tag_query = text("SELECT * FROM " + self.table + " Where " + self.statusColumn + " = 'Not_Processed' OR " + self.healColumn + " = 'Not_Processed' ORDER BY date(entry_time)  DESC")
        self.train_query = text("SELECT * FROM " + self.trainTable)
    
    def reset_data(self):
        print("Resetting Data...")
        self.conn.execute("DELETE FROM log_stream")
        self.conn.execute("DELETE FROM train")
        print("Resetting Done...")
        #self.conn.execute('insert into log_stream values(101,"Invite not found in both CBS mailbox","Queue-12","Process-9","","","1/2/21 11:45")');
        #self.conn.execute('insert into log_stream values(102,"Interviewer xxxx mail ID not found in invite.","Queue-12","Process-9","","","1/2/21 11:55")');
        #self.conn.execute('insert into log_stream values(103,"Invite not found in both TAX and PAS mailbox","Queue-12","Process-9","","","1/2/21 12:05")');
        #self.conn.execute('insert into log_stream values(104,"InternalFailed to evaluate expression Replace([MailBody],$Item$,[Mail_Data.ID]) - The collection has no c","Queue-14","Process-11","","","1/2/21 12:15")');
        #self.conn.execute('insert into log_stream values(105,"Could not execute code stage because exception thrown by code stage: The given key was not present in the dictionary.","Queue-16","Process-13","","","1/2/21 12:25")');
        #self.conn.execute('insert into log_stream values(106,"Error makes no sense has please call ps support","Queue-99","Process-13","","","1/2/21 12:35")');
        #self.conn.execute('insert into log_stream values(107,"Error makes no sense has please call ps support","Queue-11","Process-11","","","1/2/21 12:45")');
        #self.conn.execute('insert into log_stream values(108,"Bot could not find the right email template from the mail box","Queue-10","Process-10","","","1/2/21 12:55")');
        
    def new_log(self,data):
        for d in data:
            if d[0]!=0:
                self.conn.execute('insert into log_stream values('+str(d[0])+',"'+d[1]+'","'+d[2]+'","'+d[3]+'","'+d[4]+'","'+d[5]+'","'+d[6]+'")');
    