from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model='gemini-3.6-flash')
import streamlit as st

# while True:
#     query = input("User: ")
#     if query.lower() in ["stop", "bye"]:
#         print("Good Bye!")
#         break

#     res = llm.invoke(query)
#     print("AI:",res.content[0]["text"])

st.title("Ask Buddy - AI QnA Bot")
st.markdown("My QnA chatbot with Langchain and Google Gemini!")

# streamlit run 1_qna_bot.py -> run web server

if "messages" not in st.session_state:
    st.session_state.messages = []  #initalize one list messages = [] in session storage

#show prevoious chat
for message in st.session_state.messages: # message in dict
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)


query = st.chat_input("Ask Anything...?")
if query:
    st.session_state.messages.append({"role":"user" , "content":query}) #list of dict; to prevent previous chat on dashbaord
    st.chat_message("user").markdown(query)
    res = llm.invoke(query)
    st.chat_message("ai").markdown(res.content[0]["text"]) # use markdown to remove speacial char from ai res
    st.session_state.messages.append({"role":"ai" , "content":res.content[0]["text"]})