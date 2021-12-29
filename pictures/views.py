from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from .models import Picture

def pictures_page (request):
    pictures = Picture.objects.all()
    return render(request, 'pictures/pictures_page.html', {'pictures': pictures}) 

#def pics_css(request):
    #pics = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date') <-- IDK what to sub this with
    #return render(request, 'pictures/pics.css', {'pics': pics})