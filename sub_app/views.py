import pickle
from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import JournalEntry
from .emotion_analysis import generate_analysis

def home(request):
    return render( request, 'sub_app/home.html')

def save_obj(obj, name ):
    try:
        with open('sub_app/entries_collected/' + name + '.pkl', 'rb') as f:
            curr_data = pickle.load(f)
    except:
        curr_data=list()
#  Curr_data is a list of dicts, each dict contains "entry" and "datetime" as keys and values
    curr_data.append(obj)

    with open('sub_app/entries_collected/'+ name + '.pkl', 'wb') as f:
        pickle.dump(curr_data, f)

def load_obj(name):
    with open('sub_app/entries_collected/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def journal(request):
    if (request.method== 'POST'):
        form = JournalEntry(request.POST)
        if form.is_valid():
            temp = dict()
            temp["datetime"] = datetime.now()
            temp["entry"] = form.cleaned_data["entry"]
            print(temp)
            save_obj(temp,"Anand")
            return HttpResponseRedirect( '/' )
        else:
            print( form.errors )

    form = JournalEntry()
    return render( request, 'sub_app/app.html',{'form':form} )

# Todo: Finish this function and the result.html 
def analysis(request):
    user_data = load_obj("Anand")
    analysis_results = generate_analysis(user_data)
    print("="*5)        
    print(analysis_results)
    print("="*5)        

    # Analysis_results is a list of dictionaries
    # Each dictionary has keys ("datetime","emotions","entry")
    # "datetime" is the datetime of the journal entry
    # "entry" is a list of sentences that together form the journal entry
    # "emotions" is a list of emotions, equal in size to entry, that denotes respective emotions of sentences
    # "emotions" have values ['Angry','Happy','Sad','Neutral']
    return render( request, 'sub_app/result.html',{"result": user_data})
