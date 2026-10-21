from dotenv import load_dotenv
load_dotenv()

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

llm = ChatGroq(model='openai/gpt-oss-120b') 
search = GoogleSerperAPIWrapper()

agent = create_agent(
    model=llm,
    tools=[search.run],
    system_prompt="You are a google search agent , can search any question on google",
    checkpointer=MemorySaver()
)

while True:
    query = input("Enter Query: ")
    if query in ["bye","stop"]:
        print("Good Bye!")
        break

    response = agent.invoke(
        {"messages":[{"role":"user" , "content":query}]},
        {"configurable":{"thread_id":"ayy1"}} # Now memory stored with this threaid ayy1
        )
    print("AI Answer:",response['messages'][-1].content)

# Enter Query: WHo is the PM of India - One word answer
# AI Answer: Modi
# Enter Query: What is his age ?
# AI Answer: 76 years old.
# Enter Query: Really?
# AI Answer: Narendra Modi was born on 17 September 1950, so as of 2026 he is 76 years old【source】.
# Enter Query: 
