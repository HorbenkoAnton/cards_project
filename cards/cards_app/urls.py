from django.urls import path
from . import views


urlpatterns = [
    path("", views.indexView, name="index"),
    path("draft/", views.draftView,name="draft"),
    path("words/", views.wordsView,name="words"),
    path("add/",views.addWordPageView,name="add"),
    path("edit/<int:id>",views.editWordPageView,name="edit")
]