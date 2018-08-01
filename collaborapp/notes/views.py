from django.http import HttpResponse
from django.shortcuts import render, redirect
from notes.forms import SignupForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/home')
        else:
            return HttpResponse('HWEEEI')
    else:
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'login.html')


@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')
