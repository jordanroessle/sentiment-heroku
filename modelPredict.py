from tensorflow.keras.models import load_model
import pickle
import pandas as pd
import nltk
import string
import re
from nltk.corpus import stopwords 
wn = nltk.WordNetLemmatizer()
string.punctuation
stop = stopwords.words('english')


def predictModel(theTweet):
    list_for_vectorize = []
    list_for_vectorize.append(theTweet)
    df = pd.DataFrame({'tweet':list_for_vectorize})
    clean_df = lema(df, "tweet")
    with open('vectorizer.pickle', 'rb') as inp:
        vectorize = pickle.load(inp)
        model = load_model('deep_sentiment_model_trained_zenith.h5')
        predict_me = vectorize.transform(clean_df['joined_lemm']).toarray()
        return float(model.predict(predict_me)[0][0])

def remove_punct(text):
    text_nopunct = "".join([char for char in text if char not in string.punctuation])
    return text_nopunct

def tokenize(text):
    tokens = re.split('\W+', text)
    return tokens

def remove_stopwords(tokenized_list):
    text = [word for word in tokenized_list if word not in stop]# To remove all stopwords
    return text

def lemmatizing(tokenized_text):
    text = [wn.lemmatize(word) for word in tokenized_text]
    return text

def lema(df,column):
    body_text_clean = df[column].apply(lambda x: remove_punct(x))
    body_text_tokenized = body_text_clean.apply(lambda x: tokenize(x.lower()))
    body_text_nostop = body_text_tokenized.apply(lambda x: remove_stopwords(x))
    df['body_text_lemmatized'] = body_text_nostop.apply(lambda x: lemmatizing(x))
    it_list = []
    for row in df['body_text_lemmatized']:
        it_list.append(" ".join(row))
    df['joined_lemm'] = it_list
    final_df = pd.DataFrame()
    final_df['joined_lemm'] = df['joined_lemm']
    return final_df