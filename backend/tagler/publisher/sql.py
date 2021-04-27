import pyodbc
from sqlalchemy import create_engine
from sqlalchemy import desc, select, Table
from sqlalchemy import MetaData, Table, String, Column, Text, DateTime, Boolean, text
from datetime import datetime
from typing import List

class SqlPublisher:
    def __init__(self, connection):
        self.conn = connection
        self.update = [];
        self.trainRows = [];
        self.start = "BEGIN TRANSACTION;"
        self.end = "COMMIT;"
    
    def write_result(self):
        if len(self.update) != 0:
            print(self.update)
            self.conn.execute(self.query,self.update)
        self.clear_updates()
    
    def write_result_train(self):
        if len(self.update) != 0:
            print(self.update)
            print(self.trainRows)
            self.conn.execute(self.query,self.update)
            self.conn.execute(self.train,self.update)
        self.clear_updates()
    
    def clear_updates(self):
        self.update = []
        self.trainRows = []

    def set_query_details(self, table:str, trainTable:str, idColumn:str, tagColumn:str, healColumn:str):
        self.idColumn =idColumn
        self.tagColumn = tagColumn
        self.table = table
        self.healColumn = healColumn
        self.trainTable = trainTable
        self.query = text("UPDATE " + self.table + " SET " + self.tagColumn + " = :tag ," + self.healColumn + " = :heal WHERE " + self.idColumn + "= :id")
        self.train = text("INSERT INTO " + self.trainTable + " SELECT * FROM " + self.table + " WHERE " + self.idColumn + "= :id")

    def prepare_update(self, id:int, tag:str, heal:str):
        self.update.append({"tag":tag,"id":str(id), "heal":heal})
            #"UPDATE " + self.table + " SET " + self.statusColumn + " = " + tag + " WHERE " + self.idColumn + " = " + str(id) + ";"

    def set_update(self, update:List):
        self.update = update
        print(self.update)
        #self.trainRows.append({"id":str(id)})