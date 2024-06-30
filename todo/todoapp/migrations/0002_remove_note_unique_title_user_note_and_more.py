# Generated by Django 4.2.13 on 2024-05-20 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='note',
            name='unique_title_user_note',
        ),
        migrations.RemoveConstraint(
            model_name='note',
            name='unique_slug_user_note',
        ),
        migrations.AddConstraint(
            model_name='note',
            constraint=models.UniqueConstraint(fields=('title', 'user'), name='unique_title_user_note', violation_error_message='Поле с таким заголовком уже существует'),
        ),
        migrations.AddConstraint(
            model_name='note',
            constraint=models.UniqueConstraint(fields=('slug', 'user'), name='unique_slug_user_note', violation_error_message='Поле с таким заголовком уже существует'),
        ),
    ]
