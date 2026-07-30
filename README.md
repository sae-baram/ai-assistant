# AI Assistant Demo

Ez a projekt egy egyszerű, magyar nyelvű AI asszisztens demo, amely FastAPI-alapú webszolgáltatásként fut és LangChain segítségével képes általános kérdésekre válaszolni, illetve adatbázis-lekérdezésekkel céges információkat kinyerni.

## Tartalom

- `main.py` — FastAPI alkalmazás, amely egy `/ask` endpointon keresztül fogad kérdéseket.
- `agent.py` — Üzleti logika: kérdés-útválasztás, Ollama LLM, SQL agent használata.
- `setup_db.py` — SQLite adatbázis létrehozása és mintaadatok feltöltése.
- `company.db` — Például használt SQLite adatbázis (ha már létre van hozva).
- `requirements.txt` — A projekt Python függőségei.
- `_main.py`, `demo_module.py` — egyszerű demonstrációs modul és belépési példa.

## Architektúra

                    Frontend
                        │
                        ▼
                    FastAPI
                        │
                        ▼
                Ollama (LLM)
                        │
                Tool Calling
                        │
        ┌───────────────┴──────────────┐
        │                              │
        ▼                              ▼
  Nincs tool                    query_database()
        │                              │
        ▼                              ▼
  Kész válasz                  Text-to-SQL
                                       │
                         ┌─────────────┴─────────────┐
                         │                           │
                         ▼                           ▼
                  LangChain SQL Agent          vagy Vanna.ai
                         │                           │
                         └─────────────┬─────────────┘
                                       ▼
                                  SQL Database
                                       │
                                       ▼
                                  Eredmény
                                       │
                                       ▼
                              Ollama megfogalmazza
                                       │
                                       ▼
                                   Frontend

## Használt technológiák

- Python 3.11+ ajánlott
- FastAPI
- Uvicorn
- LangChain
- Ollama (helyi LLM szerver)
- SQLite
- SQLAlchemy / langchain-community SQLDatabase
- python-dotenv

## Előkészítés

1. Klónozd a repository-t:

```powershell
cd C:\Users\User\code
git clone <a-repo-url> ai-assistant-demo
cd ai-assistant-demo
```

2. Hozz létre és aktiválj virtuális környezetet:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Telepítsd a függőségeket:

```powershell
pip install -r requirements.txt
```

4. Hozd létre az adatbázist és töltsd fel mintákkal:

```powershell
python setup_db.py
```

Ez létrehozza a `company.db` fájlt és feltölti a `employees` és `departments` táblákat mintaadatokkal.

## Környezet konfiguráció

A projekt `.env` fájlt használ a környezeti változókhoz. Az alapértelmezett értékek a következők:

```env
DATABASE_URI=sqlite:///company.db
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=qwen2.5-coder:3b
```

### Fontos

- Győződj meg róla, hogy az Ollama szerver fut és elérhető a `OLLAMA_BASE_URL` címen.
- A `LLM_MODEL` mezőben add meg az elérhető modell nevét, amely az Ollama telepített modelljei közül választható.

## A szolgáltatás indítása

A FastAPI szervert Uvicorn-nal indíthatod:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Ha minden rendben, a következő URL-en érhető el a szolgáltatás:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs` (Swagger UI)

## API végpontok

### GET `/`

Egyszerű állapotellenőrző végpont.

#### Válasz példa

```json
{
  "status": "OK",
  "message": "Hello World"
}
```

### POST `/ask`

AI kérdés-válasz végpont.

#### Kérelem példa

```json
{
  "question": "Hány dolgozó van az IT részlegben?"
}
```

#### Válasz példa

```json
{
  "question": "Hány dolgozó van az IT részlegben?",
  "answer": "Az IT részlegben 3 dolgozó van."
}
```

## Működés röviden

1. `main.py` fogadja a kérést és továbbítja az `agent.py`-nak.
2. `agent.py` eldönti, hogy a kérdéshez szükséges-e adatbázis-lekérdezés vagy elég a generális LLM válasz.
3. Általános kérdés esetén az Ollama LLM-et használja közvetlenül.
4. Adatbázis-kérdés esetén SQL agentet hoz létre a LangChain `create_sql_agent` segítségével, és a `company.db` adatbázisból húzza az információt.

## Tesztelés / kipróbálás

1. Indítsd el a szervert:

```powershell
uvicorn main:app --reload
```

2. Nyisd meg a Swagger UI-t:

```text
http://127.0.0.1:8000/docs
```

3. Próbálj ki kérdéseket a `/ask` végponttal.

4. Tesztelheted `curl`-lal vagy HTTP klienssel is:

```powershell
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question":"Mennyi az átlagfizetés az IT részlegben?"}'
```

## Tippek és hibakeresés

- Ha az Ollama nem érhető el, ellenőrizd a `OLLAMA_BASE_URL` értékét és indítsd el az Ollama szervert.
- Ha SQL kérdésre nem ad megfelelő választ, futtasd a `setup_db.py`-t újra és győződj meg róla, hogy a `company.db` fájl létezik.
- A projektetlen `requirements.txt` sok csomagot tartalmaz; ha szükséges, csak a ténylegesen használt csomagokat tartsd meg.

## Frontend telepítés

1. Nyisd meg a `frontend` mappát:

```powershell
cd frontend
```

2. Telepítsd a frontend függőségeket:

```powershell
npm install
```

3. Indítsd el a React fejlesztői szervert:

```powershell
npm run dev -- --host 0.0.0.0 --port 5173
```

4. Nyisd meg a böngészőt a `http://localhost:5173` címen.

Ha a backend más porton fut, módosítsd a `frontend/.env` fájlban a `VITE_API_URL` változót.

## Kiterjesztési lehetőségek

- Több adatbázis-tábla és komplexebb lekérdezések támogatása
- Jogosultságkezelés és felhasználói autentikáció hozzáadása
- További végpontok: `POST /questions`, `GET /history`, `GET /employees`
- Frontend alkalmazás készítése az AI asszisztenshez

## Open-WebUI integráció (ajánlott: cserélje le az alap frontendet)

Ez a projekt támogatja, hogy az alap React demo helyett az Open-WebUI frontendet használd. Mivel a környezet nem tud közvetlenül klónozni vagy futtatni hálózati parancsokat, az alábbi lépéseket lokálisan kell végrehajtani.

1. Klónozd az `open-webui`-t a `frontend` mappába és telepítsd:

```bash
./scripts/install_open_webui.sh
```

2. A script létrehoz egy `.env.local` fájlt a `frontend` mappában, amelyben a `VITE_API_BASE_URL` a backendünkre (`http://localhost:8000`) mutat. Ha az open-webui egy másik útvonalat vár, állítsd be `http://localhost:8000/ask`-re.

3. Indítsd el a backendet:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. Indítsd el az open-webui fejlesztői szerverét (a `frontend` mappában):

```bash
cd frontend
npm run dev
```

5. Nyisd meg a UI-t (általában `http://localhost:3000`) és tesztelj kérdéseket; a frontendnek a `VITE_API_BASE_URL` konfiguráció alapján a backendünkhöz kell fordulnia.

Hiba esetén másold ide a terminál kimenetét és segítek hibát keresni és javítani.

## Licence

Ez egy nyílt forráskódú demonstrációs projekt. Tetszőleges licenc alatt használhatod, amennyiben a projekt konfigurációját és függőségeit megfelelően dokumentálod.

