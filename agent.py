import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

# Környezeti változók betöltése
load_dotenv()

def get_agent(llm, db):
    """
    Létrehozza a SQL Agent-et (csak akkor hívódik meg, ha adatbázis kell).
    """
    agent = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="zero-shot-react-description",
        extra_instructions="""
        Te egy profi SQL szakértő vagy. Kövesd szigorúan ezeket a lépéseket:
        1. Értsd meg a felhasználó kérdését.
        2. Generálj egy SQL lekérdezést.
        3. FUTTASD LE a lekérdezést az eszközzel (sql_db_query).
        4. A kapott EREDMÉNYT HASZNÁLD FEL a végső válasz megfogalmazásához.
        
        FONTOS: SOHA ne állj meg annál, hogy "le kell futtatni a lekérdezést". 
        Mindig add meg a tényleges számot vagy adatot magyar nyelven a végén!
        """,
        verbose=True,
    )
    return agent


def route_question(question: str, llm) -> str:
    """
    Eldönti, hogy a kérdéshez kell-e adatbázis, vagy általános tudás.
    """
    router_prompt = PromptTemplate.from_template("""
    Elemezd a következő felhasználói kérdést.
    Döntsd el, hogy a válaszadáshoz szükség van-e egy vállalati adatbázis (pl. dolgozók, fizetések, részlegek) lekérdezésére, vagy ez egy általános, ténykereső/programozási kérdés.

    Válaszod CSAK ez a két szó egyik legyen (semmi más szöveg, csak a szó):
    - DATABASE (ha adatbázis lekérdezés kell)
    - GENERAL (ha általános tudás, magyarázat, vagy nem az adatbázisra vonatkozik)

    Kérdés: {question}
    Kategória:
    """)
    
    # A prompt és az LLM összekapcsolása (LangChain Chain)
    chain = router_prompt | llm
    response = chain.invoke({"question": question}).content.strip().upper()
    
    # Biztonsági háló: ha a modell valami mást ír, alapértelmezetten GENERAL
    return "DATABASE" if "DATABASE" in response else "GENERAL"


def ask_question(question: str) -> str:
    """
    Fő függvény: Először útválaszt, majd a megfelelő helyre irányítja a kérést.
    """
    # 1. Modell inicializálása (ez kell a routernek ÉS az agentnek is)
    model_name = os.getenv("LLM_MODEL", "qwen2.5-coder:7b")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    llm = ChatOllama(
        model=model_name,
        base_url=base_url,
        temperature=0,
    )

    # 2. LÉPÉS: Útválasztás (Routing)
    intent = route_question(question, llm)
    
    if intent == "GENERAL":
        # 3a. LÉPÉS: Általános válasz (nincs adatbázis kapcsolat)
        print(f"\n[ROUTER] Általános kérdés észlelve. Adatbázis NEM szükséges.\n")
        general_prompt = f"Válaszolj tömören, érthetően és segítőkészen a következő kérdésre magyar nyelven: {question}"
        response = llm.invoke(general_prompt)
        return response.content
        
    else:
        # 3b. LÉPÉS: Adatbázis válasz (SQL Agent meghívása)
        print(f"\n[ROUTER] Adatbázis lekérdezés szükséges. SQL Agent indítása...\n")
        db_uri = os.getenv("DATABASE_URI", "sqlite:///company.db")
        db = SQLDatabase.from_uri(db_uri)
        
        agent = get_agent(llm, db)
        response = agent.invoke({"input": question})
        return response["output"]