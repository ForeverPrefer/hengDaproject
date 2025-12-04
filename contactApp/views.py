from django.shortcuts import render
from django.shortcuts import HttpResponse
from .forms import ResumeForm

# Create your views here.
def contact(request):
    return render(request, 'contact.html', {'activmenu': 'contactapp','smenu': 'contact',})

from .models import Ad

def recruit(request):
    AdList = Ad.objects.all().order_by('-publishDate')
    if request.method == "POST":
        resumeForm = ResumeForm(data=request.POST, files=request.FILES)
        if resumeForm.is_valid():
            resumeForm.save()
            return render(request, 'success.html', {
                'activmenu': 'contactapp',
                'smenu': 'recruit',
            })
    else:
        resumeForm = ResumeForm()
    return render(request, 'recruit.html', {
        'activmenu': 'contactapp',
        'smenu': 'recruit',
        'AdList': AdList,
        'resumeForm': resumeForm,
    })