import json


def read_json_file(file_path):
    """
    Читает данные из JSON-файла и возвращает их в виде списка словарей.

    :param file_path: Путь к JSON-файлу.
    :return: Список словарей с данными.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                # Если файл пустой, возвращаем пустой список
                data = []
        return data
    except FileNotFoundError as e:
        print(f"Файл {file_path} не найден.")
        raise e
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON в файле {file_path}.")
        raise e


def write_json_file(file_path, data):
    """
    Записывает данные в JSON-файл.

    :param file_path: Путь к JSON-файлу.
    :param data: Список словарей с данными для записи.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Данные успешно записаны в файл {file_path}.")
    except IOError as e:
        print(f"Ошибка записи в файл {file_path}: {e}")
        raise RuntimeError(f"Не удалось записать данные в файл {file_path}.") from e


def process_data(data):
    """
    Обрабатывает данные, например, добавляя новый элемент в каждый словарь.

    :param data: Список словарей с данными.
    :return: Обработанный список словарей.
    """
    for item in data:
        item['processed'] = True
    return data


def main(file_path):
    """
    Основная функция для чтения, обработки и записи данных.

    :param file_path: Путь к JSON-файлу.
    """
    try:
        # Чтение данных из файла
        data = read_json_file(file_path)
        print("Данные успешно прочитаны.")

        # Обработка данных
        processed_data = process_data(data)
        print("Данные успешно обработаны.")

        # Запись обработанных данных обратно в файл
        write_json_file(file_path, processed_data)
        print("Данные успешно записаны.")

    except (FileNotFoundError, json.JSONDecodeError, RuntimeError) as e:
        print(f"Обработано исключение: {e}")


if __name__ == '__main__':
    file_path = 'users.json'
    main(file_path)
