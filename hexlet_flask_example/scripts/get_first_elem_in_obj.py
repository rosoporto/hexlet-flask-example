def get_first_elem(list_object, id):
    return next((elem for elem in list_object if elem['id'] == id), None)


if __name__ == '__main__':
    pass
