from django.shortcuts import render
from chat.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import Http404


@login_required
def home(request):
    user = request.user
    all_chats = ChatRoom.objects.all().filter(clearance__lte=user.profile.clearance)
    arguments = {'chat_rooms': all_chats}
    return render(request, 'HTML/home.html', arguments)


@login_required
def chatroom(request, chat_name):
    chat_room = get_object_or_404(ChatRoom, id=chat_name)
    user = request.user
    try:
        if int(user.profile.clearance) > chat_room.clearance:
            message_stream = ChatMessage.objects.all().filter(send_in=chat_room)
            arguments = {'message_stream': message_stream}
            return render(request, 'HTML/chatroom.html', arguments)
        else:
            raise Http404
    except chat_room.DoesNotExist:
        raise Http404
