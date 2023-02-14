import os
import pathlib
import sys

import pandas as pd
import psycopg2

photos_path = "plants_photos"
if len(sys.argv) > 1:
    photos_path = sys.argv[1]
if photos_path != "--help" and not os.path.isdir(photos_path):
    print(f"Файл {photos_path} не найден")
    photos_path = "--help"
if photos_path == "--help":
    print(
        "Скрипт для загрузки информации о фотографиях в базу данных. Обрабатывает фотографии с названиями фйлов"
        " как названия растений, переименовывает их в id растений и отмечает в базе, что данное растение имеет фотографию"
    )
    print(f"Использование: python {sys.argv[0]} <путь/до/папки_с_фотографиями>")
    print("Используемые переменные окружения: DB_HOST,DB_PORT,DB_NAME,DB_USER,DB_PASS")

db_host = os.environ.get("DB_HOST", "localhost")
db_port = os.environ.get("DB_PORT", 5432)
db_name = os.environ.get("DB_NAME", "greendb")
db_user = os.environ.get("DB_USER", "postgres")
db_pass = os.environ.get("DB_PASS", "postgres")

print(f"В качестве папки с фотографиями используется {photos_path}")
print(f"Подключение к базе данных будет произведено как postgresql://{db_user}@{db_host}:{db_port}/{db_name}")
print()

get_conn = lambda: psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_pass,
    application_name="update_plants_photos",
    connect_timeout=10,
)

# Известные переименования и функция нормализации названий для сравнения

exc = {"Клен сахаристый": "Клён сахарный"}


def normalize(s: str) -> str:
    res = s.replace("ё", "е").replace("\xa0", " ").replace("\u0438\u0306", "й").lower().strip()
    return exc[res] if res in exc else res


exc = {normalize(key): normalize(val) for key, val in exc.items()}

try:
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT name_ru as name, id FROM plants")
        plants = (
            pd.DataFrame(cur.fetchall(), columns=[d.name for d in cur.description]).set_index("id").sort_values("name")
        )
finally:
    conn.close()
plants["name"] = plants["name"].apply(normalize)

photos_dir = pathlib.Path(photos_path)
plant_names = []
filenames = {}
for file in photos_dir.iterdir():
    if not file.name.endswith((".jpg", ".jpeg")):
        continue
    if file.name != normalize(file.name):
        file = file.rename(photos_dir / normalize(file.name))
    plant_name = file.name[: file.name.rfind(".")]
    plant_names.append(plant_name)
    filenames[plant_name] = file.name

plant_names = pd.Series(sorted(plant_names), name="plant_name")

plant_names_found = plant_names[pd.Series([plant_name in plants["name"].unique() for plant_name in plant_names])]
plant_names_found.index = [plants["name"][plants["name"] == val].index[0] for val in plant_names_found]

missings = plant_names[~plant_names.isin(plant_names_found)]
print(
    f"Обнаружено {missings.shape[0]} фотографий для которых не нашлось растения в БД. {plant_names_found.shape[0]} будут обновлены"
)
if missings.shape[0] > 0:
    print("Названия фотографий без растения в БД будут сохранены в файл missings.txt")
    with open("missings.txt", "w", encoding="utf-8") as file:
        print("\n".join(list(missings)), file=file)

try:
    with get_conn() as conn, conn.cursor() as cur:
        for plant_id, plant_name in plant_names_found.items():
            photo_name = filenames[plant_name]
            new_photo_name = f"{plant_id}{photo_name[photo_name.rfind('.') :]}"
            cur.execute("UPDATE plants SET photo_name = %s WHERE id = %s", (new_photo_name, plant_id))
            (photos_dir / photo_name).rename(photos_dir / new_photo_name)
finally:
    try:
        conn.close()
    except:
        pass
