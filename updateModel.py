from nltk.corpus.reader import senseval
from nltk.corpus.reader.knbc import test
from tensorflow.keras.models import load_model
import pickle
import pandas as pd
import nltk
import string
from modelPredict import lema
from nltk.corpus import stopwords
import keras.metrics

wn = nltk.WordNetLemmatizer()
string.punctuation
stop = stopwords.words('english')


# variables used in isolated_mode.py to fit model
EPOCHS = 50
BATCH_SIZE = 2048
METRICS = [
      keras.metrics.TruePositives(name='tp'),
      keras.metrics.FalsePositives(name='fp'),
      keras.metrics.TrueNegatives(name='tn'),
      keras.metrics.FalseNegatives(name='fn'), 
      keras.metrics.BinaryAccuracy(name='accuracy'),
      keras.metrics.Precision(name='precision'),
      keras.metrics.Recall(name='recall'),
      keras.metrics.AUC(name='auc'),
      keras.metrics.AUC(name='prc', curve='PR'), # precision-recall curve
]


def updateModel(tweetsFit):
    #tweetsFit should be list dictionarys
    df = pd.DataFrame(tweetsFit)
    clean_df = lema(df, "tweet")
    with open('vectorizer.pickle', 'rb') as inp:
        vectorize = pickle.load(inp)
        model = load_model('deep_sentiment_model_trained_zenith.h5')
        new_train = vectorize.transform(clean_df['joined_lemm']).toarray()
        new_test = df['sentiment']
        model.compile(optimizer='adam',
            loss=keras.losses.BinaryCrossentropy(),
            metrics=METRICS)
        model.fit(new_train, new_test, batch_size=BATCH_SIZE, epochs=EPOCHS)