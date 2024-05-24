from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main import views

urlpatterns = [
    path('', views.index, name="index"),
    path('add_user', views.add_user, name="add_user"),
    path('add_news', views.add_news, name="add_news"),
    path('add_friend', views.add_friend, name="add_friend"),
    path('add_group', views.add_group, name="add_group"),
    path('add_user_to_group', views.add_user_to_group, name="add_user_to_group"),
    path('view_users', views.view_users, name="view_users"),
    path('view_messages', views.view_messages, name="view_messages"),
    path('view_news', views.view_news, name="view_news"),
    path('view_groups', views.view_groups, name="view_groups"),
    path('write_message', views.write_message, name="write_message"),
    path('delete_friend', views.delete_friend, name="delete_friend"),
    path('get_friends/<int:user_id>/', views.get_friends, name="get_friends"),
    path('get_users_without_friends/<int:user_id>/', views.get_users_without_friends, name="get_users_without_friends"),
    path('get_available_groups/<int:user_id>/', views.get_available_groups, name="get_available_groups")
]
