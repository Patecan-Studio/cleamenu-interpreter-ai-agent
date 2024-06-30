from langchain.agents import initialize_agent, AgentType, create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI

from typing import List, Dict, Any

import os

from ai_agent.cleamenu_tools import food_tools

# LLM Initialization
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(max_retries=10, temperature=0,  # type: ignore
                 model_name="gpt-4o")


def initialize_agent_zero_shot(tools: List, is_agent_verbose: bool = True, max_iterations: int = 10, return_thought_process: bool = False):
    memory = ConversationBufferMemory(memory_key="chat_history")

    # Initialize ai_agent
    agent = initialize_agent(
        tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=is_agent_verbose, max_iterations=max_iterations, return_intermediate_steps=return_thought_process, memory=memory)

    return agent


def initialize_agent_with_new_openai_functions(tools: List, is_agent_verbose: bool = True, max_iterations: int = 3, return_thought_process: bool = False):
    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=is_agent_verbose,
                             max_iterations=max_iterations, return_intermediate_steps=return_thought_process)

    return agent


cleamenu_agent = initialize_agent_with_new_openai_functions(
    tools=food_tools
)


#
# while True:
#     request = input(
#         "\n\nRequest: ")
#     result = agent({"input": request})
#     answer = result["output"]
#     print(answer)

#text_query()
