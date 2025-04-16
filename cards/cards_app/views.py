from django.http import HttpResponse,Http404
from django.shortcuts import render
from .models import Card
from django.views import generic
import random


def indexView(requset):
    return render(requset,"cards_app/index.html",{})


def draftView(request):
    try:
        draftable_cards = Card.objects.filter(is_draftable= True)
    except Card.DoesNotExist:
        raise Http404("card does not exist")
    random_card = random.choice(draftable_cards)
    return render(request,"cards_app/draft.html",{"random_card":random_card} )


def wordsView(request):
    try:
        words = Card.objects.all()
    except Card.DoesNotExist:
        raise Http404("card does not exist")
    return render(request,"cards_app/words.html", {"words":words})



def addWordPageView(request):
    return render(request, "cards_app/add_word.html",{})



def editWordPageView(request,id):
    try:
        card = Card.objects.get(pk=id)
    except Card.DoesNotExist:
        raise Http404("card does not exist")
    return render(request,"cards_app/edit_word.html",{"card":card})