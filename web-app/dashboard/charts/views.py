from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context = {
    }
    return render(request, 'charts/home.html', context)


def static_page(request):
    return render(request, 'charts/static_page.html', {'title': 'static_page'})


def ad(request):
    return render(request, 'charts/ad.html', {'title': 'ad'})


def detailed(request):
    return render(request, 'charts/detailed.html', {'title': 'detailed'})


def history(request):
    return render(request, 'charts/history.html', {'title': 'history'})


def visit(request):
    return render(request, 'charts/visit.html', {'title': 'visit'})


def productive(request):
    return render(request, 'charts/productive.html', {'title': 'productive'})
