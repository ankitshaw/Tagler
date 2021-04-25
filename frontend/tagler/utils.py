import requests
import streamlit as st
import os

API_ENDPOINT = os.getenv("API_ENDPOINT", "https://haystack-demo-api.deepset.ai")
MODEL_ID = "1"
DOC_REQUEST = "query"
TAGGER = "classify-exception"
INSERT = "insert"


@st.cache(show_spinner=False)
def insert_db(query):
   url = API_ENDPOINT + "/" + INSERT
   response_raw = requests.post(url, json={"query":query})
   return response_raw

#@st.cache(show_spinner=False) //Check 
def poll_tag(file):
   url = API_ENDPOINT + "/" + TAGGER
   resp = requests.get(url)
   print(resp)
   return json2Df(resp.json())

def json2Df(resp):
  return resp







def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

