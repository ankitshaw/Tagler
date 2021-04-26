import streamlit as st

def write():      
    st.title("Tagler")
    st.markdown("""
    <style>
    label {
    display: none;
    }
	.stTextInput>div>div>input {
    color: #4F8BF9;
	}

	.main {
		padding-left:150px;
	}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">Welcome to Tagler Demo</p>', unsafe_allow_html=True)
    st.image("./images/arch.png")
