from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from .models import Picture

def pictures_page (request):
    pictures = Picture.objects.all()
    return render(request, 'pictures/pictures_page.html', {'pictures': pictures}) 