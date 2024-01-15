import os 
import json
import pandas as pd
import traceback
import PyPDF2


from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain, OpenAI
from langchain.chains import SequentialChain


# load environment variables as mentioned in .env

load_dotenv() 

# geting envrionment variable like => os.environ
key = os.getenv('OPENAI_API_KEY')

# making openai object
llm = ChatOpenAI(openai_api_key = key,model_name = 'gpt-3.5-turbo',temperature = 0.6)

# creating Tempalate for PromptTemplate

Template = '''

You are a helpful MCQ Generater and u have been given a text : {text},

You have to generate {number} mcq questions on {subject} and 
level of difficulty should be {level} .

The response should be kept the way it is given in RESPONSE_JSON and use it as guide

### RESPONSE_JSON

{response_json}'''

quiz_prompt = PromptTemplate(
    
    input_variables = ['text','number','subject','level','response_json'],
    template = Template
)


quiz_chain = LLMChain(llm = llm,prompt = quiz_prompt,output_key = 'quiz')


Template2 = '''

Quiz : {quiz} ,

U are an english grammerian and writer 
Task : Ur task is to anyalyse or review the quiz questions in the given quiz 
quiz for the given subject : {subject},

Just give a review about the quiz like how it is and 
If the quiz doesn't fit with the cognitve abiltiy of the student then just change the 
questions in the quiz and difficulty level of the quiz to make it fit
'''

# to check the complexity and review the quiz

complex_prompt = PromptTemplate(
    
    input_variables = ['quiz','subject'],
    template = Template2
)

complex_chain = LLMChain(llm = llm, prompt = complex_prompt, output_key = 'complexity')

final_chain = SequentialChain(chains = [quiz_chain, complex_chain], input_variables = ['text','number','subject','level','response_json'],output_variables = ['quiz','complexity'])