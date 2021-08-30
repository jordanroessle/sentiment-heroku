# Dependencies
# ----------------------------------
from flask import Flask, render_template, redirect, jsonify, request
from flask import send_from_directory
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, update, Table
from sqlalchemy.orm import Session
from datetime import datetime
from modelPredict import predictModel
import tweet
import database


# initialize flask
app = Flask(__name__)

# Create database connection String
rds_connection_string = "postgres:postgres@localhost:5432/sentiment_db"
engine = create_engine(f'postgresql://{rds_connection_string}')

metadata = MetaData(engine)
tweet_data = Table('tweet_data', metadata, autoload=True, autoload_with=engine)

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
	conn = engine.connect()
	session = Session(bind=engine)
	available_tweets = session.query(tweet_data).filter(tweet_data.c.sentiments == 9).count()
	session.close()
	print(available_tweets)
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
	conn.execute(update_db)

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
	
	# Create connection to SQL database
	conn = engine.connect()

	# Create object update
	tweet_update = (
		update(tweet_data).
		where(tweet_data.c.id == tweet_dict['id']).
		values(sentiments=tweet_dict['sentiments'], time_data_inserted=tweet_dict['time_data_inserted'])
	)
	conn.execute(tweet_update)
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
	conn.execute(tweet_update)
	return {}

@app.route("/data")
def datacalled():
	session = Session(bind=engine)
	vals = session.query(tweet_data).filter(tweet_data.c.sentiments != 9).all()
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
