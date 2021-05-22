import requests
import streamlit as st
import os
from utils import poll_tag, load_css, poll_log
import pandas as pd


def write():
	load_css("./css/my.css")
	st.markdown('<p class="big-font">Log Tagger</p>', unsafe_allow_html=True)

	run_query = st.button("Get New Exception")
	tag = st.button("Identify Exception Tag")
	if run_query:
		with st.spinner("Retrieving new Exceptions from DB..."):
			df = poll_log(run_query)

		st.write("## Polled Exceptions:")
		st.write(pd.DataFrame(df))

	if tag:
		with st.spinner("Tagging the Exceptions and Updating DB..."):
			df = poll_tag(run_query)

		st.write("Tagged Exceptions:")
		st.write(pd.DataFrame(df))