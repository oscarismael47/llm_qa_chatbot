from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.embeddings.openai import OpenAIEmbeddings
import streamlit as st
import pymilvus_db_helper
import os

# Set OpenAI API credentials from Streamlit secrets
os.environ["OPENAI_API_TYPE"] = st.secrets["OPENAI_TYPE"]
os.environ["OPENAI_API_BASE"] = st.secrets["OPENAI_BASE"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_KEY"]
os.environ["OPENAI_API_VERSION"] = st.secrets["OPENAI_VERSION"]

#
COLLECTION_NAME = st.secrets["DB_COLLECTION_NAME"]  # Set your collection name

# Initialize ChatOpenAI object for interacting with OpenAI's language model
llm = ChatOpenAI(   model_name = st.secrets["OPENAI_MODEL_NAME"],
                    temperature = 0.1,
                    model_kwargs = {"engine":st.secrets["OPENAI_ENGINE"]} )

embeddings = OpenAIEmbeddings(deployment=st.secrets["OPENAI_DEPLOYMENT"])

def generate(template,input_variables,variables_dict,llm_selected):
    """
    Generate a response using a prompt template and variables.

    Args:
    - template (str): The template for generating the prompt.
    - input_variables (list): List of variables to be replaced in the template.
    - variables_dict (dict): Dictionary containing variable values.
    - llm_selected: Selected language model for generating the response.

    Returns:
    - str: The generated response.
    """
    # Create a PromptTemplate object
    prompt_template = PromptTemplate(input_variables=input_variables,template=template)
    # Create an LLMChain object
    chain = LLMChain(llm=llm_selected,prompt=prompt_template)
    response = chain.run(variables_dict)
    return response

def ask(question):
    """
    Generate a response to a user question.

    Args:
    - question (str): The user's question.

    Returns:
    - str: The generated response to the question.
    """
    template = """Answer the question.
                question:{QUESTION}
                response:"""
    input_variables = ["QUESTION"]
    variables_dict = {"QUESTION": question}
    response = generate(template,input_variables,variables_dict,llm)
    return response

def ask_over_files(question,files):
    question_embedding = create_embeddings([question])
    output_fields=["title","text","namespace"]
    filter=f'namespace  in {files}'
    db_response = pymilvus_db_helper.search(question_embedding,output_fields,filter,COLLECTION_NAME)
    titles,texts = db_response[0],db_response[1]
    context = "You are AI assistant. Your role is to answer based on the context(selected documents).Be friendly ".join(texts)
    template = """Answer the following question by using only the context.
                question:{QUESTION}
                context:{CONTEXT}
                response:"""
    input_variables = ["QUESTION","CONTEXT"]
    variables_dict = {"QUESTION": question,"CONTEXT": context}
    response = generate(template,input_variables,variables_dict,llm)
    return response

def create_embeddings(texts):
    embeddings_list = []
    for text in texts:
        res = embeddings.embed_query(text)
        embeddings_list.append(res)
    return embeddings_list

if __name__ == "__main__":
    response = ask_over_files("who is naruto",["dragon_ball.pdf","naruto.pdf"])
    print(response)