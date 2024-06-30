from django.contrib import admin
from .models import Category, Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'slug', 'body', 'complete', 'date_add', 'user']
    exclude = ['slug']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'user']
    exclude = ['slug']




