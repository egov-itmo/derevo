import os
import sys
import psycopg2
import pandas as pd
from pathlib import Path

filename = "Список растений.txt"
if len(sys.argv) > 1:
    filename = sys.argv[1]
if filename != "--help" and not os.path.isfile(filename):
    print(f"Файл {filename} не найден.")
    filename = "--help"
if filename == "--help":
    print("Скрипт для сверки списка растений (по одному названию на строку) с названиями растений из база данных.")
    print("В начале будут выведены растения, отсутствующие в базе данных, далее - список несостыковок, обнаруженных автоматически.")
    print(f"Использование: python {sys.argv[0]} <путь/до/файла.txt>")
    print("Используемые переменные окружения: DB_HOST,DB_PORT,DB_NAME,DB_USER,DB_PASS")

db_host = os.environ.get("DB_HOST", "localhost")
db_port = os.environ.get("DB_PORT", 5432)
db_name = os.environ.get("DB_NAME", "greendb")
db_user = os.environ.get("DB_USER", "postgres")
db_pass = os.environ.get("DB_PASS", "postgres")

print(f"В качестве входного файла списка растений {filename}")
print(f"Подключение к базе данных будет произведено как postgresql://{db_user}@{db_host}:{db_port}/{db_name}")
print()

get_conn = lambda: psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_pass,
    application_name="test_plants_names",
    connect_timeout=10,
)

exc = {
    "Клен сахаристый": "Клён сахарный"
}

def normalize(s: str) -> str:
    res = s.replace("ё", "е").replace("\xa0", " ").replace("\u0438\u0306", "й").lower().strip()
    return exc[res] if res in exc else res

exc = {normalize(key): normalize(val) for key, val in exc.items()}

plants = set(Path(filename).read_text().split("\n"))
try:
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, name_ru FROM plants")
        df = pd.DataFrame(cur.fetchall(), columns=["id", "name"])
        df["normalized"] = df["name"].apply(normalize)
finally:
    try:
        conn.close()
    except:
        pass

missing = []
rename = {}
for name in plants:
    l = normalize(name)
    if l not in df["normalized"].unique():
        missing.append(name)
        continue
    db_name = df[df["normalized"] == l]["name"].iloc[0]
    if db_name == name:
        continue
    rename[name] = db_name

if len(missing) > 0:
    print("Не найдены в базе данных:")
    for name in missing:
        print(f"{name:<40}")
    print()
if len(rename) > 0:
    print("Несоответствия названий (в документе -> в базе данных):")
    for name, db_name in rename.items():
        print(f"{name:<40} -> {db_name}")