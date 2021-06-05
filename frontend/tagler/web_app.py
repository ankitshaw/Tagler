"""Main module for the streamlit app"""
import streamlit as st
import pages.welcome
import pages.tagger
import pages.insert
import pages.feedback
import pages.training
import pages.load_logs
from utils import load_css

PAGES = {
    "Welcome": pages.welcome,
    "Log Tagger": pages.tagger,
    "Train Feedback": pages.feedback,
    "Create New Log": pages.insert,
    "Trained Exception": pages.training,
    "Load Logs": pages.load_logs,
}


def main():
    st.set_page_config(page_title="Ernst & Young - Tagler: Smart Exception Tagger and Healer",page_icon="⚠️",layout="wide")
    load_css("./css/my.css")  
    #st.write('<style>body { margin: 0; font-family: Arial, Helvetica, sans-serif;} .header{padding: 10px 16px; background: #000000; color: #ffffff; position:fixed;top:0;} .sticky { position: fixed; top: 0; width: 300%;} </style><div class="header" id="myHeader">Tagler</div>', unsafe_allow_html=True)
    st.sidebar.image("./images/favicon.png", width=100)
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    page.write()

if __name__ == "__main__":
    main()
