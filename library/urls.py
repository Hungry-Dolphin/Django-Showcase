from django.urls import include, path
import library.views as l

urlpatterns = [
    path('home', l.home, name='library_home'),
    # path('read/<str:current_book>/', l.read_book, name='current_book'),
]
