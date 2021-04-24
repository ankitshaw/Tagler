import requests
import streamlit as st
import os

API_ENDPOINT = os.getenv("API_ENDPOINT", "https://haystack-demo-api.deepset.ai")
MODEL_ID = "1"
DOC_REQUEST = "query"
TAGGER = "tagger"
INSERT = "insert"


@st.cache(show_spinner=False)
def insert_db(query):
   url = API_ENDPOINT + "/" + INSERT
   response_raw = requests.post(url, json={"query":query})
   return response_raw

@st.cache(show_spinner=False)
def poll_tag(file):
   url = API_ENDPOINT + "/" + TAGGER
   response_raw = requests.post(url)
   return json2Df(resp)

def json2Df(resp):
  pass







def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

