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
	query =details['Data Point']
	print("Query is:", query)
	result_obj = tweepy.Cursor(api.search,q=query,since=since,until=until,geocode=geocode)
	for tweet in result_obj.items():	
		db[details['Name']].insert_one(tweet._json)
	print("Mongo insertion complete!")
print('Scrapping Job completed')
	