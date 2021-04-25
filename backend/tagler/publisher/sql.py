import pyodbc
from sqlalchemy import create_engine
from sqlalchemy import desc, select, Table
from sqlalchemy import MetaData, Table, String, Column, Text, DateTime, Boolean, text
from datetime import datetime

class SqlPublisher:
    def __init__(self, connection):
        self.conn = connection
        self.update = [];
        self.start = "BEGIN TRANSACTION;"
        self.end = "COMMIT;"
    
    def write_result(self):
        if len(self.update) != 0:
            self.conn.execute(self.query,self.update)
        self.clear_updates()
    
    def clear_updates(self):
        self.update = []

    def set_query_details(self, table:str, idColumn:str, statusColumn:str, healColumn:str):
        self.idColumn =idColumn
        self.statusColumn = statusColumn
        self.table = table
        self.healColumn = healColumn
        self.query = text("UPDATE " + self.table + " SET " + self.statusColumn + " = :tag ," + self.healColumn + " = :heal WHERE " + self.idColumn + "= :id")

    def prepare_update(self, id:int, tag:str, heal:str):
        self.update.append({"tag":tag,"id":str(id), "heal":heal})
            #"UPDATE " + self.table + " SET " + self.statusColumn + " = " + tag + " WHERE " + self.idColumn + " = " + str(id) + ";"
