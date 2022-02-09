from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from .models import Sponsors

def sponsors_page (request):
    sponsors = Sponsors.objects.all()
    return render(request, 'sponsors/sponsors_page.html', {'sponsors': sponsors}) 