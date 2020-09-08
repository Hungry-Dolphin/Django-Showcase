from django.shortcuts import render
from django.contrib import auth, messages
from chat.models import *
from chat.forms import *


def home(request):
    return render(request, 'HTML/home.html')

