import pickle
from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
import numpy as np
from .forms import JournalEntry
from .emotion_analysis import generate_analysis
from jchart import Chart
from jchart.config import Axes, DataSet, rgba

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


class BarChart(Chart):
    chart_type = 'bar'

    def set_data(self, analysis,emote):
        self.labels = [ ele["datetime"] for ele in analysis]
        self.data = [ ele["emotion"].count(emote) for ele in analysis]
        # self.data = [ { 'y':ele["emotion"].count(emote) ,'x': ele["datetime"]}  for ele in analysis] 

    def get_labels(self, **kwargs):
        return self.labels

    def get_datasets(self, **kwargs):
        colors = list()

        temp = list(np.random.choice(range(256), size=3))
        colors = [(rgba(temp[0],temp[1],temp[2],0.3)) for _ in range(len(self.labels))]

        return [DataSet(label='Bar Chart',
                        data=self.data,
                        borderWidth=1,
                        backgroundColor=colors,
                        borderColor=colors)]


class PieChart(Chart):
    chart_type = 'pie'
    
    def set_LandD(self,emotion):
        self.labels=list(emotion.keys())
        self.data = [ emotion[l] for l in self.labels]

    def get_labels(self, **kwargs):
        return self.labels

    def get_datasets(self, **kwargs):
        data = self.data
        colors = [
            "#FF6384",
            "#36A2EB",
            "#FFCE56",
            "#90EE90"
        ]
        return [DataSet(data=data,
                        label="Overall Emotion",
                        backgroundColor=colors,
                        hoverBackgroundColor=colors)]


def analysis_2(request):
    user_data = load_obj("Anand")
    analysis_results,_ = generate_analysis(user_data)
    print("="*5)        
    print(analysis_results)
    print("="*5)        
    pie = BarChart()
    pie.set_data(analysis_results,"Angry")

    # Analysis_results is a list of dictionaries
    # Each dictionary has keys ("datetime","emotions","entry")
    # "datetime" is the datetime of the journal entry
    # "entry" is a list of sentences that together form the journal entry
    # "emotions" is a list of emotions, equal in size to entry, that denotes respective emotions of sentences
    # "emotions" have values ['Angry','Happy','Sad','Neutral']
    return render( request, 'sub_app/result.html',{"line_chart":pie,"emote":"Angry"})

def analysis_3(request):
    user_data = load_obj("Anand")
    analysis_results,_ = generate_analysis(user_data)
    print("="*5)        
    print(analysis_results)
    print("="*5)        
    pie = BarChart()
    pie.set_data(analysis_results,"Happy")

    # Analysis_results is a list of dictionaries
    # Each dictionary has keys ("datetime","emotions","entry")
    # "datetime" is the datetime of the journal entry
    # "entry" is a list of sentences that together form the journal entry
    # "emotions" is a list of emotions, equal in size to entry, that denotes respective emotions of sentences
    # "emotions" have values ['Angry','Happy','Sad','Neutral']
    return render( request, 'sub_app/result.html',{"line_chart":pie,"emote":"Happy"})

def analysis_4(request):
    user_data = load_obj("Anand")
    analysis_results,_ = generate_analysis(user_data)
    print("="*5)        
    print(analysis_results)
    print("="*5)        
    pie = BarChart()
    pie.set_data(analysis_results,"Sad")

    # Analysis_results is a list of dictionaries
    # Each dictionary has keys ("datetime","emotions","entry")
    # "datetime" is the datetime of the journal entry
    # "entry" is a list of sentences that together form the journal entry
    # "emotions" is a list of emotions, equal in size to entry, that denotes respective emotions of sentences
    # "emotions" have values ['Angry','Happy','Sad','Neutral']
    return render( request, 'sub_app/result.html',{"line_chart":pie,"emote":"Sad"})

def analysis_5(request):
    user_data = load_obj("Anand")
    analysis_results,_ = generate_analysis(user_data)
    print("="*5)        
    print(analysis_results)
    print("="*5)        
    pie = BarChart()
    pie.set_data(analysis_results,"Neutral")

    # Analysis_results is a list of dictionaries
    # Each dictionary has keys ("datetime","emotions","entry")
    # "datetime" is the datetime of the journal entry
    # "entry" is a list of sentences that together form the journal entry
    # "emotions" is a list of emotions, equal in size to entry, that denotes respective emotions of sentences
    # "emotions" have values ['Angry','Happy','Sad','Neutral']
    return render( request, 'sub_app/result.html',{"line_chart":pie,"emote":"Neutral"})


def analysis(request):
    user_data = load_obj("Anand")
    analysis_results,emotion = generate_analysis(user_data)
    print("="*5)        
    print(analysis_results)
    print("="*5)        
    pie = PieChart()
    pie.set_LandD(emotion)

    # Analysis_results is a list of dictionaries
    # Each dictionary has keys ("datetime","emotions","entry")
    # "datetime" is the datetime of the journal entry
    # "entry" is a list of sentences that together form the journal entry
    # "emotions" is a list of emotions, equal in size to entry, that denotes respective emotions of sentences
    # "emotions" have values ['Angry','Happy','Sad','Neutral']
    return render( request, 'sub_app/result.html',{"line_chart":pie})
