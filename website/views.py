# Useful Links:
# http://ccbv.co.uk/
# http://django-braces.readthedocs.org/en/latest/index.html

from django.shortcuts import render_to_response
from django.template import RequestContext

def homepage(request):
    return render_to_response('homepage.html', locals(), RequestContext(request))
