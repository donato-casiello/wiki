from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# To display an entry page
def wiki(request, entry):
    # Get the list of all entries
    entry_list = util.list_entries()
    # Lower case the list to compare with entry, case-insensetive
    entry_list = [x.lower() for x in entry_list]
    # The entry exists
    if entry.lower() in entry_list: 
        text = markdown2.markdown(util.get_entry(entry))
        title = util.get_entry(entry)
        return render(request, "encyclopedia/wiki.html", {
            "entry": entry,
            "text": text, 
            "list": entry_list
        })
    # The entry doesn't exists
    else:
        # We have to change here to redirect to customise error page
        return render(request, "encyclopedia/not_found.html", {
            "entry": entry
        })
    
# Search function
def search(request):
    if request.method == "POST":
        entry = request.POST["q"]
        # Convert all the entries in uppercase 
        list = util.list_entries()
        list = [x.upper() for x in list]
        # Is in the list
        if entry.upper() in list:
            return HttpResponseRedirect(reverse("entry:wiki", args=(entry, )))
        # Isn't in the list
        else:
            substring = [i for i in list if entry.upper() in i]
            return render(request, "encyclopedia/search.html", {
                "substring": substring
            })
        
        
# Create a new page
def new_page(request):
    # user submit the page
    if request.method == "POST":
        title = request.POST["title"]
        text = request.POST["text"]
        # Check user submit empty field
        if title == "" or text == "":
            return render (request, "encyclopedia/new_page.html", {
                "message" : "Can't save with an empty field"
            })
        # Check if the entry already exists
        entry_list = util.list_entries()
        # Ignoring upper and lowercase
        entry_list = [x.lower() for x in entry_list]
        if title.lower() in entry_list:
            return render(request, "encyclopedia/new_page.html", {
                "message": "This entry already exists"
            })
        # User submit valid input
        else: 
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse("entry:wiki", args=(title, )))
    # user get the page
    else:
        return render(request, "encyclopedia/new_page.html")
    
# Edit page
def edit(request, entry):
    text = util.get_entry(entry)
    if request.method == "POST":
        title = request.POST["title"]
        text = request.POST["content"]
        # User submit an empty input
        if title == "" or text == "":
            return render(request, "encyclopedia/edit.html", {
                "message" : "Can't save with an empty field", 
                "title" : entry, 
                "text" : text
            })
        entry_list = util.list_entries()
        entry_list = [x.lower() for x in entry_list]
        util.save_entry(title, text)
        return HttpResponseRedirect(reverse("entry:wiki", args=(title, )))
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": entry, 
            "text": text
        })
        
# Random search
def caso(request):
    list = util.list_entries()
    entry = random.choice(list)
    return HttpResponseRedirect(reverse("entry:wiki", args=(entry, )))