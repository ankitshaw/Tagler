from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.sparse import ElasticsearchRetriever
from haystack.retriever.dense import DensePassageRetriever

class KnowledgeBaseRetriever:
    def __init__(self, scheme:str="http", host:str="localhost", port:int=9200, username:str="", password:str="", index:str="document", search_field:str="text", retriever_type="sparse"):
        self.document_store = ElasticsearchDocumentStore(scheme=scheme, host=host, port=port, username=username, password=password, index=index, search_fields=search_field)
        if retriever_type=="sparse":
            self.retriever = ElasticsearchRetriever(document_store=self.document_store)
        elif retriever_type=="dense":
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
        doc  = self.retriever.retrieve(exception,top_k=2, filters=filter)
        return doc["heal_action"]