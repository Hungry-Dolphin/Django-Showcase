from django.shortcuts import render
from django.contrib import auth, messages


def login(request, invalid):
    # TODO make a login function for users
    if invalid:
        messages.info(request, 'Username or password incorrect', extra_tags="Error")
