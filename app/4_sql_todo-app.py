from dotenv import load_dotenv
load_dotenv()

# We need -> db , llm , create_agent , tools , system_prompt
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
import streamlit as st

# connect db
db = SQLDatabase.from_uri("sqlite:///my_task.db") # sqlite -> prebuild with python we can also connect postgres
db.run("""
    CREATE TABLE IF NOT EXISTS task(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT CHECK(status IN ('pending', 'in_progress', 'completed')) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")
print("DB TABLE Created!") # it creates one file in our app folder that contain all tables -> db viwer externsion

# To create agent we need ->  llm , tools ,memory , sytm prompt
llm = ChatGroq(model='openai/gpt-oss-120b') 
toolkit = SQLDatabaseToolkit(db=db , llm=llm) # toolkit connected to llm and db
tools = toolkit.get_tools()
memory = InMemorySaver()

system_prompt = """
You are a task management assistant that interacts with a SQL database containing a 'tasks' table.

TASK RULES:
1. Limit SELECT queries to 10 results max with ORDER BY created_at DESC
2. After CREATE/UPDATE/DELETE, confirm with SELECT query
3. If the user requests a list of tasks, present the output in a structured table format

CRUD OPERATIONS:
    CREATE: INSERT INTO tasks(title, description, status)
    READ: SELECT * FROM tasks WHERE ... LIMIT 10
    UPDATE: UPDATE tasks SET status=? WHERE id=? OR title=?
    DELETE: DELETE FROM tasks WHERE id=? OR title=?

Table schema: id, title, description, status(pending/in_progress/completed), created_at.
"""
# Create agent
@st.cache_resource # means this function not run ewverytime on page load so that our current session chat remain keep theri
def get_agent():
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=InMemorySaver()
    )
    return agent

agent = get_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []  #initalize one list messages = [] in session storage

for message in st.session_state.messages: # message in dict
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)

st.subheader("TaskBot - Manage Your Tasks")
prompt = st.chat_input("Ask me to manage your tasks...?")

if prompt:
    st.chat_message('user').markdown(prompt) #show user message on dashboard
    st.session_state.messages.append({"role":"user" , "content":prompt})

    with st.chat_message("ai"): # with -> ai message ke refrence me sara kaam hoga 
        with st.spinner("Processing"):
            response= agent.invoke(
                {"messages":[{"role":"user" , "content":prompt}]},
                {"configurable":{"thread_id":"ayy2"}}
            )
            result = response['messages'][-1].content
            st.markdown(result) # ai message
            st.session_state.messages.append({"role":"ai" , "content":result})
 

