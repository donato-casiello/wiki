from django.urls import path

from . import views

app_name = "entry"

urlpatterns = [
    path("", views.index, name="index"), 
    path("wiky/<str:entry>", views.wiky, name="wiky"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("caso", views.caso, name="caso")
]
