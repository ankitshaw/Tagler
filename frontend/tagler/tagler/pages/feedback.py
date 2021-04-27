import requests
import streamlit as st
import os
from utils import poll_feedback, load_css, push_feedback
import pandas as pd
import time

columns = ["id","exception_input","process","queue","exception_tag","heal_action","entry_time"]

def write():
	load_css("./css/my.css")
	st.markdown('<p class="big-font">Send Feedback</p>', unsafe_allow_html=True)
	
	#run_query = st.button("Get Logs for Feedback")
	refresh = st.button("Refresh")

	#if run_query:
	#with st.spinner("Retrieving and Tagging the Exceptions from DB..."):
	df = poll_feedback(True)
	#print(df)
	if len(df[columns[0]]) != 0:
		#st.write(pd.DataFrame(df))
		create_header()
		create_body(df)	
	else:
		st.write("Great! No pending feedbacks!")




def create_header():
	col1, col2, col3, col4, col5, col6, col7 = st.beta_columns((0.4,2,0.6,0.6,1,1,0.6))
	col1.write(columns[0])
	col2.write(columns[1])
	col3.write(columns[2])
	col4.write(columns[3])
	col5.write(columns[4])
	col6.write(columns[5])
	col7.write(columns[6])

def create_body(df):
	size = len(df[columns[0]])
	mp = {}
	for i in range(size):
		mp[df[columns[0]][i]] = {"id":df[columns[0]][i],"tag":df[columns[4]][i],"heal":df[columns[5]][i]}

		col1, col2, col3, col4, col5, col6, col7 = st.beta_columns((0.4,2,0.6,0.6,1,1,0.6))
		col1.write(df[columns[0]][i])
		col2.write(df[columns[1]][i])
		col3.write(df[columns[2]][i])
		col4.write(df[columns[3]][i])
		if df[columns[4]][i] == "Not_Processed":
			tag = col5.selectbox('Exceptions',('Not_Processed','System Exception', 'Business Exception'))#col5.text_input(label="Exception Tag", key=str(df[columns[0]][i]))
		else:
			col5.write(df[columns[4]][i])

		if df[columns[5]][i] == "Not_Processed":
			heal = col6.selectbox('Heal Action',('Not_Processed','Raise Ticket', 'Mail User', 'Restart Process'))#col6.text_input(label="Heal Action", key=str(df[columns[0]][i]))
		else:
			col6.write(df[columns[5]][i])
		col7.write(df[columns[6]][i])

			 
		if heal and tag:
			mp[df[columns[0]][i]]["tag"] = tag
			mp[df[columns[0]][i]]["heal"] = heal

	insert = st.button("Send Feedback")
	if insert:
		r = send_data(mp)

def send_data(mp):
	data = []
	for key in mp:
		data.append(mp[key])

	print(data)
	resp = push_feedback(data)
	if resp == None:
		st.write("Feedback Successful")