from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render, redirect ,get_object_or_404
from .models import Card
from django.views import generic
import random
import datetime


def indexView(requset):
    return render(requset,"cards_app/index.html",{})

def draftView(request):
    try:
        draftable_cards = Card.objects.filter(is_draftable= True)
    except Card.DoesNotExist:
        raise Http404("card does not exist")
    if draftable_cards:
        random_card = random.choice(draftable_cards)
        return render(request,"cards_app/draft.html",{"random_card":random_card} )
    else:
        return HttpResponse("""
        <script>
            alert("Congrats, you revised all your words!");
            window.location.href = "/";
        </script>
""")

def drafted_revision(request, id, result):
    card = get_object_or_404(Card, pk=id)

    if request.method == "POST" or request.method == "GET":
        card.last_time_drafted = datetime.datetime.now()
        card.last_result = result.lower() == "true"
        card.update_is_draftable()
        card.save()
        return redirect("draft")

    return redirect("index")


def wordsView(request):
    try:
        words = Card.objects.all()
    except Card.DoesNotExist:
        raise Http404("card does not exist")
    return render(request,"cards_app/words.html", {"words":words})

def addWordPageView(request):
    return render(request, "cards_app/add_word.html",{})

def addWord(request):
    print(request.POST)
    if request.method == "POST":
        eng = "".join(request.POST["eng_word"])
        ukr = "".join(request.POST["ukr_word"])
        Card.objects.create(eng_word = eng,ukr_word = ukr)
        return redirect("index")  
    return HttpResponseRedirect("/")

def editWordPageView(request,id):
    try:
        card = Card.objects.get(pk=id)
    except Card.DoesNotExist:
        raise Http404("card does not exist")
    return render(request,"cards_app/edit_word.html",{"card":card})

def editWord(request,id):
    if request.method == "POST":
        card = get_object_or_404(Card,pk=id)
        card.ukr_word = request.POST['ukr_word']
        card.eng_word = request.POST['eng_word']
        card.save()
        return redirect("index")
    return HttpResponseRedirect("/")

def deleteWord(request,id):
    if request.method == "POST":
        get_object_or_404(Card,pk=id).delete()
        return HttpResponseRedirect("/words")
    return HttpResponseRedirect("/")
