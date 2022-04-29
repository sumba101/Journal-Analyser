import pickle
from sklearn.feature_extraction.text import CountVectorizer

def tokenize(i):
    return i.split(' ')

vocabulary_to_load = pickle.load(open('sub_app/model_data/vocab.pkl', 'rb'))
cv = CountVectorizer(min_df=2, ngram_range=(1, 3), encoding='utf-8',tokenizer=tokenize, vocabulary=vocabulary_to_load)
model = pickle.load(open('sub_app/model_data/hindi_model.pkl','rb'))


def predict_emotion(sample_list):
    sample_review = sample_list
    test_sample = cv.transform(sample_review)  
    pred = model.predict(test_sample)
    return pred

def convert(pred):
    if pred ==0:
        return 'Angry'
    elif pred == 1:
        return 'Happy'
    elif pred == 2:
        return 'Sad'
    else:
        return 'Neutral'

def generate_analysis(user_data):
    # Param user_data is a list of dictionaries, each dict has "entry" and "datetime" as keys and values 
    # Entry is from a specific day    
    analysis_data = list()
        
    for day in user_data:
        temp = dict()
        date_time = day["datetime"]
        entry = day["entry"].split()
        emotions = predict_emotion(entry)   
        temp["datetime"]=date_time
        temp["entry"]=day
        temp["emotion"]=[ convert(e) for e in emotions]
        analysis_data.append(temp)

    return analysis_data

