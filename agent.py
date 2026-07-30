import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from llm import get_llm
from tools import query_database


llm = get_llm()


tools = [
    query_database
]


llm_with_tools = llm.bind_tools(tools)



def ask(question):

    response = llm_with_tools.invoke(
        question
    )


    # AI toolt akar használni

    if response.tool_calls:

        tool_call = response.tool_calls[0]


        if tool_call["name"] == "query_database":

            result = query_database.invoke(
                tool_call["args"]
            )


            final = llm.invoke(
                [
                    {
                        "role":"user",
                        "content":question
                    },
                    {
                        "role":"tool",
                        "content":result
                    }
                ]
            )


            return final.content


    # nincs tool

    return response.content