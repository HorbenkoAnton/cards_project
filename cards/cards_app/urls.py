from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index_page"),

    path("draft/", views.draft_view, name="draft_page"),
    path("draft/<int:id>/<str:result>/", views.drafted_card_answer_action, name="drafted_card_answer"),

    path("words/", views.words_view, name="words_page"),

    path("add/", views.add_word_view, name="add_word_page"),
    path("add/submit/", views.add_word_action, name="add_word"),

    path("edit/<int:id>/", views.edit_word_view, name="edit_word_page"),
    path("edit/<int:id>/submit/", views.edit_word_action, name="edit_word"),

    path("delete/<int:id>/", views.delete_word_action, name="delete_word"),

]
