import pickle
import time

from django.http import HttpResponseRedirect
from django.shortcuts import render

import gensim.downloader as api
from .forms import TextInput, QuestionsForm

from .parser import getProcessedData
focus_word=str()
noOfSections=int()
selected=list()
candidate_content=list()

def home(request):
    if(request.method=='POST'):
        form = TextInput( request.POST )
        if form.is_valid():
            global focus_word
            focus_word = form.cleaned_data['focus_word']
            # print("loading model ")
            # model = api.load( "fasttext-wiki-news-subwords-300" )
            # similar = model.most_similar( focus_word , topn=20 )
            # print("Loaded model and similar words")
            global noOfSections, selected, candidate_content
            # noOfSections, selected, candidate_content = getProcessedData(similar)
            noOfSections=load_obj("noOfSections")
            selected=load_obj("selectedOrder")
            candidate_content=load_obj("sectionContent")
            print(focus_word)
            return HttpResponseRedirect( '/questions/' )

    query = TextInput()

    return render( request, 'sub_app/home.html', {'query': query} )

def save_obj(obj, name ):
    with open('sub_app/AnswersData/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('sub_app/AnswersData/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def questions(request):
    if (request.method == 'POST'):
        form = QuestionsForm( request.POST, count=noOfSections, questions=selected, examples=candidate_content, focus_word=focus_word )
        if form.is_valid():
            dataset = dict()
            for i,field in enumerate(selected):
                dataset[field] = form.cleaned_data['{}) What is your answer for the section: {} under the topic {}' .format(i+1,field,focus_word)]

            print(dataset)
            save_obj(dataset,focus_word+time.ctime())
            return HttpResponseRedirect( '/results/' )

        else:
            print( form.errors )

    form = QuestionsForm( count=noOfSections, questions=selected, examples=candidate_content,
                      focus_word=focus_word )
    return render( request, 'sub_app/app.html',{'form':form} )


def result(request):
    return render( request, 'sub_app/result.html')
