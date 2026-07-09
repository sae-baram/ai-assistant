import sqlite3
import os

# Adatbázis fájl neve
DB_NAME = "company.db"

def setup_database():
    # Csatlakozás az SQLite adatbázishoz (ha nem létezik, létrehozza)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Tábla létrehozása: employees (dolgozók)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT NOT NULL,
        department TEXT NOT NULL,
        salary REAL NOT NULL,
        hire_date TEXT NOT NULL
    )
    """)
    
    # 2. Tábla létrehozása: departments (részlegek)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        budget REAL NOT NULL
    )
    """)
    
    # 3. Minta adatok beszúrása (csak ha üres a tábla)
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        employees_data = [
            ("Kovács János", "CEO", "Management", 2500000, "2015-03-15"),
            ("Nagy Anna", "CTO", "IT", 1800000, "2016-07-20"),
            ("Szabó Péter", "Senior Developer", "IT", 1200000, "2018-01-10"),
            ("Tóth Eszter", "HR Manager", "HR", 950000, "2017-05-22"),
            ("Kiss László", "Junior Developer", "IT", 650000, "2022-09-01"),
            ("Varga Katalin", "Accountant", "Finance", 850000, "2019-11-15"),
            ("Molnár Gábor", "Marketing Lead", "Marketing", 1100000, "2020-02-28"),
        ]
        
        cursor.executemany("""
        INSERT INTO employees (name, position, department, salary, hire_date)
        VALUES (?, ?, ?, ?, ?)
        """, employees_data)
        
        departments_data = [
            ("Management", 5000000),
            ("IT", 8000000),
            ("HR", 2000000),
            ("Finance", 3000000),
            ("Marketing", 4000000),
        ]
        
        cursor.executemany("""
        INSERT INTO departments (name, budget)
        VALUES (?, ?)
        """, departments_data)
        
        conn.commit()
        print(f"✅ {len(employees_data)} dolgozó és {len(departments_data)} részleg beszúrva!")
    else:
        print("ℹ️  Az adatbázis már tartalmaz adatokat.")
    
    # 4. Ellenőrzés: írjuk ki a dolgozókat
    cursor.execute("SELECT name, position, salary FROM employees")
    rows = cursor.fetchall()
    
    print("\n📊 Dolgozók az adatbázisban:")
    print("-" * 50)
    for row in rows:
        print(f"{row[0]:20} | {row[1]:20} | {row[2]:,.0f} Ft")
    
    conn.close()
    print(f"\n✅ Adatbázis létrehozva: {os.path.abspath(DB_NAME)}")

if __name__ == "__main__":
    setup_database()