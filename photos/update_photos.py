"""
Executable script to update plants photos in the database
"""
import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests
from rich.console import Console

console = Console(emoji=False, highlight=False)

photos_path = "input_photos"  # pylint: disable=invalid-name
if len(sys.argv) > 1:
    photos_path = sys.argv[1]  # pylint: disable=invalid-name
if photos_path != "--help" and not os.path.isdir(photos_path):
    console.print(f"[red]Файл [i]{photos_path}[/i] не найден[/red]. Отображается --help.")
    photos_path = "--help"  # pylint: disable=invalid-name

if photos_path == "--help":
    console.print(
        "Скрипт для загрузки информации о фотографиях в базу данных. Обрабатывает фотографии с названиями фйлов"
        " из [green]заданной папки[/green] как названия растений, сравнивает с названиями, возвращенными back-end'ом"
        " и загружает фотографии для совпавших."
    )
    console.print(f"Использование: python {sys.argv[0]} [green]<путь/до/папки_с_фотографиями>[/green]")
    console.print(
        "Используемые переменные окружения: [b]DB_HOST[/b],[b]DB_PORT[/b],[b]DB_NAME[/b],[b]DB_USER[/b],[b]DB_PASS[/b]"
    )
    sys.exit(0)

plants_endpoint = os.environ.get("PLANTS_ENDPOINT", "http://localhost:8080/api/plants/all")
photo_endpoint = os.environ.get("PHOTO_ENDPOINT", "http://localhost:8080/api/update/plant/{plant_id}/photo")

console.print(f"В качестве папки с фотографиями используется [green]{photos_path}[/green]")
console.print(f"Данные о растениях будут запрошены по адресу [magenta]{plants_endpoint}[/magenta]")
console.print(f"Фотографии будут отправляться по шаблону [cyan]{photo_endpoint}[/cyan]")
print()

# Известные переименования и функция нормализации названий для сравнения

exc = {"Клен сахаристый": "Клён сахарный"}


def normalize(name: str) -> str:
    """
    Normalize name for comparison with other normalized names.
    """
    normalized = name.replace("ё", "е").replace("\xa0", " ").replace("\u0438\u0306", "й").lower().strip()
    return exc.get(normalized, normalized)


exc = {normalize(key): normalize(val) for key, val in exc.items()}

plants = pd.DataFrame(requests.get(plants_endpoint, timeout=60).json()["plants"])
plants["name"] = plants["name_ru"].apply(normalize)

photos_dir = Path(photos_path)
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
    f"Обнаружено {missings.shape[0]} фотографий для которых не нашлось растения в БД."
    f" {plant_names_found.shape[0]} будут обновлены"
)
if missings.shape[0] > 0:
    print("Названия фотографий без растения в БД будут сохранены в файл missings.txt")
    with open("missings.txt", "w", encoding="utf-8") as file:
        print("\n".join(list(missings)), file=file)

errors = 0  # pylint: disable=invalid-name
for plant_id, plant_name in plant_names_found.items():
    photo_name = filenames[plant_name]
    console.print(f"Sending {filenames[plant_name]} image as a photo for plant {plant_name} (id={plant_id})")

    try:
        with (photos_dir / filenames[plant_name]).open("rb") as file:
            res = requests.post(
                photo_endpoint.replace("{plant_id}", str(plant_id)),
                files={"photo_data": file},
                timeout=60,
            )
        if res.status_code != 200:
            console.print(f"Error code {res.status_code}. Output: {res.text}")
            errors += 1
            time.sleep(1)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        console.print(f"[red]Excption occured: {exc!r}[/red]")
        errors += 1
        time.sleep(1)

console.print(
    f"[green]Фотографии обновлены[/green]. Ошибок при загрузке: [red]{errors}[/red],"
    f" всего фотографий отправлено: [cyan]{len(plant_names_found)}[/cyan]"
)
