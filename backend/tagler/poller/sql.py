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
        self.create_table_schema()
        self.new_log_query = text("SELECT * FROM " + self.table + " Where " + self.statusColumn + " = '' ORDER BY date(entry_time)  DESC LIMIT " + str(self.batchSize))
        self.not_tag_query = text("SELECT * FROM " + self.table + " Where " + self.statusColumn + " = 'Not_Processed' OR " + self.healColumn + " = 'Not_Processed' ORDER BY date(entry_time)  DESC")
        self.train_query = text("SELECT * FROM " + self.trainTable)
    
    def create_table_schema(self):
        # metadata = MetaData()
        # self.log_table = Table('log_table', metadata,
        #     Column('id', Integer(), primary_key=True),
        #     Column('exception_input', String(300), nullable=False),
        #     Column('process', String(30), nullable=False),
        #     Column('queue', String(30), nullable=False),
        #     Column('exception_tag', String(30), nullable=True),
        #     Column('heal_action', String(50), nullable=True),
        #     Column('entry_time', DateTime(), default=datetime.now),
        # )
        #metadata.create_all(self.engine)
        pass