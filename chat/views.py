from django.shortcuts import render, redirect
from chat.models import *
from chat.forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth import authenticate, get_user_model, login, logout


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


def login_view(request):
    re_dir = request.GET.get('next')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            if re_dir:
                return redirect(re_dir)
            return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'auth/login.html', {'form': form})
