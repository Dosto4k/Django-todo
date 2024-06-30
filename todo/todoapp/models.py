from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count, QuerySet
from django.utils.text import slugify
from .services import translate_title_to_slug


def get_categories_and_percentage_of_completed_notes(curr_user) -> QuerySet:
    """
    Функция считает процент выполненных заметок по каждой категории
    и возвращает QuerySet всех категорий с процентом выполненных заметок
    """
    all_note_count = Category.objects.filter(user=curr_user).order_by('name').annotate(
        all_note=Count('notes__id')
    ).values(
        'all_note',
        'name',
        'slug'
    )
    comp_note_count = Category.objects.filter(user=curr_user).order_by('name').filter(
        notes__complete=True,
    ).annotate(
        comp=Count('notes__id')
    ).values(
        'comp',
        'name',
        'slug'
    )
    for cat_all in all_note_count:
        cat_all['percent_complete'] = '0.0%'
        for cat_comp in comp_note_count:
            if cat_all['name'] == cat_comp['name']:
                cat_all['percent_complete'] = f"{round((cat_comp['comp'] / cat_all['all_note']) * 100, 1)}%"
                break
    return all_note_count


def get_percentage_of_completed_and_count_notes(queryset) -> dict:
    """
    Функция считает процент выполненных заметок
    и возвращает процент выполненных заметок,
    кол-во всех заметок и кол-во выполненных заметок
    """
    count_notes = queryset.count()
    count_complete_notes = queryset.filter(complete=True).count()
    percent_complete = f'{round((count_complete_notes / count_notes) * 100, 1)}%'
    return {
        'count_notes': count_notes,
        'count_complete_notes': count_complete_notes,
        'percent_complete': percent_complete
    }


class Note(models.Model):
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='Категория',
    )
    title = models.CharField(
        max_length=50,
        verbose_name='Заголовок',

    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Slug',
    )
    body = models.TextField(
        verbose_name='Текст заметки',
    )
    complete = models.BooleanField(default=False, verbose_name='Завершена')
    date_add = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='Пользователь',
    )

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.slug = slugify(translate_title_to_slug(self.title))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['complete', '-date_add']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'user'],
                name='unique_title_user_note',
                violation_error_message='Поле с таким заголовком уже существует',
            ),
            models.UniqueConstraint(
                fields=['slug', 'user'],
                name='unique_slug_user_note',
                violation_error_message='Поле с таким заголовком уже существует',
            ),
        ]


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Slug',
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='category',
        verbose_name='Пользователь',
    )

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.slug = slugify(translate_title_to_slug(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'], name='unique_name_user_category'),
            models.UniqueConstraint(fields=['slug', 'user'], name='unique_slug_user_category'),
        ]
