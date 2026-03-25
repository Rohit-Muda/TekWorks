import streamlit as st
from Task import predict_delays

st.title("ML prediction for flight delays")
st.write("This is a simple Streamlit app to predict flight delays using a machine learning model.")

#i have an file called Task.py that predicts the flight delays using a machine learning model. i want to add a simple UI using streamlit to that prediction that shows visualzation and predicted values

st.file_uploader("Upload your flight data", type=["csv"])
if st.button("Predict Delays"):
    # Here you would call your Task.py prediction function and pass the uploaded file
    # call Task.py
    predictions = Task.predict_delays(uploaded_file)
    st.write("Predictions would be displayed here after processing the uploaded file.")