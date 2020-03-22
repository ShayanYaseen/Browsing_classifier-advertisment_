from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='chart-home'),
    path('static_page/', views.static_page, name='chart-static_page'),
    path('ad/', views.ad, name='chart-ad'),
    path('detailed/', views.detailed, name='chart-detailed'),
    path('history/', views.history, name='chart-history'),
    path('productive/', views.productive, name='chart-productive'),
    path('visit/', views.visit, name='chart-visit'),
]
