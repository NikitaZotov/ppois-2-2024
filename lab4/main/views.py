from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import JsonResponse
import os
from .models import User, Gender, Group, Message, News


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def get_friends(request, user_id):
    user = User.objects.get(id=user_id)
    friends = user.friends.all()
    friends_list = [{"id": friend.id, "username": friend.username} for friend in friends]
    return JsonResponse({"friends": friends_list})


def get_users_without_friends(request, user_id):
    user = User.objects.get(id=user_id)
    users_without_friends = User.objects.all().exclude(id=user.id).difference(user.friends.all())
    users_without_friends_list = [{"id": user.id, "username": user.username} for user in users_without_friends]
    return JsonResponse({"users_without_friends": users_without_friends_list})


def get_available_groups(request, user_id):
    user = User.objects.get(id=user_id)
    available_groups = Group.objects.all().difference(user.group_set.all())
    available_groups = [{"id": group.id, "name": group.name} for group in available_groups]
    return JsonResponse({"available_groups": available_groups})


def add_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        age = request.POST.get("age")
        gender = Gender.objects.get(id=request.POST.get("gender"))
        if User.objects.filter(username=username).exists():
            error_message = "Пользователь с таким псевдонимом уже существует"
            return render(request, 'main/add_user.html', {'error_message': error_message})
        if 0 > int(age) or int(age) > 170:
            error_message = "Некорректный возраст"
            return render(request, 'main/add_user.html', {'error_message': error_message})

        user = User(username=username, name=name, surname=surname, age=age, gender=gender)
        user.save()
        return redirect('/')

    return render(request, 'main/add_user.html')


def add_news(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.POST.get("user"))
        content = request.POST.get("content")
        image = request.FILES.get("image")

        if image:
            fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, "main/static/main/img/news"))
            filename = fs.save(image.name, image)
            image_url = fs.url(filename)
        else:
            image_url = None

        news = News(user=user, content=content, image=image_url)
        news.save()

        return redirect('/')

    users = User.objects.all()
    data = {'users': users}
    return render(request, 'main/add_news.html', data)


def add_friend(request):
    if request.method == 'POST':
        first_user = User.objects.get(id=request.POST.get("firstUser"))
        second_user = User.objects.get(id=request.POST.get("secondUser"))
        first_user.friends.add(second_user)
        return redirect('/')

    users = User.objects.all()
    data = {'users': users}
    return render(request, 'main/add_friend.html', data)


def add_group(request):
    if request.method == 'POST':
        name = request.POST.get("groupName")
        if Group.objects.filter(name=name).exists():
            error_message = "Группа с таким названием уже существует"
            return render(request, 'main/add_group.html', {'error_message': error_message})
        group = Group(name=name)
        group.save()
        return redirect('/')

    return render(request, 'main/add_group.html')


def add_user_to_group(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.POST.get("user"))
        group = Group.objects.get(id=request.POST.get("group"))
        group.users.add(user)
        return redirect('/')

    users = User.objects.all()
    groups = Group.objects.all()
    data = {'users': users, 'groups': groups}
    return render(request, 'main/add_user_to_group.html', data)


def view_users(request):
    users = User.objects.all()
    data = {'users': users}
    return render(request, 'main/view_users.html', data)


def view_messages(request):
    messages = Message.objects.all()
    data = {'messages': messages}
    return render(request, 'main/view_messages.html', data)


def view_news(request):
    news = News.objects.all()
    data = {'news': news}
    return render(request, 'main/view_news.html', data)


def view_groups(request):
    groups = Group.objects.all()
    data = {'groups': groups}
    return render(request, 'main/view_groups.html', data)


def write_message(request):
    if request.method == 'POST':
        message = Message()
        message.sender = User.objects.get(id=request.POST.get("sender"))
        message.receiver = User.objects.get(id=request.POST.get("receiver"))
        message.text = request.POST.get("text")
        message.save()
        return redirect('/')

    users = User.objects.all()
    data = {"users": users}
    return render(request, 'main/write_message.html', data)


def delete_friend(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.POST.get("user"))
        friend = User.objects.get(id=request.POST.get("friend"))
        user.friends.remove(friend)
        return redirect('/')

    users = User.objects.all()
    data = {"users": users}
    return render(request, 'main/delete_friend.html', data)
