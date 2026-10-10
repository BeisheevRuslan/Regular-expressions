import csv
import re
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# TODO 1: Работа ФИО

for row in contacts_list[1:]:
    fio = " ".join(row[:3]).split()
    while len(fio) < 3:
        fio.append("")
    # Записываем очищенные данные обратно в первые 3 колонки
    row[0] = fio[0]  # Фамилия
    row[1] = fio[1]  # Имя
    row[2] = fio[2]  # Отчество


# TODO 2: Работа с форматами номеров телефонов

def format_phone(phone):
    if not phone:
        return phone

    pattern = r"(\+7|8)[\s\-\.\(\)]*(\d{3})[\s\-\.\(\)]*(\d{3})[\s\-\.\(\)]*(\d{2})[\s\-\.\(\)]*(\d{2})(?:\s*\(?(доб\.?\s*\d+)\)?)*"
    match = re.search(pattern, phone)
    if match:
        # Собираем основной номер
        result = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"

        # Если есть добавочный номер (группа 6), очищаем его от лишних пробелов и скобок
        ext = match.group(6)
        if ext:
            # Заменяем "доб. " или "доб " на стандартизированное "доб."
            ext_clean = re.sub(r"доб\.?\s*", "доб.", ext)
            result += f" {ext_clean}"

        return result

    return phone


for row in contacts_list[1:]:
    row[5] = format_phone(row[5])

# TODO 3: Работа с дублями ФИО

unique_contacts = {}

for row in contacts_list[1:]:
    key = (row[0], row[1])

    if key not in unique_contacts:
        # Если человека еще нет в словаре, добавляем его
        unique_contacts[key] = row
    else:
        # Если человек уже есть, объединяем данные
        existing_row = unique_contacts[key]

        # Проходим по всем колонкам, начиная с 3-й (Отчество и далее)
        for i in range(2, len(row)):
            # Если в сохраненной записи поле пустое, а в новой есть данные - заменяем
            if not existing_row[i] and row[i]:
                existing_row[i] = row[i]

# Собираем итоговый список: сначала заголовок, затем уникальные записи
contacts_list = [contacts_list[0]] + list(unique_contacts.values())

# TODO 4: Запись в файл

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)
