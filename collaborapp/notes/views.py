from django.http import HttpResponse
from django.shortcuts import render, redirect
from notes.forms import SignupForm, NoteForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from notes.models import Note

@login_required(login_url='/login')
def home(request):
    notes = Note.objects.filter(author=request.user).order_by('-created')

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            author = request.user
            note = Note(title=title, body=body, author=author)
            note.save()
            form = NoteForm()
        else:
            form = NoteForm(request.POST)
    else:
        form = NoteForm()
    return render(request, 'home.html', {'form': form, 'notes': notes})

