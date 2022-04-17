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
    created = models.DateTimeField(
        verbose_name='Дата и время добавления',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created']
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
    left = models.IntegerField(
        blank=True,
        null=True
    )
    right = models.IntegerField(
        blank=True,
        null=True
    )
    replays = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        default=None,
        related_name='replays_comment',
        verbose_name='Родительский комментарий',
        blank=True,
        null=True
    )
    level = models.IntegerField(
        blank=True,
        null=True
    )
    created = models.DateTimeField(
        verbose_name='Дата и время добаления',
        auto_now_add=True
    )

    class Meta:
        ordering = ['created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
        self.set_mptt()

    def set_mptt(self, left=1, replays=None, level=1):
        for obj in type(self).objects.filter(replays=replays):
            comment, count = obj, 0
            while comment.replays_comment.exists():
                for replay in comment.replays_comment.all():
                    count += 1
                    comment = replay
            data = {
                'level': level,
                'left': left,
                'right': left + (count * 2) + 1
            }
            type(self).objects.filter(id=obj.id).update(**data)
            left = data['right'] + 1
            self.set_mptt(
                left=data['left'] + 1,
                replays=obj.id,
                level=data['level'] + 1
            )
