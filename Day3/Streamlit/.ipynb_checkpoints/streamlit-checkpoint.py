import streamlit as st

st.title("My First Streamlit App")
st.text_input("Enter your name:")
st.number_input("Enter your age:", min_value=0, max_value=120)
st.radio("Select your gender:", ("Male", "Female", "Other"))
st.selectbox("Select your country:", ("USA", "Canada", "UK", "Australia"))
st.multiselect("Select your hobbies:", ("Reading", "Traveling", "Cooking", "Sports"))
st.slider("Select your satisfaction level:", 0, 10, 5)  
st.date_input("Select your date of birth:")
st.time_input("Select your preferred meeting time:")
st.file_uploader("Upload your profile picture:")
st.color_picker("Pick your favorite color:")
st.progress(50)  # Display a progress bar at 50%
st.checkbox("I agree to the terms and conditions")
st.button("Submit")

# st.success("Form submitted successfully!")
# st.error("There was an error submitting the form.")
# st.warning("Please fill out all required fields.")
# st.info("This is an informational message.")
# st.balloons()
# st.toast("Welcome to the Streamlit app!")
# st.sidebar.title("Sidebar")
# st.sidebar.text_input("Enter your email:")
# st.sidebar.button("Subscribe")
# st.cache_data
# def expensive_computation(x):
#     return x * x
# result = expensive_computation(10)
# st.write("The result of the expensive computation is:", result)
# st.map()
# st.pyplot()
# st.audio()
# st.video()
# st.json({"name": "Rohit", "age": 19, "city": "New York"})
# st.latex(r"E=mc^2")
# st.experimental_rerun()
# st.session_state['counter'] = st.session_state.get('counter', 0) + 1
# st.write("Counter value:", st.session_state['counter'])
# st.form("my_form")
# st.form_submit_button("Submit Form")
# st.experimental_show({"key": "value"})
# st.experimental_get_query_params()

