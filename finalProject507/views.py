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

# for JSON data
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

#get view
from django.views import View
from finalProject507.models import Order, County, CountyCase

#Aggregation
from django.db.models import Sum, Max

#plotly
from plotly.offline import plot
import plotly.graph_objs as go

class HomeView(View):
    def get(self, request) :
        context = {}
        return render(request, 'finalProject507/index.html', context)

class DataView(View):
    def get(self, request) :
        context = {
            "states": craw_covid()["county"], 
        }
        context["states"].sort()
        print(context)

        data = None
        state = request.GET.get('state')
        print(state)

        if state and state != "All States":
            data = CountyCase.objects.filter(county__stateName=state) if (state != "All States") else CountyCase.objects.all()

            fromDate = request.GET.get('from')
            print(fromDate)
            if fromDate:
                data = data.filter(date__gte=fromDate)

            toDate = request.GET.get('to')
            print(toDate)
            if toDate:
                data = data.filter(date__lte=toDate)

            if data:
                date = data.order_by('county__stateName', '-date')

            mode = request.GET.get('mode')
            print(mode)
            if mode == "SUM":
                print(data)
                data = data.values('county__countyName') \
                    .annotate(cases=Max('cases'), deaths=Max('deaths')) \
                    .order_by('-cases')
            elif mode == "plot":
                """
                plot_div = plot([Scatter(x=x_data, y=y_data,
                                    mode='lines', name='test',
                                    opacity=0.8, marker_color='green')],
                           output_type='div')
                data = go.Data([trace0, trace1])
                """
                data = data.values('county__countyName', 'cases', 'deaths', 'date')\
                    .order_by('county__countyName', 'date')
                print(data)
                traces = []

                current_county = None
                dates  = []
                cases  = []
                deaths = []
                for row in data:
                    if not current_county:
                        current_county = row["county__countyName"]
                    elif current_county != row["county__countyName"]:#save
                        traces.append(go.Scatter(x=dates, y=cases, name=current_county,))

                        current_county = None
                        dates  = []
                        cases  = []
                        deaths = []

                        current_county = row["county__countyName"]
                    dates.append(row["date"])
                    cases.append(row["cases"])
                traces.append(go.Scatter(x=dates, y=cases, name=current_county,))

                context["plot"] = plot(go.Data(traces), output_type='div')
                data = None
            else:
                date = None

        context["data"] = data
        return render(request, 'finalProject507/data.html', context)

class NewsView(View):
    def get(self, request) :
        context = {
            "states": craw_covid()["orders"], 
        }

        data = None
        state = request.GET.get('state')
        print(state)
        if state: 
            print(state)
            data = Order.objects.filter(stateName=state) if state != "ALL" else Order.objects.all()

            fromDate = request.GET.get('from')
            print(fromDate)
            if fromDate:
                data = Order.objects.filter(date__gte=fromDate)

            toDate = request.GET.get('to')
            print(toDate)
            if toDate:
                data = Order.objects.filter(date__lte=toDate)
            if data:
                date = data.order_by('-date', 'stateName')
        context["data"] = data
        return render(request, 'finalProject507/news.html', context)

class GetJsonView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        """
        category = request.GET.get('cat')
        fromDate = request.GET.get('fromDate')
        toDate = request.GET.get('toDate')
        count = request.GET.get('count')

        news = News.objects.all()
        if category:
            news = news.filter(category=category)

        if fromDate:
            try:
                fromDate = datetime.strptime(fromDate, '%Y-%m-%d').date()
                news = news.filter(date__gte=fromDate)
            except:
                print("ERROR date: "+fromDate)

        if toDate:
            try:
                toDate = datetime.strptime(toDate, '%Y-%m-%d').date()
                news = news.filter(date__lte=toDate)
            except:
                print("ERROR date: "+toDate)

        #news = News.objects.filter(date__range=["2011-01-01", "2011-01-31"])[:count]
        if count: 
            news = news[:int(count)]


        news = news.values()
        news_list = list(news)
        """
        """
        return JsonResponse(users_list, safe=False)
        user_count = User.objects.filter(active=True).count()
        """
        ctx = {"covid": craw_covid(),}
        return Response(ctx)