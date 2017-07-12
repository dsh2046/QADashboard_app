from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def add(request):
    a = request.GET['a']
    b = request.GET.get('b',0)
    c = int(a)+int(b)
    return HttpResponse(str(c))

def add2(request, a, b):
    c=int(a)+int(b)
    return HttpResponse(str(c))

def index(request):
    string = map(str, range(20))
    return render(request, 'calculator/home.html', {'list': string})
