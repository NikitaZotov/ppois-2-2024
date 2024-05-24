import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab4.settings')
django.setup()


from main.models import User, Gender, News, Message, Group


def main():
    menu_choose = int(input("1. Добавить пользователя.\n2. Добавить новость.\n3. Добавить друга.\n"
                            "4. Добавить группу.\n5. Добавить пользователя в группу."
                            "\n6. Просмотреть пользователей.\n7. Просмотреть новости.\n"
                            "8. Просмотреть сообщения.\n9. Просмотреть все группы.\n10. Написать сообщение.\n"
                            "11. Удалить друга.\nВведите ваш выбор: "))

    if menu_choose == 1:
        username = input("Введите псевдоним пользователя: ")
        if User.objects.filter(username=username).exists():
            print("Пользователь с таким псевдонимом уже существует")
            return
        name = input("Введите имя пользователя: ")
        surname = input("Введите фамилию пользователя: ")
        age = int(input("Введите возраст пользователя: "))
        if 0 > int(age) or int(age) > 170:
            print("Некорректный возраст")
            return
        gender_id = int(input("Введите номер пола пользователя(1 - мужской/2 - женский): "))
        if not Gender.objects.filter(id=gender_id).exists():
            print("Неверный пол")
            return
        gender = Gender.objects.get(id=gender_id)

        user = User(username=username, name=name, surname=surname, age=age, gender=gender)
        user.save()
        print("Пользователь успешно создан!")

    elif menu_choose == 2:
        username = input("Введите псевдоним пользователя: ")

        if not User.objects.filter(username=username).exists():
            print("Данного пользователя не существует")
            return
        user = User.objects.get(username=username)
        content = input("Введите текст новости: ")

        news = News(content=content, user=user)
        news.save()
        print("Новость успешно добавлена!")

    elif menu_choose == 3:
        user_username = input("Введите псевдоним пользователя: ")
        if not User.objects.filter(username=user_username).exists():
            print("Данного пользователя не существует")
            return
        user = User.objects.get(username=user_username)
        friend_username = input("Введите псевдоним пользователя: ")
        if not User.objects.filter(username=friend_username).exists():
            print("Данного пользователя не существует")
            return
        friend = User.objects.get(username=friend_username)
        if user == friend:
            print("Нельзя добавить в друзья самого себя")
            return
        user.friends.add(friend)
        print("Друг успешно добавлен!")

    elif menu_choose == 4:
        group_name = input("Введите название группы: ")
        if Group.objects.filter(name=group_name).exists():
            print("Группа с таким названием уже существует")
            return
        group = Group(name=group_name)
        group.save()
        print("Группа успешно добавлена!")

    elif menu_choose == 5:
        username = input("Введите псевдоним пользователя: ")
        if not User.objects.filter(username=username).exists():
            print("Данного пользователя не существует")
            return
        user = User.objects.get(username=username)
        group_name = input("Введите название группы: ")
        if not Group.objects.filter(name=group_name).exists():
            print("Данной группы не существует")
            return
        group = Group.objects.get(name=group_name)
        group.users.add(user)
        print("Пользователь успешно добавлен в группу!")

    elif menu_choose == 6:
        os.system("clear")
        users = User.objects.all()
        if len(users) == 0:
            print("Список пользователей пуст")
            return
        for user in users:
            friend_list = [friend.username for friend in user.friends.all()]
            group_list = [group.name for group in user.group_set.all()]
            print("👤Пользователь")
            print(f"Псевдоним пользователя: {user.username}")
            print(f"Имя пользователя: {user.name}")
            print(f"Фамилия пользователя: {user.surname}")
            print(f"Возраст пользователя: {user.age}")
            print(f"Друзья пользователя: {', '.join(friend_list) if len(friend_list) > 0 else 'не имеется'}")
            print(f"Группы пользователя: {', '.join(group_list) if len(group_list) > 0 else 'не имеется'}\n")

    elif menu_choose == 7:
        os.system("clear")
        news = News.objects.all()
        if len(news) == 0:
            print("Список новостей пуст")
            return
        for news_el in news:
            print("📰Новость")
            print(f"Псевдоним пользователя: {news_el.user.username}")
            print(f"Контент новости: {news_el.content}")
            print(f"Картинка: {'✅' if news_el.image else '❌'}\n")

    elif menu_choose == 8:
        os.system("clear")
        messages = Message.objects.all()
        if len(messages) == 0:
            print("Список сообщений пуст")
            return
        for message in messages:
            print("✉️Сообщение")
            print(f"Псевдоним отправителя: {message.sender.username}")
            print(f"Псевдоним получателя: {message.receiver.username}")
            print(f"Текст сообщения: {message.text}\n")

    elif menu_choose == 9:
        os.system("clear")
        groups = Group.objects.all()
        if len(groups) == 0:
            print("Список сообщений пуст")
            return
        for group in groups:
            users_list = [user.username for user in group.users.all()]
            print("👥Группа")
            print(f"Название группы: {group.name}")
            print(f"Участники: {', '.join(users_list) if len(users_list) > 0 else 'не имеется'}\n")

    elif menu_choose == 10:
        sender_username = input("Введите псевдоним отправителя: ")
        if not User.objects.filter(username=sender_username).exists():
            print("Данного пользователя не существует")
            return
        sender = User.objects.get(username=sender_username)
        receiver_username = input("Введите псевдоним получателя: ")
        if not User.objects.filter(username=receiver_username).exists():
            print("Данного пользователя не существует")
            return
        receiver = User.objects.get(username=receiver_username)
        text = input("Введите текст сообщения: ")
        message = Message(sender=sender, receiver=receiver, text=text)
        message.save()
        print("Сообщение успешно отправлено!")

    elif menu_choose == 11:
        user_username = input("Введите псевдоним пользователя: ")
        if not User.objects.filter(username=user_username).exists():
            print("Данного пользователя не существует")
            return
        user = User.objects.get(username=user_username)
        friend_username = input("Введите псевдоним друга: ")
        if not user.friends.filter(username=friend_username).exists():
            print("Данного пользователя нету в друзьях")
            return
        friend = User.objects.get(username=friend_username)
        user.friends.remove(friend)
        print("Друг успешно удален!")


if __name__ == "__main__":
    main()
