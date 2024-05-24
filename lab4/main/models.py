from django.db import models


# Create your models here.
class Gender(models.Model):
    value = models.CharField("Пол", max_length=30)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Пол"
        verbose_name_plural = "Пол"


class User(models.Model):
    username = models.CharField("Псевдоним", max_length=30)
    name = models.CharField("Имя", max_length=30)
    surname = models.CharField("Фамилия", max_length=30)
    age = models.IntegerField("Возраст")
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    friends = models.ManyToManyField("self")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Group(models.Model):
    name = models.CharField("Название группы", max_length=30)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="receiver")
    text = models.TextField("Текст сообщения", null=True, blank=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class News(models.Model):
    image = models.ImageField(upload_to="main/static/main/img", null=True, blank=True)
    datatime = models.DateTimeField("Дата и время публикации", auto_now_add=True)
    content = models.TextField("Контент новости")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
