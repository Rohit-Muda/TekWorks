import streamlit as st
from mysql import connector

def createTable():
    con=connection()
    cursor=con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS regi(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(220), password varchar(20))") 

def connection():
    try:
        return connector.connect(
            host="localhost",
            user="root",
            password="Mudarohit@2005",
            database="Students_db"
        )
    except connector.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

def login():
    try:
        con=connection()
        cursor=con.cursor()
        
        if con is None:
            return 
        
        email=st.text_input("Enter your Email: ")
        password=st.text_input("Enter your Password")
        
        if st.button("Login"):
            if(email=="" or password==""):
                st.error("Need to fill all details")
                return
            
            cursor.execute("SELECT email FROM regi WHERE email=%s and password=%s ",(email,password))
            record=cursor.fetchone()
            
            if(record==None):
                st.error("Invalid Email or Password")
            else:
                st.success("Login Success")
    
    except connector.Error as e:
        st.error(f"Error logging in: {e}")
    

def register():
    try:
        con=connection()
        cursor=con.cursor()
        
        if con is None:
            return
        
        st.title("Register")
        name=st.text_input("Enter your name: ")
        email=st.text_input("Enter your email :")
        password=st.text_input("Enter your password:")

        if st.button("Register"):

            cursor.execute("SELECT email FROM regi WHERE email=%s and password=%s ",(email,password))
            record=cursor.fetchone()
            st.write(record)
            if(record==None):
                cursor.execute("INSERT INTO regi (name,email,password) VALUES(%s,%s,%s)",(name,email,password))
                con.commit()
                st.success("Registered Successfully")
            else:
                st.error("User already exists. Please Login ")

            


    except connector.Error as e:
        st.error(f"An Error has occured : {e}")

def options():
    
    st.sidebar.title("Select")
    option=st.sidebar.radio("Select Your Operation to perform : " ,("Login","Register"))
    
    if option=="Login":
        login()
    else:
        register()

createTable()
options()