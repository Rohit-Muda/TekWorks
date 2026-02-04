import streamlit as st

st.header("Rohit")
#Header Method
st.header("This is Header method")

# Title Method
st.title("This is Title method")

# Sub header
st.subheader("This is sub-header method")

# Text Mehtod
st.text("This is text method")

# Markdown File - all markdown operations can be done here 
st.markdown("# This is Markdown File")
st.markdown("## This is Markdown File")
st.markdown("**This is Markdown File**")
st.markdown("*This is Markdown File*")
st.markdown("- point \n - point2")
st.markdown("<h3 style='color:red'>Using HTML</h3>",unsafe_allow_html=True)
# st.markdown("- pint 1 <br/>- point 2",unsafe_allow_html=True)
st.markdown("-----------------------------------------")

# Write Method
st.write("Write Method")
st.write([1,2,3])
st.write({"name":"Rohit","age":20})
st.write(123)

# Caption method
st.caption("This is Caption method")

#code method - for showing code blocks
st.code("""
    a=10
    if(a>5):
        print(a)
    print("Hello World")
""",language="python")

#latex method -- Equaitons 
st.latex('''
    a^2+b^2=c^2
''')

# Divider Method for seprating sections
st.divider()

# Button Method for clickable buttons
# Success and Error Methods
# Balloons Method and Snow Method
if st.button("Streamlit Button"):
    st.write("Button Clicked")
    st.success("Sucesss Method")
    st.balloons()
    st.snow()
else:
    st.write("Click Button")
    st.error("Button Method")
st.divider()
    
#text inputs
x=st.text_input(f"Enter Name:")
st.write(f"Name: {x}")

name=st.text_input("Enter your name:")

if name=="":
    st.warning("No Name Entered")
elif not name.isalpha():
    st.warning("Cannot be Alpha Numeric")
else :
    st.write(f"Your Name is : {name}")
st.divider()


#number input
age=st.number_input("Enter age:")
st.write(age)
st.divider()

#text area 
feedback=st.text_area("Enter the Feedback")
st.write(feedback)
st.divider()

#checkbox
if st.checkbox("Agree T&C"):
    st.write("Thank You")
st.divider()

#Radio Button
gender=st.radio("Select gender",("Male","Female"))
st.write(f"gender is {gender}")
st.divider()

#select method-- dropdown select
country=st.selectbox("select your country: ",("India","dubai"))
st.write(f"country:{country}")
st.divider()

# multi select
skill=st.multiselect(
    "select skill:",["Python","Java"]
)
st.write(skill)
st.divider()

#slider
age=st.slider("Select your age: ",0,50,1)
st.write("Your age:",age)

#file upload
file=st.file_uploader("Choose File:")
if file is not None:
    st.write(f"File uploaded : {file.name}")
st.divider()

#form method
with st.form("my_form"):
    name=st.text_input("Enter name:")
    age=st.number_input("Enter age:")
    login=st.form_submit_button("Submit")

if login:
        st.write(f"Name:{name}")
        st.write(f"Age: {age}")
        st.success("Login Done")
st.divider()

#columns Method 
col1,col2,col3=st.columns(3)
with col1:
    st.header("Column1")
    st.write("This is col1")
with col2:
    st.header("Column2")
    st.write("This is col2")
with col3:
    st.header("Column3")
    st.write("THis is col3")
st.divider()

#container method
container=st.container()
container.write("Insie Container")
container.button("Container")

data={
    'Name': ['Anurag', 'Sumit', 'Rohit'],
    'Age': [21, 22, 20],
    'Course': ['B.Tech', 'M.Tech', 'BBA']
}
st.table(data)
st.divider()

#sidebar method
st.sidebar.radio("Operations",("Insert","Delete"))
st.sidebar.checkbox("T&C")
st.sidebar.multiselect(
    "select skill:",["Python","Java"]
)
st.sidebar.button("Submit")


#caching data
@st.cache_data
def load_data():
    return [1,2,3]
data=load_data()
st.write(data)