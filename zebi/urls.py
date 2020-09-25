from django.contrib import admin
from django.urls import include, path
import chat.views as c_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', c_views.home, name='home'),
    path('chat/', include('chat.urls')),

    # Authentication
    path('accounts/login/', c_views.login_view, name='login'),
    path('accounts/logout/', c_views.logout_view, name='logout'),
    path('accounts/register/', c_views.register_view, name='register'),

]
