from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Note
from string import ascii_lowercase


def only_ru_or_eng_letter_validator(arr):
    """
    Проверяет чтобы в заголовке заметки или названии категории были только Русские или Английские буквы
    """
    list_char = ascii_lowercase + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    for char in arr:
        if char.isalpha() and char.lower() not in list_char:
            raise ValidationError(
                message="""
                В названии категории и заголовке заметки могут присутствовать только Русские и 
                Английские символы, цифры и знаки препинания
                """,
                params={'Символ': char}
            )


def count_ru_and_eng_char(arr):
    """
    Проверяет есть ли в названии или заголовке хотя бы одна Русская или Английская буква
    """
    list_char = ascii_lowercase + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    count_chars = 0
    for char in arr:
        if char.isalpha() and char.lower() in list_char:
            count_chars += 1
    if count_chars == 0:
        raise ValidationError(
            message="""
            В названии категории и заголовке заметки должен присутствовать 
            хотя бы один Русский или Английский символ
            """
        )


class UpdateNoteForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(
            Category.objects.filter(user=user),
            label='Категория',
            widget=forms.Select(
                attrs={
                    'class': 'category-field',
                    'onmousedown': "if(this.options.length>10){this.size=10;}",
                    'onchange': 'this.size=0;',
                    'onblur': "this.size=0;",
                }
            ),
        )

    title = forms.CharField(
        max_length=50,
        label='Заголовок',
        widget=forms.TextInput(
            attrs={
                'class': 'title-field'
            }
        ),
        validators=[only_ru_or_eng_letter_validator, count_ru_and_eng_char]
    )
    body = forms.CharField(
        label='Содержание',
        widget=forms.Textarea(
            attrs={
                'class': 'body-field'
            }
        ),
    )

    class Meta:
        model = Note
        fields = ['title', 'body', 'category']


class CreateNoteForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(
            Category.objects.filter(user=user),
            label='Категория',
            widget=forms.Select(
                attrs={
                    'class': 'category-field',
                    'onmousedown': "if(this.options.length>10){this.size=10;}",
                    'onchange': 'this.size=0;',
                    'onblur': "this.size=0;",
                }
            ),
        )

    title = forms.CharField(
        max_length=50,
        label='Заголовок',
        widget=forms.TextInput(
            attrs={
                'class': 'title-field'
            }
        ),
        validators=[only_ru_or_eng_letter_validator, count_ru_and_eng_char]
    )
    body = forms.CharField(
        label='Содержание',
        widget=forms.Textarea(
            attrs={
                'class': 'body-field'
            }
        ),
    )

    class Meta:
        model = Note
        fields = ['title', 'body', 'category', 'user']


class CreateCategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        label='Название',
        widget=forms.TextInput(
            attrs={
                'class': 'name-field'
            }
        ),
        validators=[only_ru_or_eng_letter_validator, count_ru_and_eng_char]
    )

    class Meta:
        model = Category
        fields = ['name', 'user']
