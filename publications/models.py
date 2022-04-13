from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Publication(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='publications',
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Публикация'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )

    created = models.DateTimeField(
        verbose_name='Дата и время',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
