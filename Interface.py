import streamlit as st
st.set_page_config(
    page_title="My app",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 My chemistry app")

st.markdown("## Welcome")
SMILES = st.text_input("Give me a SMILES")
st.write("The current smiles is", SMILES)
pt_group = "D4"
st.write("The point group of your molecule is", pt_group)