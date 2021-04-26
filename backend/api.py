from fastapi import FastAPI
from tagler.healer.retriever import KnowledgeBaseRetriever
from tagler.poller.sql import SqlPoller
from tagler.publisher.sql import SqlPublisher
from tagler.tagger.inference import NLPTagClassifier
from tagler.healer.actions import Email, ServiceNow
from tagler.trainer.nlp_trainer import NLPTagTrainer
from app import predict_exception_tag, get_feedback_rows
from pydantic import BaseModel
import logging as LOGGER
import time


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
async def push_feedback(data):
    import ast
    print(data)
    print(list(data)[0])
    res_list = ast.literal_eval(data)
    print(res_list[0])
    #raw_data = get_feedback_rows()
    #preturn raw_data
