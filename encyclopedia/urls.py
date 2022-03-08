from django.urls import path

from . import views

app_name = "wikis"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.search, name="wikiPage"),
    path("wiki/<str:name>", views.wiki, name="wikiResult"),
    path("wiki/<str:name>/edit", views.epague, name="wikiedit"),
    path("CreatePage", views.NewPage, name="create"),
    path("edit/<str:name>", views.epague, name="edit")
]
