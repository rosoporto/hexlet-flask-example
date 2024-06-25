from faker import Faker
from faker.providers import BaseProvider
import random


def initialize_custom_faker(object_custom, seed):
    """
    Инициализирует объект Faker с кастомным провайдером
    и seed для воспроизводимости результатов.

    :param object_custom: Кастомный провайдер данных.
    :param seed: Seed для генератора случайных чисел.
    :return: Инициализированный объект Faker.
    """
    fake = Faker()
    fake.add_provider(object_custom)
    fake.seed_instance(seed)
    random.seed(seed)
    return fake


class CourseProvider(BaseProvider):
    def course_name(self):
        courses = [
            'Python for Beginners',
            'Advanced JavaScript',
            'Data Science with R',
            'Machine Learning with Python',
            'Web Development with Django',
            'React and Redux',
            'Introduction to SQL',
            'DevOps with Docker',
            'Cybersecurity Basics',
            'Mobile App Development with Flutter'
        ]
        return random.choice(courses)

    def course_duration(self):
        durations = [
            '4 weeks',
            '6 weeks',
            '8 weeks',
            '10 weeks',
            '12 weeks'
        ]
        return random.choice(durations)

    def course_level(self):
        levels = [
            'Beginner',
            'Intermediate',
            'Advanced'
        ]
        return random.choice(levels)

    def course_price(self):
        return round(random.uniform(100.0, 1000.0), 2)


def generate_course(courses_count=10, fake=None):
    """
    Генерирует список курсов программирования.

    :param courses_count: Количество курсов для генерации (по умолчанию 10).
    :param fake: Инициализированный объект Faker.
    :return: Список сгенерированных курсов.
    """
    if courses_count <= 0:
        raise ValueError("Количество курсов должно быть больше нуля")

    if fake is None:
        raise ValueError("Необходимо передать объект Faker")

    courses = []
    for i in range(1, courses_count + 1):
        courses.append({
            'id': i,
            'name': fake.course_name(),
            'duration': fake.course_duration(),
            'level': fake.course_level(),
            'price': fake.course_price()
        })

    return courses


if __name__ == '__main__':
    SEED = 1234
    fake = initialize_custom_faker(CourseProvider, SEED)

    # Генерация курсов с использованием значения по умолчанию
    courses = generate_course(fake=fake)
    for course in courses:
        print(course)

    # Генерация курсов с указанием конкретного количества
    more_courses = generate_course(5, fake)
    for course in more_courses:
        print(course)
