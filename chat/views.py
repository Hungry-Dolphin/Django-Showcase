from django.shortcuts import render, redirect
from chat.models import *
from chat.forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth import authenticate, login, logout


@login_required
def home(request):
    user = request.user
    all_chats = ChatRoom.objects.all().filter(clearance__lte=user.profile.clearance)
    arguments = {'chat_rooms': all_chats}
    return render(request, 'chat/home.html', arguments)


@login_required
def chatroom(request, chat_name):
    chat_room = get_object_or_404(ChatRoom, id=chat_name)
    user = request.user
    try:
        if int(user.profile.clearance) > chat_room.clearance:
            if request.method == 'POST':
                form = MessageForm(request.POST)
                if form.is_valid():
                    ChatMessage(
                        user=user,
                        send_in=chat_room,
                        content=form.cleaned_data.get('content')
                                ).save()
                    return redirect(request.path_info)
            message_stream = ChatMessage.objects.all().filter(send_in=chat_room)
            arguments = {
                'message_stream': message_stream,
                'form': MessageForm()}
            return render(request, 'chat/chatroom.html', arguments)
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


def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    re_dir = request.GET.get('next')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            Profile(user=user, clearance=1).save()
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)
            if re_dir:
                return redirect(re_dir)
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {'form': form})
