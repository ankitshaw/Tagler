import logging as LOGGER
import time

from tagler.esloader.healer import KnowledgeBaseLoader
from tagler.healer.retriever import KnowledgeBaseRetriever
from tagler.poller.sql import SqlPoller
from tagler.publisher.sql import SqlPublisher
from tagler.publisher.model import SQL_PUSH
from tagler.tagger.inference import NLPTagClassifier
from tagler.healer.actions import Email, ServiceNow

LOGGER.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=LOGGER.DEBUG)
HOST = "enterprise-search-deployment-fa9443.es.ap-east-1.aws.elastic-cloud.com"
USER = "elastic" 
PWD = "JHhtpUXnGsq30zMPYuuXgGeC"

kb = KnowledgeBaseLoader(scheme="https",host=HOST,port=9243, username=USER, password=PWD, index="tagger-healer", search_fields="exception_input")
kb2 = KnowledgeBaseLoader(scheme="https",host=HOST,port=9243, username=USER, password=PWD, index="tagger-healer-stream", search_fields="exception_input")
#kb.load_csv("/workspaces/Tagler-Hackathon/models/kb.csv")

nlpTagger = NLPTagClassifier("../models","cpu")
esRetriever = KnowledgeBaseRetriever(scheme="https",host=HOST,port=9243, username=USER, password=PWD, index="tagger-healer", search_fields="exception_input")
sqlPol = SqlPoller(conn_string="sqlite:///../models/tagler_prd.db")
sqlPub = SqlPublisher(sqlPol.conn)
sqlPol.set_query_details("log_stream","train",100,"exception_input","exception_tag","heal_action")
sqlPub.set_query_details("log_stream","train","id","exception_tag","heal_action")
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
    es_load = []
    for exc in sqlPol.poll():
        print(exc)
        nlpTag = nlpTagger.classify_exception(exc[1])
        esTag, heal_action = query_resolution( esRetriever, exc )
        print(nlpTag)
        print(esTag)
        if nlpTag == esTag or esTag:
            nlpTag=esTag #confidence logic needed
            sqlPub.prepare_update(exc[0],nlpTag,heal_action)
            prepare_result_api(send_data, exc, nlpTag, heal_action)
            perform_healing( heal_action )
        else:
            sqlPub.prepare_update(exc[0],"Not_Processed","Not_Processed")
            prepare_result_api(send_data, exc, "Not_Processed","Not_Processed")
        
    #sqlPub.clear_updates()
    sqlPub.write_result()
    kb2.load_from_ui(prepare_es_load_log(send_data))
    return send_data
        #tagging nlp model
        #es rule extract
    


def get_feedback_rows():
    send_data={"id":[],"exception_input":[],"queue":[],"process":[],"exception_tag":[],"heal_action":[],"entry_time":[]}
    for exc in sqlPol.poll_feedback():
        print(exc)
        send_data = prepare_result_api(send_data, exc, exc[4], exc[5])
    return send_data

def push_feedback_rows(send_data):
    print(send_data)
    sqlPub.set_update(send_data)
    sqlPub.write_result_train()
    es_load = []
    for exc in sqlPol.poll_train():
        print(exc)
        es_load.append(prepare_es_load(exc))
        print(es_load)
    kb.load_from_ui(es_load)
    kb2.load_from_ui(es_load)

def get_train_rows():
    send_data={"id":[],"exception_input":[],"queue":[],"process":[],"exception_tag":[],"heal_action":[],"entry_time":[]}
    for exc in sqlPol.poll_train():
        print(exc)
        send_data = prepare_result_api(send_data, exc, exc[4], exc[5])
    return send_data

def get_log_rows():
    send_data={"id":[],"exception_input":[],"process":[],"queue":[],"exception_tag":[],"heal_action":[],"entry_time":[]}
    for exc in sqlPol.poll():
        print(exc)
        send_data = prepare_result_api(send_data, exc, exc[4], exc[5])
    return send_data

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

def prepare_result_api( send_data, exc, tag, heal):
    """
        Publishes the result to output/analytics stream
    """
    send_data["id"].append(exc[0])
    send_data["exception_input"].append(exc[1])
    send_data["queue"].append(exc[2])
    send_data["process"].append(exc[3])
    send_data["exception_tag"].append(tag)
    send_data["heal_action"].append(heal)
    send_data["entry_time"].append(exc[6])
    
    return send_data


def prepare_es_load_log(send_data):
    es_load = []
    for i in range(len(send_data["id"])):
        if send_data["exception_tag"][i] != "Not_Processed":
            es_load.append({"text":"","id":send_data["id"][i],"exception_input":send_data["exception_input"][i],"queue":send_data["queue"][i],"process":send_data["process"][i],"exception_tag":send_data["exception_tag"][i],"heal_action":send_data["heal_action"][i],"entry_time":send_data["entry_time"][i]})
    return es_load

def prepare_es_load(exc):
    return {"text":"","id":str(exc[0]+100),"exception_input":exc[1],"queue":exc[2],"process":exc[3],"exception_tag":exc[4],"heal_action":exc[5],"entry_time":exc[6]}

def insert_new_log(data):
    sqlPol.new_log(data)

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
#print(predict_exception_tag())
#print(get_feedback_rows())
#push_feedback(send_data=[{"id":106,"tag":"tp","heal":"ok"}])