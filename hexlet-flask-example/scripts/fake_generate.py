import random
from faker import Faker


def initialize_faker(seed):
    fake = Faker()
    fake.seed_instance(seed)
    random.seed(seed)
    return fake


def generate_users(users_count, fake):
    ids = list(range(1, users_count))
    random.shuffle(ids)

    users = []
    for i in range(users_count - 1):
        users.append({
            'id': ids[i],
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.free_email(),
        })

    return users


def generate_companies(companies_count, fake):
    ids = list(range(companies_count))
    random.shuffle(ids)

    companies = []
    for i in range(companies_count):
        companies.append({
            "id": ids[i],
            "name": fake.company(),
            "phone": fake.phone_number(),
        })

    return companies


def generate_data(count, data_type, fake):
    if data_type == 'domains':
        return [fake.domain_name() for _ in range(count)]
    elif data_type == 'phones':
        return [fake.phone_number() for _ in range(count)]
    else:
        raise ValueError(f"Unknown data type: {data_type}")


if __name__ == '__main__':
    SEED = 1234
    fake = initialize_faker(SEED)
    
    users = generate_users(100, fake)
    companies = generate_companies(100, fake)
    domains = generate_data(10, 'domains', fake)
    phones = generate_data(10, 'phones', fake)
    
    # Пример вывода данных
    print(users[:5])
    print(companies[:5])
    print(domains[:5])
    print(phones[:5])
    