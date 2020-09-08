from django.urls import include, path
import chat.views as c

urlpatterns = [
    path('<str:chat_name>/', c.chatroom, name='chat_name'),
]
