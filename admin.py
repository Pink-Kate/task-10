from django.contrib import admin
from .models import Quote, Author, Tag

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'death_date', 'quotes_count', 'created_by', 'created_at')
    list_filter = ('birth_date', 'death_date', 'created_at')
    search_fields = ('name', 'bio')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'created_by', 'created_at')
    list_filter = ('author', 'tags', 'created_at')
    search_fields = ('text', 'author__name')
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',) 