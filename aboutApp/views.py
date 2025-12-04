from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Award

# Create your views here.
def survey(request):
    return render(request, 'survey.html', {'activmenu': 'about','smenu': 'survey',})

def honor(request):
    awards = Award.objects.all()
    return render(request, 'honor.html', {'activmenu': 'about','smenu': 'honor','awards': awards})