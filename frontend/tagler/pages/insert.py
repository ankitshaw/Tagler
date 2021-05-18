import streamlit as st
from utils import insert_db, insert_db, load_css
from annotated_text import annotated_text

columns = ["id","exception_input","queue","process","exception_tag","heal_action","entry_time"]

def annotate_answer(answer,context):
    start_idx = context.find(answer)
    end_idx = start_idx+len(answer)
    annotated_text(context[:start_idx],(answer,"ANSWER","#8ef"),context[end_idx:])

def write():
    load_css("./css/my.css")      
    st.write("Insert New Exception to DB")
    #query = st.text_input("Please provide your query:",value="INSERT INTO...")
    create_header()
    body()



def create_header():
    col1, col2, col3, col4, col5= st.beta_columns((0.4,2,0.6,0.6,0.6))
    col1.write(columns[0])
    col2.write(columns[1])
    col3.write(columns[2])
    col4.write(columns[3])
    col5.write(columns[6])

def body():
    col1, col2, col3, col4, col5= st.beta_columns((0.4,2,0.6,0.6,0.6))
    id = col1.text_input(value="0",label=columns[0])
    ip = col2.text_input(label=columns[1])
    q =  col3.text_input(label=columns[2])
    p = col4.text_input(label=columns[3])
    #tag = col5.selectbox('Exceptions',('Not_Processed','System Exception', 'Business Exception'))#col5.text_input(label="Exception Tag", key=str(df[columns[0]][i]))
    #heal = col6.selectbox('Heal Action',('Not_Processed','Raise Ticket', 'Mail User', 'Restart Process'))#col6.text_input(label="Heal Action", key=str(df[columns[0]][i]))
    t = col5.text_input(label=columns[6])

    data = [int(id),ip,q,p,"","",t]

    run_query = st.button("Insert")
    if run_query:
        with st.spinner("Performing insert in db... "):
            results = insert_db(data)
        st.write(results)



