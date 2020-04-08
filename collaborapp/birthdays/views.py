from django.shortcuts import render
from collaborapp.decorators import group_required


@group_required('us')  # private page, only admins and members of 'us' can access it
def show_card(request, birthday_person, age):
    template = str(birthday_person) + '/' + str(age) + '/card.html'
    return render(request, template)
