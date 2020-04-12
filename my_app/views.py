from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models
# Create your views here.
BASE_CRAIGLIST_URL = 'https://lima.craigslist.org/search/hhh?query={}'

def home(request):
    return render(request,'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url= BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li',{'class':'result-row'})


    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        
        final_postings.append((post_title, post_url, post_price))

    stuff = {
    'search':search,
    'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html',stuff)
