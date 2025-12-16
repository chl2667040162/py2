import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sports_competition.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from competitions.models import Competition


def create_users_and_permissions():
    print("Создание пользователей и разрешений...")

    # Создаем группы
    admin_group, created = Group.objects.get_or_create(name='Администраторы')
    organizer_group, created = Group.objects.get_or_create(name='Организаторы')
    participant_group, created = Group.objects.get_or_create(name='Участники')

    # Получаем ContentType для модели Competition
    content_type = ContentType.objects.get_for_model(Competition)

    # Получаем все разрешения
    permissions = Permission.objects.filter(content_type=content_type)

    # Назначаем разрешения группам
    # Администраторы - все права
    for perm in permissions:
        admin_group.permissions.add(perm)

    # Организаторы - могут создавать и редактировать свои соревнования
    organizer_perms = [
        'can_create_competition',
        'can_edit_competition',
        'can_delete_competition',
        'can_register_participant',
    ]
    for perm_name in organizer_perms:
        try:
            perm = Permission.objects.get(codename=perm_name, content_type=content_type)
            organizer_group.permissions.add(perm)
        except Permission.DoesNotExist:
            print(f"Разрешение {perm_name} не найдено")

    # Участники - могут регистрироваться
    participant_perms = ['can_register_participant']
    for perm_name in participant_perms:
        try:
            perm = Permission.objects.get(codename=perm_name, content_type=content_type)
            participant_group.permissions.add(perm)
        except Permission.DoesNotExist:
            print(f"Разрешение {perm_name} не найдено")

    # Создаем тестовых пользователей
    users = [
        {
            'username': 'admin',
            'password': 'admin123',
            'email': 'admin@example.com',
            'first_name': 'Иван',
            'last_name': 'Петров',
            'groups': [admin_group]
        },
        {
            'username': 'organizer1',
            'password': 'org123',
            'email': 'org1@example.com',
            'first_name': 'Мария',
            'last_name': 'Сидорова',
            'groups': [organizer_group]
        },
        {
            'username': 'organizer2',
            'password': 'org456',
            'email': 'org2@example.com',
            'first_name': 'Алексей',
            'last_name': 'Иванов',
            'groups': [organizer_group]
        },
        {
            'username': 'participant1',
            'password': 'part123',
            'email': 'part1@example.com',
            'first_name': 'Сергей',
            'last_name': 'Кузнецов',
            'groups': [participant_group]
        },
        {
            'username': 'participant2',
            'password': 'part456',
            'email': 'part2@example.com',
            'first_name': 'Ольга',
            'last_name': 'Смирнова',
            'groups': [participant_group]
        },
        {
            'username': 'viewer',
            'password': 'view123',
            'email': 'viewer@example.com',
            'first_name': 'Дмитрий',
            'last_name': 'Федоров',
            'groups': []  # Только просмотр
        }
    ]

    for user_data in users:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'is_active': True
            }
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"✓ Создан пользователь: {user.username}")
        else:
            print(f"⚠ Пользователь уже существует: {user.username}")

        # Назначаем группы
        for group in user_data['groups']:
            user.groups.add(group)

    # Создаем тестовые соревнования
    create_test_competitions()

    print("\n" + "=" * 50)
    print("СОЗДАНО:")
    print("=" * 50)
    print("Группы:")
    print("  - Администраторы (все права)")
    print("  - Организаторы (создание, редактирование, удаление, регистрация)")
    print("  - Участники (регистрация)")

    print("\nПользователи:")
    print("  1. admin (admin123) - Администратор")
    print("  2. organizer1 (org123) - Организатор")
    print("  3. organizer2 (org456) - Организатор")
    print("  4. participant1 (part123) - Участник")
    print("  5. participant2 (part456) - Участник")
    print("  6. viewer (view123) - Наблюдатель")

    print("\nТестовые соревнования созданы")


def create_test_competitions():
    """Создание тестовых соревнований"""

    # Получаем пользователей
    try:
        admin_user = User.objects.get(username='admin')
        organizer1 = User.objects.get(username='organizer1')
        organizer2 = User.objects.get(username='organizer2')
    except User.DoesNotExist:
        print("Пользователи не найдены. Сначала создайте пользователей.")
        return

    # Удаляем старые тестовые соревнования (если есть)
    Competition.objects.filter(name__startswith='Тестовое').delete()

    # Создаем тестовые соревнования
    competitions = [
        {
            'name': 'Тестовое соревнование по футболу',
            'description': 'Ежегодный турнир по футболу среди любительских команд',
            'sport_type': 'football',
            'location': 'Центральный стадион',
            'start_date': timezone.now() + timedelta(days=7),
            'end_date': timezone.now() + timedelta(days=9),
            'max_participants': 16,
            'status': 'planned',
            'is_public': True,
            'created_by': organizer1
        },
        {
            'name': 'Баскетбольный кубок города',
            'description': 'Открытый чемпионат города по баскетболу',
            'sport_type': 'basketball',
            'location': 'Спортивный комплекс "Олимп"',
            'start_date': timezone.now() + timedelta(days=14),
            'end_date': timezone.now() + timedelta(days=16),
            'max_participants': 12,
            'status': 'planned',
            'is_public': True,
            'registration_deadline': timezone.now() + timedelta(days=10),
            'created_by': organizer2
        },
        {
            'name': 'Закрытый теннисный турнир',
            'description': 'Турнир для членов клуба',
            'sport_type': 'tennis',
            'location': 'Теннисный клуб "Ас"',
            'start_date': timezone.now() + timedelta(days=21),
            'end_date': timezone.now() + timedelta(days=23),
            'max_participants': 8,
            'status': 'planned',
            'is_public': False,
            'created_by': admin_user
        },
        {
            'name': 'Плавание: 100м вольным стилем',
            'description': 'Соревнования по плаванию на дистанции 100м',
            'sport_type': 'swimming',
            'location': 'Бассейн "Волна"',
            'start_date': timezone.now() - timedelta(days=2),
            'end_date': timezone.now() - timedelta(days=1),
            'max_participants': 20,
            'status': 'completed',
            'current_participants': 18,
            'is_public': True,
            'created_by': organizer1
        },
        {
            'name': 'Чемпионат по шахматам',
            'description': 'Блиц-турнир по шахматам',
            'sport_type': 'chess',
            'location': 'Центр интеллектуальных игр',
            'start_date': timezone.now() + timedelta(hours=2),
            'end_date': timezone.now() + timedelta(hours=6),
            'max_participants': 30,
            'status': 'ongoing',
            'current_participants': 25,
            'is_public': True,
            'created_by': organizer2
        }
    ]

    for comp_data in competitions:
        competition = Competition.objects.create(**comp_data)
        print(f"✓ Создано соревнование: {competition.name}")


if __name__ == '__main__':
    create_users_and_permissions()