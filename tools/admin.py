from django.contrib import admin
from .models import CipherTool, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(CipherTool)
class CipherToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'tool_type', 'order', 'created_at')
    list_filter = ('category', 'tool_type', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_editable = ('category', 'order')
