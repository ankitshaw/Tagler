from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from typing import List, Optional, Generator, Set
import pandas as pd

class KnowledgeBaseLoader:
    def __init__(self, scheme:str="http", host:str="localhost", port:int=9200, username:str="", password:str="", index:str="document"):
        self.document_store = ElasticsearchDocumentStore(scheme=scheme, host=host, port=port, username=username, password=password, index=index)
    
    def load_csv(self, dir:str):
        df = pd.read_csv(dir)
        docs = self.format_to_dict(df)
        self.document_store.write_documents(docs)
    
    def format_to_dict(self, df):
        documents = []
        columns = df.columns
        for index, row in df.iterrows():
            doc = {"text":""}
            for col in columns:
                doc[col] = row[col] 
            documents.append(doc)

        return documents
    
    def load_table(self):
        #To be taken up if needed
        pass