import json
import re
import pandas as pd
from pymongo import MongoClient

# configuration keys
keys = json.load(open('config.json', 'r'))
# Reading Representative details from csv file 
sample_df = pd.read_csv('Involved_x_Spark_Sheet1.csv')
# Mongodb
client = MongoClient()
db = client['test']


def refine(tweet_texts: list):
    for i in range(len(tweet_texts)):
        if tweet_texts[i]:
            tweet_texts[i] = tweet_texts[i].replace('"', '')
            tweet_texts[i] = tweet_texts[i].replace('"', '')
            tweet_texts[i] = tweet_texts[i].replace("'", '')
            tweet_texts[i] = tweet_texts[i].replace('.', '')
            tweet_texts[i] = tweet_texts[i].replace('&', '')
            tweet_texts[i] = tweet_texts[i].replace(',', '')
            tweet_texts[i] = tweet_texts[i].replace('‘', '')
            tweet_texts[i] = tweet_texts[i].replace('’', '')
            tweet_texts[i] = tweet_texts[i].replace('”', '')
            tweet_texts[i] = tweet_texts[i].replace('“', '')
            tweet_texts[i] = ' '.join(filter(lambda x: 'https' not in x, tweet_texts[i].split()))
            tweet_texts[i] = ' '.join(filter(lambda x: 'http' not in x, tweet_texts[i].split()))
            tweet_texts[i] = ' '.join(filter(lambda x: '@' not in x, tweet_texts[i].split()))
            for word in filter(lambda x: x[0] == '#', tweet_texts[i].split()):
                tweet_texts[i] = tweet_texts[i].replace(word,
                                                        re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', word))
            tweet_texts[i] = tweet_texts[i].replace('#', '')
            tweet_texts[i] = tweet_texts[i].lower()
    return tweet_texts


# Scrapping and storing tweets of each representative
for index, details in sample_df.iterrows():
    print("For the User: ", details['Data Point'])
    texts = []
    checked_ids = []
    # batch_total = db[details['Data Point']].find().count()
    # csv_id = 0
    # batch_size = 3000
    # if batch_total < 3000:
    #     batch_size = batch_total

    # for batch_value in range(0, int(batch_total/batch_size)+1):
    #     print("batch value", batch_value)
    #     skip = batch_value*batch_size
    tweets = db[details['Data Point']].find(no_cursor_timeout=True)
    for tweet in tweets:
        if 'retweeted_status' in tweet:
            if tweet['retweeted_status'].get('id') not in checked_ids:
                texts.append(tweet['retweeted_status'].get('full_text'))
                checked_ids.append(tweet['retweeted_status'].get('id'))
        else:
            if tweet.get('id') not in checked_ids:
                texts.append(tweet['full_text'])
    texts = refine(texts)
    df = pd.DataFrame(texts, columns=["text"])
    csv_name = 'preprocessed_data\\' + details['Data Point'] + '_refined_tweets_.csv'
    df.to_csv(csv_name, index=False)
    tweets.close()
    # csv_id += 1
    print("Completed PreProcessing for the data of: ", details['Data Point'])
print("Pre-Processing completed!")
