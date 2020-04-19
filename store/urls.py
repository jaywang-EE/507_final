from django.urls import path, re_path, reverse_lazy
from . import views
from django.views.generic import TemplateView

app_name='store'

urlpatterns = [
    path('', views.PicCreateView.as_view(), name='all'),
    re_path('^(?P<code>[A-Za-z0-9]+)$', views.PicDetailView.as_view(), name='pic_detail'),
    #path('create_', views.PicCreateView.as_view(), name='pic_create'),
    path('pic_picture_/<int:pk>', views.stream_file, name='pic_picture'),
]

