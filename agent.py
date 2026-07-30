import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from llm import get_llm
from tools import query_database
from config import language_instruction


llm = get_llm()


tools = [
    query_database
]


llm_with_tools = llm.bind_tools(tools)



def ask_llm(question):

    # Prepend the language instruction to every prompt
    prefix = language_instruction()

    response = llm_with_tools.invoke(
        f"{prefix}\n\n{question}"
    )


    # AI toolt akar használni

    if response.tool_calls:
        
        tool_call = response.tool_calls[0]


        if tool_call["name"] == "query_database":

            result = query_database.invoke(
                tool_call["args"]
            )


            # Pass the question and the tool result as a single string prompt
            prompt = f"{prefix}\n\nQuestion: {question}\n\nTool result:\n{result}"
            final = llm.invoke(prompt)

            return final.content


    # nincs tool

    return response.content