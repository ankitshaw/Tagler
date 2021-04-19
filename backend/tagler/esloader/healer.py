from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.file_converter.base import BaseConverter
from haystack.file_converter.docx import DocxToTextConverter
from haystack.file_converter.pdf import PDFToTextConverter
from haystack.file_converter.txt import TextConverter
from haystack.preprocessor.preprocessor import PreProcessor

from typing import List, Optional, Generator, Set

import re
import os
import pandas as pd


class KnowledgeBaseLoader:
    def __init__(self, scheme:str="http", host:str="localhost", port:int=9200, username:str="", password:str="", index:str="document"):
        self.document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")
    
    def load(self, dir):
        df = pd.read_csv("filename.csv")
        docs = self.preprocessor(df)
        self.document_store.write_documents(docs)
    
    def preprocess(self, dir, documentCol:str, exceptionCol:str):
        processor = PreProcessor(clean_empty_lines=True,
                    clean_whitespace=True,
                    clean_header_footer=True,
                    split_by="word",
                    split_length=200,
                    split_respect_sentence_boundary=True)

        documents = []
        columns = df.columns
        for index, row in df.iterrows():
            for col in columns:
                if col == "input":
            text = self.clean(text)
            details = self.extract_details(text,exceptions)
            documents.append({"text": text, "details": details, "meta": {"name": path.name}})

        return documents

    def clean(self, document: str) -> str:
        text = document
        lines = text.splitlines()
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            cleaned_lines.append(line)
        text = "\n".join(cleaned_lines)
        text = re.sub(r"\n\n+", "\n\n", text)

        return text

    def extract_details(self, doc:str):
        #Queue	Process	Predicted Exception Tag	Self-Heal (Dummy)	TimeStamp
        return {}
