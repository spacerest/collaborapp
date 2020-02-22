from django.shortcuts import render

# Create your views here.

def show_card(request, birthday_person, age):
    template = str(birthday_person) + '/' + str(age) + '/card.html'
    return render(request, template)
