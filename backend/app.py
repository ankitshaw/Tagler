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
sqlPub = SqlPublisher(sqlPol.conn)
sqlPol.set_query_details("logs",2,"exception_input","exception_tag")
sqlPub.set_query_details("logs","id","exception_tag")
serviceNow = ServiceNow()


def continuous_exception_tagging():
    """
        Performs continuous perdiction for all the data
    """
    while True:
        predict_exception_tag()


def predict_exception_tag():
    """
        Performs prediction for all the data present in db performs resolution steps
    """
    for exc in sqlPol.poll():
        nlpTag = nlpTagger.classify_exception(exc[1])
        esTag, heal_action = query_resolution( esRetriever, exc )

        if nlpTag == esTag:
            publish_result( sqlPub, exc[0], nlpTag )
            perform_healing( heal_action )
        else:
            publish_result( sqlPub, exc[0], "Not Processed" )
        #tagging nlp model
        #es rule extract
        #if confident update predicted tag and extract heal condition else update Not Processed and skip heal

    LOGGER.debug( "Sleeping for 2 secs" )
    time.sleep(2)

    # exception_type = self.classify_exception( exception )
    # self.publish_result( exception, EXCEPT_MAPPING.get( exception_type ) )
    # steps = self.query_resolution( exception, exception_type )
    # self.perform_healing( steps )


def publish_result( sqlPub, exception, tag ):
    """
        Publishes the result to output/analytics stream
    """
    sqlPub.prepare_update( ,"Not Processed" )
    sqlPub.write_result()


def perform_healing( heal_action ):
    """
        Performs healing mechanism for the exception occured
    """
    if heal_action == "Raise Ticket": #handle this in a Healer class
        serviceNow.raise_ticket()


def query_resolution( esRetriever, exc ):
    """
        Queries to Elastic search for getting the healing resolution steps
    """
    return esRetriever.get_exception( exc[1], filter={ "queue" : exc[2], "process" : exc[3] } )
