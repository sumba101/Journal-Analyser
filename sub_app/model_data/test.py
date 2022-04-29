import pickle
from sklearn.feature_extraction.text import CountVectorizer

def tokenize(i):
    return i.split(' ')

vocabulary_to_load = pickle.load(open('vocab.pkl', 'rb'))
cv = CountVectorizer(min_df=2, ngram_range=(1, 3), encoding='utf-8',tokenizer=tokenize, vocabulary=vocabulary_to_load)

model = pickle.load(open('hindi_model.pkl','rb'))

def predict_sarcasm(sample_review):
    sample_review = sample_review
    test_sample = cv.transform(sample_review)  
    pred = model.predict(test_sample)
    return pred

sample_text =[u"कैब ड्राइवर बुरा था",u"कैब ड्राइवर बुरा था"]
prediction = predict_sarcasm(sample_text)
print(prediction[1])