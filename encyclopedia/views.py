from django.shortcuts import render,redirect
from random import randrange
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from sys import exit
import markdown2

class qSearchForm(forms.Form):
    q = forms.CharField(label=False)

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    # comment= forms.CharField(widget=forms.Textarea())
    content= forms.CharField(label="Content",widget=forms.Textarea(attrs={"rows":"15", "cols":"90"}))
class editPageForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.HiddenInput)
    # comment= forms.CharField(widget=forms.Textarea())
    content= forms.CharField(label="Content",widget=forms.Textarea(attrs={"rows":"15", "cols":"90"}))
   
def index(request):
    entries=util.list_entries()
    entryR=randrange(len(entries))
    return render(request, "encyclopedia/index.html", {
    "random": entries[randrange(len(entries))],
    "entries":entries,
    "form":qSearchForm,
    })

def search(request):
    entries=util.list_entries()
    entryR=randrange(len(entries))
    if request.method=="POST":
        qsearch = qSearchForm(request.POST)
        if qsearch.is_valid():
            rsearch = qsearch.cleaned_data["q"]        
            return redirect("wikis:wikiResult",name=rsearch)
    return render(request, "encyclopedia/index.html", {
    "random": entries[randrange(len(entries))],
    "entries":entries,
    "form":qSearchForm,
    })
def wiki(request, name):
    entries=util.list_entries()
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
            # print(string)
    if found:
        content=util.get_entry(name)
        content1=markdown2.markdown(content)
        # print(name,"-------------\n",content,"\n-------------\n",content1,"-------------\n")
        return render(request, "encyclopedia/wiki.html", {
        "name":name,
        "random": entries[randrange(len(entries))],
        "content":content1,
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
    entries=util.list_entries()
    entryR=randrange(len(entries))
    if request.method=="POST":
        qsearch = NewPageForm(request.POST)
        if qsearch.is_valid():
            tsearch = qsearch.cleaned_data["title"]
            for string in entries:
                # print("\n //////////",string.lower(), tsearch.lower() ,string.lower()== tsearch.lower(),"\n //////////")
                if string.lower()== tsearch.lower():
                    name=string
                    return render(request, "encyclopedia/npage.html", {
                    "error":True,
                    "newPage":qsearch,
                    "random": entries[randrange(len(entries))],
                    "form":qSearchForm,
                    "name":tsearch
                    })

            csearch = qsearch.cleaned_data["content"]        
            # print(tsearch,csearch,util.list_entries())
            util.save_entry(tsearch,"# "+tsearch+"\n"+csearch)
            # print(tsearch,csearch,util.list_entries())
            entries=util.list_entries()
            return HttpResponseRedirect ( reverse ("wikis:index" ))


    return render(request, "encyclopedia/npage.html", {
        "newPage":NewPageForm,
        "random": entries[randrange(len(entries))],
        "form":qSearchForm,
    })
def epague(request,name):
    if request.method=="POST":
        editEntrie = editPageForm(request.POST)
        if editEntrie.is_valid():
            newEntrie = editEntrie.cleaned_data["content"]
            newName = editEntrie.cleaned_data["title"]
            util.save_entry(newName,newEntrie)
            return HttpResponseRedirect ( reverse ("wikis:wikiResult", kwargs={ 'name':name }))
    entries=util.list_entries()
    content=util.get_entry(name)
    form=editPageForm(initial={'title':name,'content':content})
    return render(request, "encyclopedia/epage.html", {
        "editPage":form,
        "random": entries[randrange(len(entries))],
        "name": name,       
    })