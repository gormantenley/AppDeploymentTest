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


#draw a picture of a cat
st.image("https://images.unsplash.com/photo-1555685812-3c7f8b5e4a2d", caption="A cute cat", use_column_width=True)
st.write("This is a picture of a cat. Isn't it cute?")
st.write("This is a picture of a cat. Isn't it cute?")
st.write("This is a picture of a cat. Isn't it cute?")
st.write("This is a picture of a cat. Isn't it cute?")
st.write("This is a picture of a cat. Isn't it cute?")
