from django.shortcuts import render
from .models import Country
# Create your views here.

def stats(request):
    countries = Country.objects.all()
    return render(request, 'site_info/stats.html', {
        'countries': countries,
    })