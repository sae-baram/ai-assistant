from langchain_community.agent_toolkits import create_sql_agent
from database import get_database
from llm import get_llm


def create_agent():

    llm = get_llm()

    db = get_database()


    agent = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="tool-calling",
        verbose=True
    )


    return agent