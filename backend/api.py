from fastapi import FastAPI
import logging as LOGGER
import time

from tagler.healer.retriever import KnowledgeBaseRetriever
from tagler.poller.sql import SqlPoller
from tagler.publisher.sql import SqlPublisher
from tagler.tagger.inference import NLPTagClassifier
from tagler.healer.actions import Email, ServiceNow
from tagler.trainer.nlp_trainer import NLPTagTrainer
from app import predict_exception_tag


class TagException(BaseModel):
    id:int
    exception:str
    type:str


app = FastAPI()


@app.get("/")
def home():
    return {"msg": "Welcome to Tagler"}


@app.get('/classify-exception')
async def classify_expection():

    predict_exception_tag()

    return jsonify()


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
async def tag_exception( tag : TagException ):
    try:
        # TagException write the tagged exception in new table so that it can used for retraining purpose
        TagException
    except:
        return jsonify( 'status', 400 )

    return jsonify( 'status' : 200 )
