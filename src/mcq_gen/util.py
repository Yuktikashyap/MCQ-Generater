
import os
import json
import pandas as pd
import PyPDF2
import traceback


def read_flie(file):
    
    if file.name.endswith('.pdf'):
        try :
           
            pdf_content = PyPDF2.PdfFileReader(file)
            
            text = ''
            
            for page in pdf_content.pages:
                text+=page
            
            return text
        
        except Exception as e :
            raise Exception( 'error in reading the file >> Please try reuploading')
    
    elif file.name.endswith('.txt'):
        
        return file.read().decode('utf-8')
    
    else :
        
        raise Exception(
            
            'Not File desired format : only PDF and txt files are supported '
        )
        
    
def get_table_data(quiz_str):
    
    try : 
    
        quiz_dict = json.loads(quiz_str)
                
        table = []

        for key,value in quiz_dict.items():
                
            print(key," | ",value)
                
            ques = value['question']
            options = ' | '.join( 
                [
                    f"{option} : {options}"
                    for option, options in value['options'].items()
                        
                    ]
                )
            correct = value['correct']
            table.append({'ques':ques,'options' : options, 'correct' : correct})
        
        return table
    
    except Exception as e :
        
        # traceback.print(e)
        
        return False


     
    