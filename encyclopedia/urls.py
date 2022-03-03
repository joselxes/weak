from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.search, name="wikiPage"),
    path("wiki/<str:name>", views.wiki, name="wikiResult"),
    path("CreatePage", views.NewPage, name="create")
]
