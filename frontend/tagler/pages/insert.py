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
    st.markdown('<p class="big-font">Create New Log</p>', unsafe_allow_html=True)
    #query = st.text_input("Please provide your query:",value="INSERT INTO...")

    count = 4
    create_header()
        #body()
    body2(int(count))



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
    t = col5.text_input(label=columns[6])

    data = [int(id),ip,q,p,"","",t]

    run_query = st.button("Insert")
    if run_query:
        with st.spinner("Performing insert in db... "):
            results = insert_db(data)
        st.write(results)

def body2(n):
    
    mp = {}

    for i in range(n):
        mp[i] = []
        col1, col2, col3, col4, col5= st.beta_columns((0.4,2,0.6,0.6,0.6))

        id = col1.text_input(value="0",label=columns[0],key=str(i))
        ip = col2.text_input(label=columns[1],key=str(i))
        q =  col3.text_input(label=columns[2],key=str(i))
        p = col4.text_input(label=columns[3],key=str(i))
        t = col5.text_input(label=columns[6],key=str(i))

        mp[i] = [int(id),ip,q,p,"","",t]

    data = mp.values() #[int(id),ip,q,p,"","",t]

    run_query = st.button("Create")
    if run_query:
        with st.spinner("Performing insert in db... "):
            results = insert_db(list(data))
        st.write(results)



