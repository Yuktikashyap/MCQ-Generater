from setuptools import setup,find_packages

# find_packages - automatically detect the local packages

setup(
    
    name = 'mecq_gen',
    version='0.0.1',
    description='Creating the projcet : MCQ Generater',
    author='Yukti Kashyap',
    author_email='kashyapyukti12@gmail.com',
    install_requires=['openai','langchain','python-dotenv','PyPDF2'],
    packages=find_packages()
)