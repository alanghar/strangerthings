import textwrap

from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic.base import View
from lightmanager import LightManager


def homepageview(request):
    lm = LightManager.getInstance()
    #lm.spell('tipper')
    return render(request, 'index.html', {})

def spellview(request):
    text = request.POST.get('spell_text')
    lm = LightManager.getInstance()
    lm.enqueuePhrase(text)
    return redirect(homepageview)