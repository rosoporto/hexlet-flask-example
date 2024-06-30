def delete_data_by_id(id, data):
    try:
        index = next(
            (inx for inx, elem in enumerate(data) if elem['id'] == id),
            None
        )
        if index is None:
            raise Exception('User with this ID was not found')
        del data[index]
        return True, data
    except Exception as e:
        print(f"Error: {e}")
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
    result = delete_data_by_id(id_to_update, data)
    if result:
        print(f'User with id {id_to_update} has been delete')
