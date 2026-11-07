
import streamlit as st

st.set_page_config(page_title="Court of AI", page_icon="⚖️")

st.title("⚖️ Court of AI")
st.subheader("The World's Most Unnecessary Courtroom")

st.write("Welcome! Here, anyone can be put on trial.")

accusation = st.text_input(
    "What is the defendant accused of?"
)

if st.button("Start Trial"):
    if accusation:
        st.success("Court is now in session!")
        st.write("The accusation:", accusation)
    else:
        st.warning("Please enter an accusation!")
