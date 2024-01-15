import os 
import json
import pandas as pd
import traceback
import PyPDF2
import streamlit as st
from src.mcq_gen.util import read_flie, get_table_data
from src.mcq_gen.MCQGenerator import final_chain
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

from langchain.callbacks import get_openai_callback
from langchain.chains import SequentialChain    


st.set_page_config(page_title = "MCQ Generater", page_icon='https://archive.org/download/github.com-langchain-ai-langchain_-_2023-09-20_11-56-54/cover.jpg')

st.title("🤖 MCQ Generater 🦜🔗")

st.image('https://miro.medium.com/v2/resize:fit:1400/1*odEY2uy37q-GTb8-u7_j8Q.png')


with open('D:\Project\Response.json','r') as f:
    RESPONSE_JSON = json.load(f)


# taking inputs

with st.form("user inputs") :
    
    # file upload
    
    uploaded_file = st.file_uploader('upload PDF or txt File 👨‍🚀')
    
    # number of mcq
    
    num_mcq = st.number_input('no. of mcq 🎯',min_value = 2,max_value = 70)
    
    # subject
    
    subject = st.text_input('subject 📚',max_chars = 50)
    
    level = st.text_input('level of hardness 👩🏻‍💻', max_chars = 25, placeholder = 'simple')
    
    submit = st.form_submit_button("Create")
    
if uploaded_file and submit is not None and subject and level and num_mcq : 
    
    with st.spinner('loading...😎') :
    
        try : 
            
            # calling the read_file func in utils and it will the uploaded doc text
            text = read_flie(uploaded_file)
            with get_openai_callback() as cb :
            
                response = final_chain(
                    {
                        'text' : text,
                        'number' : num_mcq,
                        'subject' : subject,
                        'level' : level,
                        'response_json' : json.dumps(RESPONSE_JSON)
                    }
                ) 
        except Exception as e :
            raise Exception('Error coming : Try again later 🕵️‍♀️')
        
        else :
            
            # print(response)
            if isinstance(response,dict):
                # make the DataFrame
                
                quiz = response.get('quiz',None)
                
                if quiz is not None :
                    
                    table_data = get_table_data(quiz)
                    
                    if table_data is not None :
                    
                        df = pd.DataFrame(table_data)
                        df.index = df.index+1 # index in the table/df start from 1 and not from 0 
                        st.table(df)
                        
                        
                        # displaying review as well
                        
                        st.header('Review 🧙🏽')
                        st.text_area(label = ' ',value=response['complexity'])
                    
                    else :
                        st.error("Sorry : There is an Error in Table Data 🕵️‍♀️")
                        
                else :
                    
                    st.error("Sorry : Error in Quiz 🕵️‍♀️")
            
            else :
                
                st.write(response)
                
        
      
    
        
        
        
        
        


