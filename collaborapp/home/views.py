from django.shortcuts import render, redirect
from notes.forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

# gunicorn -b 0.0.0.0:8002 collaborapp.wsgi --daemon --workers=3


def go_home(request):
    return render(request, 'home/index.html')


#not currently being used
def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'home/signup.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'home/signup.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'home/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'home/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('/login')
