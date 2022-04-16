from django.contrib import admin

from .models import Comment, Publication


class CommentInLine(admin.StackedInline):
    model = Comment


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'created',
        'author'
    )
    search_fields = (
        'text',
    )
    list_filter = (
        'created',
    )
    inlines = [CommentInLine]
    model = Publication


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'publication',
        'text',
        'created',
        'author'
    )
    model = Comment
