"""Main module for the streamlit app"""
import streamlit as st
import pages.welcome
import pages.tagger
import pages.insert
import pages.feedback
from utils import load_css

PAGES = {
    "Welcome": pages.welcome,
    "Tagger Exception": pages.tagger,
    "Insert to DB": pages.insert,
    "Feedback": pages.feedback,
}


def main():
    st.set_page_config(layout="wide")
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    page.write()

if __name__ == "__main__":
    main()
