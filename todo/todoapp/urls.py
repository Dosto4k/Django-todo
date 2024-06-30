from django.urls import path

from . import views

app_name = 'todo'
urlpatterns = [
    path('', views.CategoryListView.as_view(), name='all_categories'),
    path('create/', views.CreateCategory.as_view(), name='create_category'),
    path('delete/', views.CategoryListDelete.as_view(), name='category_delete_list'),
    path('delete/<int:category_id>/', views.CategoryDelete.as_view(), name='delete_category'),
    path('<slug:category_slug>/', views.NotesOfCategory.as_view(), name='notes_of_category'),
    path('<slug:category_slug>/create/', views.CreateNote.as_view(), name='create_note'),
    path('<slug:category_slug>/<slug:note_slug>/delete/', views.DeleteNote.as_view(), name='delete_note'),
    path('<slug:category_slug>/<slug:note_slug>/update/', views.UpdateNote.as_view(), name='update_note'),
]


# todo подумать если мы добавим категорию a(На английском) то уже не сможем добавить категорию а(На русском)
#   потому что slug у них будет одинаковый
#   также это работает и с заголовком заметки
#   подумать как можно это исправить

# todo сделать регистрацию

