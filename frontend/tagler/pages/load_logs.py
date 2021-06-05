import streamlit as st
from utils import insert_db, insert_db, load_css
import pandas as pd

columns = ["id","exception_input","queue","process","exception_tag","heal_action","entry_time"]


def write():
    load_css("./css/my.css")
    st.markdown('<p class="big-font">Load New Log</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file,header=0)
        st.write(dataframe)
        data = getData(dataframe)
        load(data)

def getData(df):
    mp = {}
    for i, row in df.iterrows():
        mp[i] = []
        mp[i] = [int(row["id"]),row["exception_input"],row["queue"],row["process"],"","",row["entry_time"]]

    data = mp.values()
    return data

def load(data):
    run_query = st.button("Create")
    if run_query:
        with st.spinner("Performing insert in db... "):
            results = insert_db(list(data))
            print(results)
            if results == None:
                st.write("Logs created in DB.")





