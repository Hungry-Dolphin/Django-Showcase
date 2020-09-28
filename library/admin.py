from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    ordering = ('-uploaded_at',)
    list_filter = ['clearance', ]
    search_fields = ['title']
    list_display = ['title', 'clearance', 'id', 'uploaded_at']


admin.site.register(Book, BookAdmin)
