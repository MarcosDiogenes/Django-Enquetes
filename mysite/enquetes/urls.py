from django.urls import path

from . import views

app_name = "enquetes"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detalhe"),
    path("<int:pk>/resultado/", views.ResultsView.as_view(), name="resultado"),
    path("<int:pergunta_id>/voto/", views.voto, name="voto"),
]