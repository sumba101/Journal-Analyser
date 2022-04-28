import pickle
from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import JournalEntry


def home(request):
    return render( request, 'sub_app/home.html')

def save_obj(obj, name ):
    with open('sub_app/entries_collected/' + name + '.pkl', 'rb') as f:
        curr_data = pickle.load(f)
#  Curr_data is a list of dicts, each dict contains "entry" and "datetime" as keys and values
    curr_data.append(obj)

    with open('sub_app/entries_collected/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('sub_app/AnswersData/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def journal(request):
    if (request.method == 'POST'):
        form = JournalEntry( request.POST)
        if form.is_valid():
            form["datetime"] = datetime.now()
            print(form.cleaned_data)
            save_obj(form,"Anand")
            return HttpResponseRedirect( '/' )

        else:
            print( form.errors )

    form = JournalEntry()
    return render( request, 'sub_app/app.html',{'form':form} )


def analysis(request):
    return render( request, 'sub_app/result.html')
