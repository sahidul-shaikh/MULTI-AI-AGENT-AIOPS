from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

from app.config.settings import settings

def get_response_from_ai_agents(llm_id , query , allow_search ,system_prompt):

    llm = ChatGroq(model=llm_id)

    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    agent = create_react_agent(
        model=llm,
        tools=tools,
    )


    state = {"messages": [
    ("system", system_prompt),   
    ("user", query),             
    ]}

    response = agent.invoke(state)

    messages = response.get("messages")

    ai_messages = [message.content for message in messages if isinstance(message,AIMessage)]

    return ai_messages[-1]

# if __name__ == "__main__":
#     llm_id = "llama-3.3-70b-versatile"
#     query = "Explain the theory of relativity in simple terms."
#     allow_search = True
#     system_prompt = "You are a helpful assistant."

#     response = get_response_from_ai_agents(llm_id, query, allow_search, system_prompt)
#     print("AI Response:", response)





