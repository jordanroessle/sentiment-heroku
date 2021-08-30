import pandas as pd
from sqlalchemy import create_engine
import sklearn
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords 
from tensorflow.keras.models import load_model
from sklearn.metrics import confusion_matrix
import seaborn as sns
from tensorflow import keras
import string
import re
from sklearn.preprocessing import Normalizer
import pickle

vectorizer = TfidfVectorizer()
tfidf_vect = TfidfVectorizer()
wn = nltk.WordNetLemmatizer()
string.punctuation
stop = stopwords.words('english')

rds_connection_string = "postgres:postgres@localhost:5432/sentiment_db"
engine = create_engine(f'postgresql://{rds_connection_string}')

df = pd.read_sql_query('select * from sentiment_data', con=engine).iloc[np.random.choice(np.arange(50000), 5000, False)]

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
    final_df['sentiments'] = df['sentiments']
    final_df['joined_lemm'] = df['joined_lemm']
    return final_df

clean_df = lema(df,'text')

x = clean_df['joined_lemm']
y = clean_df['sentiments']
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, test_size=0.2)
vectorizer = TfidfVectorizer()
vectorizer.fit(X_train)
vectorized_train = vectorizer.transform(X_train).toarray()
vectorized_test = vectorizer.transform(X_test).toarray()
vectorized_val = vectorizer.transform(X_val).toarray()
norm = Normalizer().fit(vectorized_train)
norm_vectorized_train = norm.transform(vectorized_train)
norm_vectorized_test = norm.transform(vectorized_test)
norm_vectorized_val = norm.transform(vectorized_val)

pickle.dump(vectorizer, open("vectorizer.pickle", "wb"))

train_labels = np.array(y_train)
bool_train_labels = train_labels != 0
val_labels = np.array(y_val)
test_labels = np.array(y_test)

train_features = norm_vectorized_train
val_features = norm_vectorized_val
test_features = norm_vectorized_test

train_features = np.clip(train_features, -5, 5)
val_features = np.clip(val_features, -5, 5)
test_features = np.clip(test_features, -5, 5)

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

EPOCHS = 50
BATCH_SIZE = 2048

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_prc', 
    verbose=1,
    patience=10,
    mode='max',
    restore_best_weights=True)

    
def make_model(metrics=METRICS, output_bias=None):
    if output_bias is not None:
        output_bias = tf.keras.initializers.Constant(output_bias)
    model = keras.Sequential([
        keras.layers.Dense(
            16, activation='relu',
            input_shape=(train_features.shape[-1],)),
        keras.layers.Dense(50, activation='relu'),
        keras.layers.Dense(50, activation='relu'),
        keras.layers.Dropout(0.5),

        keras.layers.Dense(1, activation='sigmoid',
                         bias_initializer=output_bias),
  ])

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss=keras.losses.BinaryCrossentropy(),
        metrics=metrics)

    return model

model = make_model()
baseline_history = model.fit(
    train_features,
    train_labels,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=(val_features, val_labels),
    callbacks=[early_stopping])

model.save("deep_sentiment_model_trained_zenith.h5", save_format='tf')