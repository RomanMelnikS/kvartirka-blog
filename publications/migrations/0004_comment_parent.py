# Generated by Django 4.0.4 on 2022-04-14 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0003_remove_publication_comments_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nested_comments', to='publications.comment', verbose_name='Комментарий'),
        ),
    ]
