from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect

def homepage (request):
    return render(request, 'homepage/homepage.html', {}) 