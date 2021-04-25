from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.sparse import ElasticsearchRetriever
from haystack.retriever.dense import DensePassageRetriever

class KnowledgeBaseRetriever:
    def __init__(self, scheme:str="http", host:str="localhost", port:int=9200, username:str="", password:str="", index:str="document", search_fields:str="text", retriever_type="sparse"):
        self.document_store = ElasticsearchDocumentStore(scheme=scheme, host=host, port=port, username=username, password=password, index=index, search_fields=search_fields)
        if retriever_type=="sparse":
            self.retriever = ElasticsearchRetriever(document_store=self.document_store)
        elif retriever_type=="dense": #Experimental 
            self.retriever = DensePassageRetriever(document_store=self.document_store, 
                                      query_embedding_model="facebook/dpr-question_encoder-single-nq-base", # shift these to yaml? download the models
                                      passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
                                      max_seq_len_query=64,
                                      max_seq_len_passage=256,
                                      batch_size=2,
                                      use_gpu=True,
                                      embed_title=True,
                                      use_fast_tokenizers=True
                                      )

    def get_heal_action(self, exception:str, filter:dict=None):
        doc  = self.retriever.retrieve(exception,top_k=1, filters=filter) #to check if first element is the best match or is it random seq
        return doc[0]["heal_action"]
    
    def get_exception(self, exception:str, filter:dict=None):
        doc  = self.retriever.retrieve(exception,top_k=1, filters=filter)
        if len(doc) != 0:
            doc = doc[0].to_dict()
            return doc["meta"]["exception_tag"], doc["meta"]["heal_action"]