from django.shortcuts import render,redirect
from random import randrange
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
class qSearchForm(forms.Form):
    q = forms.CharField(label=False)
entries=util.list_entries()
entryR=randrange(len(entries))   
def index(request):
    return render(request, "encyclopedia/index.html", {
    "random": entries[randrange(len(entries))],
    "entries":entries,
    "form":qSearchForm,
    })

def search(request):
    if request.method=="POST":
        qsearch = qSearchForm(request.POST)
        if qsearch.is_valid():
            rsearch = qsearch.cleaned_data["q"]        
            return redirect("wiki:wikiResult",name=rsearch)
    return render(request, "encyclopedia/index.html", {
    "random": entries[randrange(len(entries))],
    "entries":entries,
    "form":qSearchForm,
    })
def wiki(request, name):
    namel=name.lower()
    nameBool=False
    found=False
    content=""
    nlist=[]
    for string in entries:
        if string.lower()== namel:
            found=True
            name=string
        elif namel in string.lower():
            nlist.append(string)
            nameBool= True
            print(string)

    if found:
        content=util.get_entry(name)
        return render(request, "encyclopedia/wiki.html", {
        "name":name,
        "random": entries[randrange(len(entries))],
        "content":content,
        "form":qSearchForm,
        })
    if nameBool:
        return render(request, "encyclopedia/wiki.html", {
            "empty":True,
            "similars":True,
            "name":name,
            "random": entries[randrange(len(entries))],
            "entries":nlist,
            "form":qSearchForm,
        })
    return render(request, "encyclopedia/wiki.html", {
    "empty":True,
    "name":name,
    "random": entries[randrange(len(entries))],
    "entries":entries,
    "form":qSearchForm,
    })

def NewPage(request):
    return render(request, "encyclopedia/npage.html", {
        "random": entries[randrange(len(entries))],
        "form":qSearchForm,
    })

