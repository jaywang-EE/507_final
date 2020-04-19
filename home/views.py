from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from datetime import datetime

from finalProject507.models import CountyCase, County
from finalProject507.crawler import craw
from finalProject507.crawlers.crawler import craw_covid
# Create your views here.
import json


class HomeView(View):
    def get(self, request) :
        context = {}
        return render(request, 'home/index.html', context)

class ProjectsView(View):
    def get(self, request) :
        context = {}
        return render(request, 'home/projects.html', context)

