import logging as LOGGER
import time

from tagler.esloader.healer import KnowledgeBaseLoader
from tagler.healer.retriever import KnowledgeBaseRetriever
from tagler.poller.sql import SqlPoller
from tagler.publisher.sql import SqlPublisher
from tagler.tagger.inference import NLPTagClassifier
from tagler.healer.actions import Email, ServiceNow


# kb = KnowledgeBaseLoader(scheme="https",host=HOST,port=9243, username=USER, password=PWD, index="tagger-healer", search_fields="exception_input")
# kb.load_csv("/workspaces/Tagler-Hackathon/models/kb.csv")

nlpTagger = NLPTagClassifier("/workspaces/Tagler-Hackathon/models","cpu")
esRetriever = KnowledgeBaseRetriever(scheme="https",host=HOST,port=9243, username=USER, password=PWD, index="tagger-healer", search_fields="exception_input")
sqlPol = SqlPoller(conn_string="sqlite:////workspaces/Tagler-Hackathon/models/tagler_prd.db")
sqlPub = SqlPublisher(sqlPol.conn)
sqlPol.set_query_details("log_stream",2,"exception_input","exception_tag")
sqlPub.set_query_details("logs","stream","exception_tag","heal_action")
serviceNow = ServiceNow()


def continuous_exception_tagging():
    """
        Performs continuous perdiction for all the data
    """
    while True:
        tag_one_batch()
        LOGGER.debug( "Sleeping for 5 secs" )
        time.sleep(5)


def predict_exception_tag():
    """
        Performs prediction for all the data present in db performs resolution steps
    """
    send_data={"id":[],"exception_input":[],"process":[],"queue":[],"exception_tag":[],"heal_action":[],"entry_time":[]}
    for exc in sqlPol.poll():
        print(exc)
        nlpTag = nlpTagger.classify_exception(exc[1])
        esTag, heal_action = query_resolution( esRetriever, exc )
        print(nlpTag)
        print(esTag)
        if nlpTag == esTag:
            sqlPub.prepare_update(exc[0],nlpTag,heal_action)
            prepare_result_api(send_data, exc, nlpTag, heal_action)
            perform_healing( heal_action )
        else:
            sqlPub.prepare_update(exc[0],"Not Processed","Not Healed")
            prepare_result_api(send_data, exc, "Not_Processed", "Not_Healed")
        
    sqlPub.clear_updates()
    #sqlPub.write_result()
    return send_data
        #tagging nlp model
        #es rule extract
        #if confident update predicted tag and extract heal condition else update Not Processed and skip heal


    # exception_type = self.classify_exception( exception )
    # self.publish_result( exception, EXCEPT_MAPPING.get( exception_type ) )
    # steps = self.query_resolution( exception, exception_type )
    # self.perform_healing( steps )

def tag_one_batch():
    for exc in sqlPol.poll():
        nlpTag = nlpTagger.classify_exception(exc[1])
        esTag, heal_action = query_resolution( esRetriever, exc )

        if nlpTag == esTag:
            sqlPub.prepare_update(exc[0],nlpTag,heal_action)
            perform_healing( heal_action )
        else:
            sqlPub.prepare_update(exc[0],"Not Processed","Not Healed")
    
    sqlPub.write_result()

def prepare_result_api( send_data, exc, tag, heal ):
    """
        Publishes the result to output/analytics stream
    """
    send_data["id"].append(exc[0])
    send_data["exception_input"].append(exc[1])
    send_data["process"].append(exc[2])
    send_data["queue"].append(exc[3])
    send_data["exception_tag"].append(tag)
    send_data["heal_action"].append(heal)
    send_data["entry_time"].append(exc[6])
    
    return send_data



def perform_healing( heal_action ):
    """
        Performs healing mechanism for the exception occured
    """
    return "HEALED"
    if heal_action == "Raise Ticket": #handle this in a Healer class
        serviceNow.raise_ticket()


def query_resolution( esRetriever, exc ):
    """
        Queries to Elastic search for getting the healing resolution steps
    """
    return esRetriever.get_exception( exc[1], filter={ "queue" : [exc[2]], "process" : [exc[3]] } )


def ngrok():
    from pyngrok import ngrok

    # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
    # when starting the server
    port = 8000

    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port).public_url
    LOGGER.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    # Update any base URLs or webhooks to use the public ngrok URL

    #init_webhooks(public_url)

ngrok()