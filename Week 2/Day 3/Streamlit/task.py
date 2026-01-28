import streamlit as st
from mysql import connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def connection():
    try:
        return connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
    except connector.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

def read_data():
    try:
        con=connection()
        cursor=con.cursor()
        
        if con is None:
            return 
        
        st.title("Read Data")
        cursor.execute("SELECT * FROM Students")
        
        records=cursor.fetchall()
        df=pd.DataFrame(records,columns=["ID","NAME","AGE"])
        st.write(df)
    
    except connector.Error as e:
        print("Error reading data from database", e)
    

def insert_data():
    try:
        con=connection()
        cursor=con.cursor()
        
        if con is None:
            return
        st.title("Insert Data")
        id=st.number_input("Enter your ID : ")
        name=st.text_input("Enter your Name :")
        age=st.number_input("Enter your Age:")
    
        if st.button("Submit"):
            cursor.execute("INSERT INTO Students VALUES(%s,%s,%s)",(id,name,age))
            con.commit()
            st.success("Data Inserted Successfully")

    except connector.Error as e:
        st.error(f"An Error has occured : {e}")
    

def update_data():
    try:
        con=connection()
        cursor=con.cursor()
        
        if con is None:
            return
        st.title("Update Data")
        id=st.number_input("Enter your Curret ID: ")
        
        st.write("Enter New Values of Data to Update")
        uid=st.number_input("Enter your new ID or OLD Id : ")
        name=st.text_input("Enter your Name : ")
        age=st.number_input("Enter your Age : ")
        
        if st.button("Submit"):
            cursor.execute("UPDATE Students SET id=%s, name=%s, age=%s where id=%s",(uid,name,age,id))
            con.commit()
            if cursor.rowcount == 0:
                st.warning("No record found with this ID")
            else:
                st.success("Data Updated Successfully")
        
    except connector.Error as e:
        st.error(f"An Error has occured : {e}")
      

def delete_data():
    try:
        con=connection()
        cursor=con.cursor()
        
        if con is None:
            return
        st.title("Delete Data")
        id=int(st.number_input("Enter your ID you want to delete: "))
        
        if st.button("Submit"):
            cursor.execute("DELETE FROM Students WHERE id=%s",(id,))
            con.commit()
            if cursor.rowcount == 0:
                st.warning("No record found with this ID")
            else:
                st.success("Data Deleted Successfully")
        
    except connector.Error as e:
        st.error(f"An Error has occured : {e}")
    


def options():
    
    st.sidebar.title("CURD Operations")
    option=st.sidebar.radio("Select Your Operation to perform : " ,("Read","Insert","Update","Delete"))
    
    if option=="Insert":
        insert_data()
    elif option=="Read":
        read_data()
    elif option=="Update":
        update_data()
    else:
        delete_data()

options()



