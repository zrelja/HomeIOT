import json

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
def index(request):

    template = 'backend/app.html'
    return render(request, template)


def app(request):

    template = 'backend/app.html'
    return render(request, template)

@require_GET
def privacy(request):
    return render(request,
                  'backend/privacy.html',
                  {
                      'title': 'SmithX',
                      'message': "Thank you! Your request has been received."
                  })

def smithxApp(request):

    template = 'backend/smithxApp.html'
    return render(request, template)