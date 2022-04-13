from django.contrib import admin

from .models import Comment, Publication


class CommentInLine(admin.StackedInline):
    model = Comment


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author'
    )
    search_fields = (
        'text',
    )
    list_filter = (
        'pub_date',
    )
    inlines = [CommentInLine]
    model = Publication
