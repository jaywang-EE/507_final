from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name='home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('projects', views.ProjectsView.as_view(), name='projects'),
]

