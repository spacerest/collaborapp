from django.shortcuts import render
from .models import Gift
from collaborapp.decorators import group_required


@group_required('us')  # private page, only admins and members of 'us' can access it
def show_card(request, birthday_person, birthday_gifter, age):
    template = str(birthday_person) + '/' + str(birthday_gifter) + '/' + str(age) + '/card.html'
    return render(request, template)

def home(request):
    data = {}
    data['gifts'] = Gift.objects.filter(recipient=request.user)
    print(data['gifts'])
    return render(request, 'home.html', data)
