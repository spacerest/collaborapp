from django.shortcuts import render
from postoffice.forms import LetterReceiver


# Create your views here.

def home(request):
    form = LetterReceiver()
    data = {'form': form}
    return render(request, 'postoffice/home.html', data)
