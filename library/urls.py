from django.urls import path
import library.views as library

urlpatterns = [
    path('home', library.home, name='library_home'),
    # path('read/<str:current_book>/', l.read_book, name='current_book'),
]
