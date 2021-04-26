import streamlit as st
from utils import insert_db, insert_db
from annotated_text import annotated_text


def annotate_answer(answer,context):
    start_idx = context.find(answer)
    end_idx = start_idx+len(answer)
    annotated_text(context[:start_idx],(answer,"ANSWER","#8ef"),context[end_idx:])

def write():      
    st.write("Insert New Exception to DB")
    query = st.text_input("Please provide your query:",value="INSERT INTO...")
    run_query = st.button("Insert")

    if run_query:
        with st.spinner("Performing insert in db... "):
            results = insert_db(query)
        st.write("Result: "+results)



