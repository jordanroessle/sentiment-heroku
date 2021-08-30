# Dependencies
# ----------------------------------
import os
from flask import Flask, render_template, redirect, jsonify, request
from flask import send_from_directory
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, update, Table
from sqlalchemy.orm import Session
from datetime import datetime
from modelPredict import predictModel
from sqlalchemy import Column, Integer, String, Float, SmallInteger, Date
import tweet

# initialize flask
app = Flask(__name__)

# Create database connection String
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

tweet_data = Table(
        'tweet_data', 
        Column('id', String, primary_key = True), 
        Column('tweet', String), 
        Column('sentiments', SmallInteger),
        Column('predicted_sentiments', Float),
        Column('time_data_inserted', Date) 
    )

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/voting")
def voting():
	return render_template("voting.html")

@app.route("/stats")
def statistics():
	return render_template("statistics.html")

@app.route("/load_tweet")
def load_tweet():
	available_tweets = db.session.query(tweet_data).filter(tweet_data.c.sentiments == 9).count()
	db.session.close()
	
	if available_tweets == 0:
		tweet.api_call()

	df = pd.read_sql_query('select * from tweet_data WHERE tweet_data.sentiments = 9', con=conn)
	df = df.iloc[0]
	
	tweet_dict = {
		"id":df['id'],
		"tweet":df['tweet'],
		"sentiments":int(df['sentiments']),
		"predicted_sentiments":df["predicted_sentiments"],
		"time_data_inserted":df['time_data_inserted']
	}

	tweet_dict['predicted_sentiments'] = predictModel(tweet_dict['tweet'])

	update_db = (
		update(tweet_data).
		where(tweet_data.c.id == tweet_dict['id']).
		values(predicted_sentiments=tweet_dict['predicted_sentiments'])
	)
	db.session.execute(update_db)
	db.session.commit()

	return jsonify(tweet_dict)


@app.route("/positive_update", methods = ['POST'])
def positive_update():
	# Try to grab values, will catch if someone clicks on face before a tweet loads
	try:
		tweet_dict = {
			"id": request.form['id'],
			"tweet": request.form['tweet'],
			"sentiments": 1,
			"predicted_sentiments": request.form["predicted_sentiments"],
			"time_data_inserted": datetime.now()
		}
	except:
		return {}

	# Create object update
	tweet_update = (
		update(tweet_data).
		where(tweet_data.c.id == tweet_dict['id']).
		values(sentiments=tweet_dict['sentiments'], time_data_inserted=tweet_dict['time_data_inserted'])
	)
	
	db.session.execute(tweet_update)
	db.session.commit()	
	return {}

@app.route("/negative_update", methods = ['POST'])
def negative_update():
	# Try to grab values, will catch if someone clicks on face before a tweet loads
	try:
		tweet_dict = {
			"id": request.form['id'],
			"tweet": request.form['tweet'],
			"sentiments": 0,
			"predicted_sentiments": request.form["predicted_sentiments"],
			"time_data_inserted": datetime.now()
		}
	except:
		return {}

	# Create connection to SQL database
	conn = engine.connect()
	
	# Create object update
	tweet_update = (
		update(tweet_data).
		where(tweet_data.c.id == tweet_dict['id']).
		values(sentiments=tweet_dict['sentiments'], time_data_inserted=tweet_dict['time_data_inserted'])
	)
	db.session.execute(tweet_update)
	db.session.commit()	
	return {}

@app.route("/data")
def datacalled():
	vals = db.session.query(tweet_data).filter(tweet_data.c.sentiments != 9).all()
	db.session.close()
	data_list = []
	holder = len(vals)
	for i in range(holder):
		data_list.append({
            'id': vals[i][0],
			'tweet': vals[i][1],
			'sentiments': vals[i][2],
			'predicted_sentiments': vals[i][3],
			'date': vals[i][4],
		})

	return jsonify(data_list)

if __name__ == "__main__":
	app.run(debug=True)
