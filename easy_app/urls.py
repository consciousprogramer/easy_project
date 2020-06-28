from django.urls import path,include
from . import views

appname = "easy_app"
urlpatterns = [
    path("", views.index, name = "index"),

]
