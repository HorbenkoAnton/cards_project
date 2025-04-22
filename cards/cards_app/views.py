from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Card
import random
import datetime
from django.urls import reverse

def index_view(request):
    return render(request, "cards_app/index.html", {})

def draft_view(request):
    cards = Card.objects.all()
    if cards:
        weights=[card.weight for card in cards]
        random_card = random.choices(cards, weights, k=1)[0]
        return render(request, "cards_app/draft.html", {"random_card": random_card})
    else:
        return redirect(reverse("add_word_page"))


def drafted_card_answer_action(request,id, result):
    card = get_object_or_404(Card,pk=id)
    if result == 'true':
        card.drafted_true()
    elif result == 'false':
        card.drafted_false()
    card.save()
    return redirect(reverse("draft_page")) 


def words_view(request):
    try:
        words = Card.objects.all()
    except Card.DoesNotExist:
        raise Http404("card does not exist")
    return render(request, "cards_app/words.html", {"words": words})

def add_word_view(request):
    return render(request, "cards_app/add_word.html", {})

def add_word_action(request):
    if request.method == "POST":
        eng = request.POST["eng_word"]
        ukr = request.POST["ukr_word"]
        Card.objects.create(eng_word=eng, ukr_word=ukr)
        return redirect(reverse("index_page"))
    return redirect(reverse("index_page"))

def edit_word_view(request, id):
    try:
        card = Card.objects.get(pk=id)
    except Card.DoesNotExist:
        raise Http404("card does not exist")
    return render(request, "cards_app/edit_word.html", {"card": card})

def edit_word_action(request, id):
    if request.method == "POST":
        card = get_object_or_404(Card, pk=id)
        card.ukr_word = request.POST['ukr_word']
        card.eng_word = request.POST['eng_word']
        card.save()
        return redirect(reverse("words_page"))
    return redirect(reverse("index_page"))

def delete_word_action(request, id):
    if request.method == "POST":
        get_object_or_404(Card, pk=id).delete()
        return redirect(reverse("words_page"))
    return redirect(reverse("index_page"))
