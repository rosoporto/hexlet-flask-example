def update_data_by_id(id, data, new_data):
    for item in data:
        if item['id'] == id:
            # Variant #1
            # new_data = {'id': id} | new_data
            # item.update(new_data)

            # Variant #2
            item['name'] = new_data['name']
            item['email'] = new_data['email']

            return True, data
    return False


if __name__ == '__main__':
    # Исходный массив
    data = [
        {'id': 1, 'name': 'Ara', 'email': 'Ara@yandex.ru'},
        {'id': 2, 'name': 'Bara', 'email': 'Bara@vov.ru'},
        {'id': 3, 'name': 'Cara', 'email': 'Cara@vov.ru'},
        {'id': 4, 'name': 'Dara', 'email': 'Dara@gmail.ru'},
        {'id': 5, 'name': 'Era', 'email': 'Era@mail.ru'},
        {'id': 6, 'name': 'Fara', 'email': 'Fara@brama.com'}
    ]
    # Пример обновления
    id_to_update = 3
    new_data = {'name': 'Zara', 'email': 'Zara@example.com'}

    updated_item = update_data_by_id(id_to_update, data, new_data)

    if updated_item:
        print("Данные обновлены:", updated_item)
    else:
        print("Элемент с данным id не найден")

    # Вывод обновленного массива
    print("Обновленный массив:", data)
