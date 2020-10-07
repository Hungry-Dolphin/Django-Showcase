from django.contrib import admin
from .models import Book, Comments


class BookAdmin(admin.ModelAdmin):
    ordering = ('-uploaded_at',)
    list_filter = ['clearance', ]
    search_fields = ['title']
    list_display = ['title', 'clearance', 'id', 'uploaded_at']


admin.site.register(Book, BookAdmin)


class CommentsAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_filter = ['book', 'user__username']
    search_fields = ['book', 'user__username', 'content', 'id']
    list_display = ['book', 'created_at', 'id', 'bumps', 'content']


admin.site.register(Comments, CommentsAdmin)
