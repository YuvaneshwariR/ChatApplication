from django.urls import path
from .views import signup, dashboard
from .views import (
    friends_list,
    chat,
    get_messages,
    find_people,
    request_user,
    incoming_requests,
)

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("find_people/", find_people, name="find_people"),
    path("request_user/", request_user, name="request_user"),
    path("incoming_requests/", incoming_requests, name="incoming_requests"),
    path("chat/", chat, name="chat"),
    path("chat/<int:user_id>/", chat, name="chat_with_user"),
    path("get_messages/<int:user_id>/", get_messages, name="get_messages"),
    path("friends/", friends_list, name="friends_list"),
    path("signup/", signup, name="signup"),
]
