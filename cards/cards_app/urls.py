from django.urls import path
from . import views


urlpatterns = [
    path("", views.indexView, name="index"),

    path("draft/", views.draftView,name="draft"),
    path("draft/<int:id>/<str:result>", views.drafted_revision,name = "revision"),
    path("words/", views.wordsView,name="words"),
    path("add/",views.addWordPageView,name="add"),
    path("addWord/",views.addWord, name="addWord"),
    path("edit/<int:id>",views.editWordPageView,name="edit"),
    path("editWord/<int:id>", views.editWord, name = "editWord"),
    path("deleteWord/<int:id>",views.deleteWord, name = "deleteWord"),

]