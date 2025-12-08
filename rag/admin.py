from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['source', 'category', 'author', 'date', 'processed', 'uploaded_at']
    list_filter = ['category', 'processed', 'language']
    search_fields = ['source', 'author', 'category']
