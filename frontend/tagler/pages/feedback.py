import streamlit as st
import datetime

def write():
	#make a title for your webapp
	st.title("Manually Tag Exceptions")

	mp = {}
	df = [{"id":110, "text":"exception", "tag":"System"}, {"id":111, "text":"exception2", "tag":"Not Processed"}]
	for x in df:
		field_1 = st.text_input('Enter Tag'+x["text"],key=str(x["id"]))
		if field_1:
			mp = {"id":x["id"],"tag":field_1}

			# st.write("ID="+str(x["id"])+"  |  Log="+x["text"]+"  |  Exception="+x["tag"])
	st.write(mp)

	to_be_deleted = set()

	for i in range(10):
	    delete = st.checkbox(f'delete {i}?', False)
	    if delete:
	        to_be_deleted.add(i)

	st.write(f'to be deleted: {to_be_deleted}')

	#lets try a both a text input and area as well as a date
	field_1 = st.text_input('Your Name') 
	field_2 = st.text_area("Your address")

	start_date = datetime.date(1990, 7, 6)
	date = st.date_input('Your birthday', start_date)

	df = [{"id":110, "text":"exception", "tag":"System"}, {"id":111, "text":"exception2", "tag":"Not Processed"}]
	for x in df:
		if x["tag"] == "":
			st.write("ID="+str(x["id"])+"  |  Log="+x["text"]+"  |  Exception="+x["tag"])
			field_1 = st.text_input('Enter Tag',value="Tag") 
		else:
			st.write("ID="+str(x["id"])+"  |  Log="+x["text"]+"  |  Exception="+x["tag"])
