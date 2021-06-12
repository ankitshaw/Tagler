import requests
import streamlit as st
import os
import json

API_ENDPOINT = os.getenv("API_ENDPOINT", "http://api:8000")
MODEL_ID = "1"
DOC_REQUEST = "query"
TAGGER = "classify-exception"
FEEDBACK = "tag-exception"
PUSH = "push-feedback"
INSERT = "insert"
TRAINING_ROWS = "training_rows"
LOG_ROWS="new_log_rows"
RESET="reset"

headers = {'Content-Type': 'application/json', 'Accept':'application/json'}


def insert_db(data):
   url = API_ENDPOINT + "/" + INSERT
   response_raw = requests.post(url,data = json.dumps(data), headers = headers)
   return json2Df(response_raw.json())

def reset():
   url = API_ENDPOINT + "/" + RESET
   response_raw = requests.get(url)
   return json2Df(response_raw.json())

#@st.cache(show_spinner=False) //Check 
def poll_tag(file):
   url = API_ENDPOINT + "/" + TAGGER
   resp = requests.get(url)
   print(resp)
   return json2Df(resp.json())

def json2Df(resp):
  return resp

#@st.cache(show_spinner=False)
def poll_feedback(file):
   url = API_ENDPOINT + "/" + FEEDBACK
   resp = requests.get(url)
   print(resp)
   return json2Df(resp.json())


def push_feedback(data):
   url = API_ENDPOINT + "/" + PUSH
   headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
   resp = requests.post(url,data = json.dumps(data), headers = headers)
   return json2Df(resp.json())

def poll_training(file):
   url = API_ENDPOINT + "/" + TRAINING_ROWS
   resp = requests.get(url)
   print(resp)
   return json2Df(resp.json())

def poll_log(file):
   url = API_ENDPOINT + "/" + LOG_ROWS
   print(url)
   resp = requests.get(url)
   print(resp.json)
   return json2Df(resp.json())






def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

