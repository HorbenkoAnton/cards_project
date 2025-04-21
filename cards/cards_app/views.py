from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Card
import random
import datetime
from django.urls import reverse


def index_view(request):
    return render(request, "cards_app/index.html", {})

def draft_view(request):
    try:
        draftable_cards = Card.objects.filter(is_draftable=True)
    except Card.DoesNotExist:
        raise Http404("card does not exist")

    if draftable_cards:
        random_card = random.choice(draftable_cards)
        return render(request, "cards_app/draft.html", {"random_card": random_card})
    else:
        return HttpResponse("""
        <script>
            alert("Congrats, you revised all your words!");
            window.location.href = "/";
        </script>
""")

def drafted_revision_action(request, id, result):
    card = get_object_or_404(Card, pk=id)

    if request.method == "POST" or request.method == "GET":
        card.last_time_drafted = datetime.datetime.now()
        card.last_result = result.lower() == "true"
        card.update_is_draftable()
        card.save()
        return redirect("draft_page")

    return redirect("index_page")

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

def unrevise_action(request,id):
    if request.method == "POST":
        card = get_object_or_404(Card,pk = id)
        card.unrevise()
        card.save()
    return redirect(reverse("words_page"))

def unrevise_all_action(request):
    if request.method == "POST":
        cards = Card.objects.all()
        for card in cards:
            card.unrevise()
            card.save()
    return redirect(reverse("words_page"))