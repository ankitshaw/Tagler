import requests
import streamlit as st
import os
from utils import poll_feedback, load_css, push_feedback, poll_training
import pandas as pd
import time

columns = ["id","exception_input","process","queue","exception_tag","heal_action","entry_time"]

def write():
	load_css("./css/my.css")
	st.markdown('<p class="big-font">Trained Exception</p>', unsafe_allow_html=True)
	
	run_query = st.button("Find")
	#train = st.button("Train")
	if run_query:
		with st.spinner("Retrieving rows to be trained..."):
			df = poll_training(run_query)

		#st.write("## Log for training:")
		st.write(pd.DataFrame(df))

	# if train:
	# 	my_bar = st.progress(0)
	# 	for percent_complete in range(100):
	# 		time.sleep(0.1)
	# 		my_bar.progress(percent_complete + 1)


def send_data(mp):
	data = []
	for key in mp:
		data.append(mp[key])

	print(data)
	resp = push_feedback(data)
	if resp == None:
		st.write("Feedback Successful")