from fastapi import FastAPI
from tagler.healer.retriever import KnowledgeBaseRetriever
from tagler.poller.sql import SqlPoller
from tagler.publisher.sql import SqlPublisher
from tagler.tagger.inference import NLPTagClassifier
from tagler.healer.actions import Email, ServiceNow
from tagler.trainer.nlp_trainer import NLPTagTrainer
from app import predict_exception_tag
import logging as LOGGER
import time


class TagException(BaseModel):
    id:int
    exception:str
    tag:str


app = FastAPI()
sqlPub = SqlPublisher()


@app.get("/")
def home():
    return { "msg": "Welcome to Tagler" }


@app.get('/classify-exception')
async def classify_expection():

    try:
        predict_exception_tag()
        # Get all tagged exception from db
    except:
        return jsonify( 'status' : 400 )

    return jsonify(  ) #return tagged exception to UI


@app.get('/train-model')
async def train_model():
    # Need to think on how to handle the new training data scenario
    try:
        trainer = NLPTagTrainer()
        trainer.train()
    except:
        return jsonify( 'status' : 400 )

    return jsonify( 'status' : 200 )


@app.post('/tag-exception')
async def tag_exception( tagException : TagException ):
    try:
        # Write the tagged exception in table so that it can used for retraining purpose
        sqlPub.prepare_update( tagException.id, tagException.tag )
    except:
        return jsonify( 'status', 400 )

    return jsonify( 'status' : 200 )
