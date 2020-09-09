from django.urls import include, path
import chat.views as c

urlpatterns = [
    path('chatroom/<str:chat_name>/', c.chatroom, name='chat_name'),
]
