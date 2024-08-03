from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import URL
import random
import string

def index(request):
    return render(request, 'index.html')

def shorten_url(request):
    if request.method == 'POST':
        orignal_url = request.POST.get('orignal_url')
        
        # Check if the orignal URL already exists in the database
        existing_url = URL.objects.filter(orignal_url=orignal_url).first()
        if existing_url:
            short_url = request.build_absolute_uri('/') + existing_url.short_url
            return render(request, 'index.html', {'short_url': short_url})
        
        # If the orignal URL doesn't exist, generate a short code and create a new entry
        short_code = generate_short_code()
        short_url = request.build_absolute_uri('/') + short_code
        URL.objects.create(orignal_url=orignal_url, short_url=short_code)
        return render(request, 'index.html', {'short_url': short_url})
    return redirect('index')

def redirect_original_url(request, short_url):
    orignal_url = URL.objects.get(short_url=short_url).orignal_url
    return redirect(orignal_url)

def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for i in range(6))
    while URL.objects.filter(short_url=short_code).exists():
        short_code = ''.join(random.choice(characters) for i in range(6))
    return short_code
