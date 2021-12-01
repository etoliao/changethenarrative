from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect

def pictures_page (request):
    return render(request, 'pictures/pictures_page.html')