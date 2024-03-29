import os,json
import streamlit as st
import llm_helper,ingest_helper,pdf_helper

#Simple Chat Bot using Streamlit and OpenAI's LLM.
#This application allows users to interact with a chatbot powered by OpenAI's Language Model.
#Users can input messages and receive responses from the chatbot.


## create json file
if not os.path.isfile("state.json"):
    with open("state.json", "w") as file:
        state = {"files":[]}
        json.dump(state,file)

section = st.sidebar.radio("Section",("Add document to DB","Chat", "Document viewer"))

if section == "Add document to DB":
    st.title("Add document to DB")
    
    ## load files
    with open("state.json") as file:
        state = json.load(file)
        files = state["files"]

    uploaded_file  = st.file_uploader("Upload a PDF file", type="pdf",label_visibility="collapsed")

    # Check if file is uploaded
    if uploaded_file is not None:
        current_upload_file = uploaded_file.name
        if current_upload_file not in files:
            ingest_helper.add_document(current_upload_file)
            files.append(current_upload_file) 
        uploaded_file = None
    
    st.multiselect('Current files', files, default=files)

    with open("state.json", "w") as file:
        state = {"files":files}
        json.dump(state,file)

elif section == "Chat":
    st.title("Chat")
    # initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    ## load files
    with open("state.json") as file:
        state = json.load(file)
        files = state["files"]

    st.sidebar.write("Documents:")
    checkboxes = {}
    for file in files:
        checkboxes[file] = st.sidebar.checkbox(file, key=file,value=True)
    selected_files = []
    for key, value in checkboxes.items():
        if value:
            selected_files.append(key)

    #Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(name=message["role"]):
            st.markdown(message["content"])

    #React to user input
    question = st.chat_input("hi")
    if question:
        # Display user message
        with st.chat_message(name="user"):
            st.markdown(question)
        # add user message to chat history
        st.session_state.messages.append({"role":"user", "content":question})
        # Get response from the llm
        response = llm_helper.ask_over_files(question,selected_files)
        # Display chatbot response
        with st.chat_message(name="assistant"):
            st.markdown(response)
        # add user message to chat history
        st.session_state.messages.append({"role":"assistant", "content":response})

elif section == "Document viewer":
    st.title("Document viewer")

    ## load files
    with open("state.json") as file:
        state = json.load(file)
        files = state["files"]

    document = st.sidebar.radio("Documents:",files)
    checkboxes = {}
    for file in files:
        if document == file:
            pdf_helper.show_pdf(file)
    


        
