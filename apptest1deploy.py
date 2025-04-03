import streamlit as st 

st.title("My first forrealskies streamlit app")
st.write("Howdyyyy!")

st.write("trying to make a change and check on github desktop")

#make a click me button 
if st.button("Click me!"):
    st.write("You clicked me!")
    st.balloons()
else:
    st.write("Click the button to see what happens!")

        