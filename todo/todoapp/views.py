from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .models import Note, Category, get_categories_and_percentage_of_completed_notes, \
    get_percentage_of_completed_and_count_notes
from .forms import UpdateNoteForm, CreateNoteForm, CreateCategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin


class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = 'todoapp/CategoryList.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return get_categories_and_percentage_of_completed_notes(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class NotesOfCategory(LoginRequiredMixin, generic.ListView):
    model = Note
    template_name = 'todoapp/NotesList.html'
    context_object_name = 'notes'

    def post(self, request, **kwargs):
        note = get_object_or_404(
            Note,
            slug=request.POST['slug'],
            user=request.user
        )
        if note.complete:
            note.complete = False
        else:
            note.complete = True
        note.save()
        return redirect(reverse_lazy('todo:notes_of_category', kwargs={'category_slug': kwargs['category_slug']}))

    def get_queryset(self):
        if self.kwargs['category_slug'] == 'all':
            return Note.objects.select_related('category').filter(user=self.request.user)
        else:
            return Note.objects.select_related('category').filter(
                category__slug=self.kwargs['category_slug'],
                user=self.request.user
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_url'] = self.kwargs['category_slug']
        if self.kwargs['category_slug'] == 'all':
            context['category'] = 'Все категории'
        else:
            context['category'] = get_object_or_404(
                Category,
                slug=self.kwargs['category_slug'],
                user=self.request.user
            ).name
        context['title'] = context['category']
        if not context['notes']:
            return context
        count_and_percent_notes = get_percentage_of_completed_and_count_notes(context['notes'])
        context['complete'] = count_and_percent_notes['count_complete_notes']
        context['all_notes'] = count_and_percent_notes['count_notes']
        context['percent_complete'] = count_and_percent_notes['percent_complete']
        return context


class DeleteNote(LoginRequiredMixin, generic.DeleteView):
    model = Note
    template_name = 'todoapp/DeleteNote.html'
    context_object_name = 'note'

    def get_object(self, **kwargs):
        return get_object_or_404(
            Note.objects.select_related('category'),
            slug=self.kwargs['note_slug'],
            user=self.request.user
        )

    def get_success_url(self):
        return reverse_lazy('todo:notes_of_category', kwargs={'category_slug': self.kwargs['category_slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_url'] = self.kwargs['category_slug']
        context['title'] = 'Удаление заметки'
        return context


class UpdateNote(LoginRequiredMixin, generic.UpdateView):
    model = Note
    form_class = UpdateNoteForm
    template_name = 'todoapp/UpdateNote.html'
    extra_context = {'title': 'Изменение заметки'}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('todo:notes_of_category', kwargs={'category_slug': self.kwargs['category_slug']})

    def get_object(self, queryset=None):
        return get_object_or_404(
            Note,
            slug=self.kwargs['note_slug'],
            user=self.request.user
        )


class CreateNote(LoginRequiredMixin, generic.CreateView):
    model = Note
    form_class = CreateNoteForm
    template_name = 'todoapp/CreateNote.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        note = form.save(commit=False)
        note.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('todo:notes_of_category', kwargs={'category_slug': self.kwargs['category_slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление заметки'
        if self.kwargs['category_slug'] != 'all':
            context['category_option'] = Category.objects.filter(user=self.request.user)
            context['category_select'] = get_object_or_404(
                Category,
                slug=self.kwargs['category_slug'],
                user=self.request.user
            )
        return context


class CreateCategory(LoginRequiredMixin, generic.CreateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = 'todoapp/CreateCategory.html'
    success_url = reverse_lazy('todo:all_categories')
    extra_context = {'title': 'Добавление категории'}

    def form_valid(self, form):
        category = form.save(commit=False)
        category.user = self.request.user
        return super().form_valid(form)


class CategoryListDelete(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = 'todoapp/CategoryListDelete.html'
    context_object_name = 'categories'
    extra_context = {'title': 'Удаление категорий'}

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryDelete(LoginRequiredMixin, generic.DeleteView):
    model = Category
    success_url = reverse_lazy('todo:category_delete_list')
    template_name = 'todoapp/DeleteCategory.html'
    context_object_name = 'category'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Category,
            pk=self.kwargs['category_id'],
            user=self.request.user
        )
