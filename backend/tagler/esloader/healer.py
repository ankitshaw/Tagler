from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
import pandas as pd

from os import path

class KnowledgeBaseLoader:
    def __init__(self, scheme:str="http", host:str="localhost", port:int=9200, username:str="", password:str="", index:str="document"):
        self.document_store = ElasticsearchDocumentStore(scheme=scheme, host=host, port=port, username=username, password=password, index=index)
    
    def load_csv(self, filepath:str):
        if path.exists(filepath):
            df = pd.read_csv(filepath)
        else:
            raise FileNotFoundError("The knowledge base path passed or the directory does not exists: " + filepath +
                                    "\nPlease check if the path is correct")

        self.docs = self.format_to_dict(df)
        self.document_store.write_documents(docs)
    
    def format_to_dict(self, df):
        documents = []
        columns = df.columns  #check if the column names are are as per requirement (text, exception_msg, predicted_tag, needed)

        for index, row in df.iterrows():
            for col in columns:
                doc[col] = row[col] 
            documents.append(doc)

        return documents
    
    def load_sql_table(self):
        #To be taken up if needed
        pass