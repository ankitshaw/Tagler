import pyodbc

class SqlPoller:
    def __init__(self, server: str, port: int, driver: str, database: str, username: str, password: str, table:str, batchSize:int, logColumn:str, statusColumn: str):
        self.conn = pyodbc.connect('DRIVER={'+driver+'};SERVER='+server+':'+str(port)+';DATABASE='+database+';UID='+username+';PWD='+ password)
        self.cursor = self.conn.cursor()
        self.query = "SELECT TOP " + str(batchSize) + " " + logColumn + " FROM " + table + " Where " + statusColumn + " = Not Processed"
    
    def poll(self):
        self.cursor.execute(self.query)
        return self.cursor.fetchall()
    
    def getMaxId(self):
        pass
