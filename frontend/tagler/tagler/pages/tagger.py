import requests
import streamlit as st
import os
from utils import poll_tag, load_css
import pandas as pd


def write():
	load_css("./css/my.css")
	st.markdown('<p class="big-font">Tagger Poll</p>', unsafe_allow_html=True)
	
	run_query = st.button("Poll")
	if run_query:
		with st.spinner("Retrieving and Tagging the Exceptions from DB..."):
			df = poll_tag(run_query)

		st.write("## Tagged Exceptions:")
		st.write(pd.DataFrame(df))