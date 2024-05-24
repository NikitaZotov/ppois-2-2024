from django.contrib import admin
from .models import User, Gender, Message, Group, News

# Register your models here.
admin.site.register(User)
admin.site.register(Gender)
admin.site.register(Message)
admin.site.register(Group)
admin.site.register(News)
