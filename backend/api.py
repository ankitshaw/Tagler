from fastapi import FastAPI
from tagler.healer.retriever import KnowledgeBaseRetriever
from tagler.poller.sql import SqlPoller
from tagler.publisher.sql import SqlPublisher
from tagler.tagger.inference import NLPTagClassifier
from tagler.healer.actions import Email, ServiceNow
from tagler.trainer.nlp_trainer import NLPTagTrainer
from app import predict_exception_tag, get_feedback_rows, push_feedback_rows, get_train_rows, get_log_rows, insert_new_log
from pydantic import BaseModel
from tagler.publisher.model import SQL_PUSH
import logging as LOGGER
import time
import ast
from typing import List, Dict


app = FastAPI()
#sqlPub = SqlPublisher()


@app.get("/")
def home():
    return { "msg": "Welcome to Tagler" }


@app.get('/classify-exception')
async def classify_expection():
    raw_data = predict_exception_tag()
    # try:
    #     raw_data = predict_exception_tag()
    #     # Get all tagged exception from db
    # except:
    #     return {'status' : 400}

    return raw_data #return tagged exception to UI


# @app.get('/train-model')
# async def train_model():
#     # Need to think on how to handle the new training data scenario
#     try:
#         trainer = NLPTagTrainer()
#         trainer.train()
#     except:
#         return jsonify({'status' : 400})

#     return jsonify({'status' : 200} )


@app.get('/tag-exception')
async def tag_exception():
    raw_data = get_feedback_rows()
    return raw_data

@app.post('/push-feedback')
async def push_feedback(data: List[Dict]):
    #data = ast.literal_eval(data)
    print(data[0]['id'])
    push_feedback_rows(data)
    #resp = push_feedback_rows(data)

@app.get('/training_rows')
async def training_rows():
    raw_data = get_train_rows()
    return raw_data

@app.get('/new_log_rows')
async def new_log_rows():
    raw_data = get_log_rows()
    return raw_data

@app.post('/insert')
async def insert(data:List):
    raw_data = insert_new_log(data)