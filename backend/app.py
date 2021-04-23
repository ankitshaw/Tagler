import logging as LOGGER
import time

from tagler.healer.retriever import KnowledgeBaseRetriever
from tagler.poller.sql import SqlPoller
from tagler.publisher.sql import SqlPublisher
from tagler.tagger.inference import NLPTagClassifier
from tagler.healer.actions import Email, ServiceNow

LOGGER.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=LOGGER.DEBUG)

nlpTagger = NLPTagClassifier("/workspaces/Tagler-Hackathon/models")
esRetriever = KnowledgeBaseRetriever()
sqlPol = SqlPoller(conn_string="sqlite:///tagler.db",)
sqlPub = SqlPublisher(s.conn)
sqlPol.set_query_details("logs",2,"exception_input","exception_tag")
sqlPub.set_query_details("logs","id","exception_tag")
serviceNow = ServiceNow()

while True:
    for exc in sqlPol.poll():
        nlpTag = nlpTagger.classify_exception(exc[1])
        esTag, heal_action = esRetriever.get_exception(exc[1], filter={"queue":exc[2],"process":exc[3]})
        if nlpTag == esTag:
            sqlPub.prepare_update(exc[0],nlpTag)
            if heal_action == "Raise Ticket": #handle this in a Healer class
                serviceNow.raise_ticket()
            
        else:
            sqlPub.prepare_update(exc[0],"Not Processed")
        #tagging nlp model
        #es rule extract
        #if confident update predicted tag and extract heal condition else update Not Processed and skip heal
        

    sqlPub.write_result()    
    LOGGER.debug("Sleeping for 5 secs")
    time.sleep(5)


#
# def publish_result( self, exception, result ):
#     """
#         Publishes the result to output/analytics stream
#     """
#     pass
#
#
# def perform_healing( self, steps ):
#     """
#         Performs healing mechanism for the exception occured
#     """
#     pass
#
#
# def query_resolution( self, exception, exception_type ):
#     """
#         Queries to Elastic search for getting the healing resolution steps
#     """
#     pass
#
#
# def predict( self, exception ):
#     """
#     Classifies type of exception and performs the resolution steps
#
#     Returns:
#     --------
#         bool - True is successful classification else false
#     """
#     try:
#
#         exception_type = self.classify_exception( exception )
#         self.publish_result( exception, EXCEPT_MAPPING.get( exception_type ) )
#         steps = self.query_resolution( exception, exception_type )
#         self.perform_healing( steps )
#
#     except Exception as e:
#         return False
#
#     return True
