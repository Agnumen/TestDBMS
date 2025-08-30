from faker import Faker
from app.infrastructure.database.enums import UserRole
fake = Faker()

def generate_test_users(count=10): # где 10 - кол-во сгенерированных пользователей
    """Генерация тестовых пользователей для системы"""
    users = list()
    for i in range(count):
        user = {
            "username": fake.user_name(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "role": fake.enum(UserRole).value,
        }
        users.append(user)
    return users