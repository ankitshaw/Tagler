import pyodbc

class SqlPoller:
    def __init__(self, server: str, port: int, driver: str, database: str, username: str, password: str, table:str, batchSize:int, logColumn:str, uidColumn: str):
        self.conn = pyodbc.connect('DRIVER={'+driver+'};SERVER='+server+':'+str(port)+';DATABASE='+database+';UID='+username+';PWD='+ password)
        self.cursor = self.conn.cursor()
        self.query = "SELECT TOP " + str(batchSize) + " " + logColumn + " FROM " + table + " Where " + uidColumn + " > "
    
    def poll(self):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def getMaxId(self):
        pass
