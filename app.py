import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import CTransformers


from langchain_community.document_loaders import PyPDFDirectoryLoader,DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Pinecone
from langchain.memory import ConversationBufferMemory

import os
# from dotenv import load_dotenv
import os
import timeit
import sys
# load_dotenv()




# Add title to streamlit application on browser
st.set_page_config(page_title=" Store",
                    page_icon='🤖',
                    layout='centered',
                    initial_sidebar_state='collapsed')


#Create a Side bar
with st.sidebar:
    st.title("Chatbot")
    st.header("Settings")

# Clear the Chat Messages
def clear_chat_history():
    st.session_state.messages=[{"role":"assistant", "content": "Hi I'm Tekinni, Welcome to SmartCity Ecommerce Store assistant, how may I assist you today?"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


if "messages" not in st.session_state.keys():
    st.session_state.messages=[{"role": "assistant", "content":"Hi I'm Tekinni, Welcome to SmartCity Ecommerce Store website, how may help you today?"}]

# Display the chat assistant default message

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        

# get user provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content":prompt})
    with st.chat_message("user"):
        st.write(prompt)
        
# # Create a Function to generate the Llama 2 Response
def generate_llama2_response(prompt_input):
    default_system_prompt="You are a helpful assistant to this store. Your role is to give authetic and helpful response. If you do not know , say you don't know. If the user greets you with a  simple 'hello', 'hi','hey',or similar grretings, regardless of the number of letters repeated or the informality of the greeting, respond with a friendly greeting in return. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for data in st.session_state.messages:
        # print("Data:", data)
        if data["role"]=="user":
            default_system_prompt+="User: " + data["content"] + "\n\n"
        else:
            default_system_prompt+="Assistant" + data["content"] + "\n\n"
            
    llm=CTransformers(model='./model/model',
                      model_type='llama',
                      config={'max_new_tokens':2048,
                              'temperature':0.01,
                              'context_length':4096})
    
    # Prompt Template
    
    template = """Use the following pieces of information to answer the user's question.

        Default_system_prompt: {default_system_prompt}
        Prompt_input: {prompt_input}

        Only return the authentic answer below and nothing else.
        Authetic answer:
        """
    
    prompt=PromptTemplate(input_variables=["default_system_prompt", "prompt_input"],
                          template=template)
    print("I got past *your prompt*")

    ## Generate the ressponse from the LLama 2 model
    response=llm(prompt.format(default_system_prompt=default_system_prompt,prompt_input=prompt_input))
    
    print("I can attest that  *your prompt* went into your train eco assistant!!!")

    print(response)
    return response


# get the assistant to respond  after user input using chat_input
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            response=generate_llama2_response(prompt)
            placeholder=st.empty()
            full_response=''
            for item in response:
                full_response+=item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)

    message= {"role":"assistant", "content":full_response}
    st.session_state.messages.append(message)     
     
     
     
 