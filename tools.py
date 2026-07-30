from langchain_core.tools import tool
from sql_agent import create_agent

sql_agent = create_agent()


@tool
def query_database(question:str):
    """
    Céges adatbázis lekérdezése.
    Használd, ha vállalati adatra van szükség.
    """

    result = sql_agent.invoke(
        {
            "input": question
        }
    )

    return result["output"]