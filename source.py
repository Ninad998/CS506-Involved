import json
import tweepy
import datetime
import pandas as pd
from pymongo import MongoClient

# configuration keys
keys = json.load(open('config.json','r'))

# Mongodb  
client = MongoClient()
db = client[keys['mongo_db']]
 
# Twitter API Authentication
auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True)
 
# Reading Representative details from csv file 
sample_df = pd.read_csv('Involved_x_Spark_Sheet1.csv')


# Twitter Search API Parameters
lang = 'en'
geocode = '42.35712,-71.06946,200mi'
until = datetime.datetime.today().strftime('%Y-%m-%d')
since = datetime.datetime.today()-datetime.timedelta(days=10)
since = since.strftime('%Y-%m-%d')


# Scrapping and storing tweets of each representative
for index, details in sample_df.iterrows():
	print("For the User: ", details['Data Point'])
	data_point  = details['Data Point']

	# based upon search query on twitter handle
	query = data_point
	result_obj = tweepy.Cursor(api.search,q=query,since=since,until=until,geocode=geocode)
	for tweet in result_obj.items():	
		db[details['Name']].insert_one(tweet._json)

	# based upon search query on Name
	query = details['Name']
	result_obj = tweepy.Cursor(api.search,q=query,since=since,until=until,geocode=geocode)
	for tweet in result_obj.items():	
		db[details['Name']].insert_one(tweet._json)

	# based upon users timeline (limit 3200 tweets)
	alltweets = []
	new_tweets = api.user_timeline(screen_name=data_point.replace('@',''),count=200)
	alltweets.extend(new_tweets)
	oldest = alltweets[-1].id - 1
	for tweet in new_tweets:
		db[details['Name']].insert_one(tweet._json)
	while len(new_tweets) > 0:
		new_tweets = api.user_timeline(screen_name = data_point.replace('@',''),count=200,max_id=oldest)
		for tweet in new_tweets:
			db[details['Name']].insert_one(tweet._json)
		alltweets.extend(new_tweets)
		oldest = alltweets[-1].id - 1

	print("Mongo insertion complete!")
print('Scrapping Job completed')
	