def validator(user_date):
    errors = {}
    if not user_date['name']:
        errors['name'] = "Field name can't be blank"
    if not user_date['email']:
        errors['email'] = "Field email can't be blank"
    return errors


if __name__ == '__main__':
    data = {'name': 'Alex', 'email': 'qwee@mail.com'}
    result = validator(data)
    print(result)  # Output: Data is valid
