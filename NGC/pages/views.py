from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'pages/index.html')

def events(request):
    return render(request, 'pages/events.html')

def hosts(request):
    return render(request, 'pages/hosts.html')

def login_view(request):
    return render(request, 'pages/login.html')
