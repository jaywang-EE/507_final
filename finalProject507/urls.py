from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name='fp507'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('json', views.GetJsonView.as_view(), name='json'),
    path('data', views.DataView.as_view(), name='data'),
    path('news', views.NewsView.as_view(), name='news'),
]

