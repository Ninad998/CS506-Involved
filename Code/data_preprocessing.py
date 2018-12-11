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
db = client[keys['mongo_db']]
r = re.compile('^\w+$')


def refine(tweet_texts: list, details):
    name = details['Name'].lower()
    name = name.split()
    handle = details['Data Point'].replace('@', '')
    name.append(handle)
    for i in range(len(tweet_texts)):
        if tweet_texts[i]:
            not_required = ['"', '"', "'", '.', '&', ',', '‘', '’', '”', '“', '#']
            for nr in not_required:
                tweet_texts[i] = tweet_texts[i].replace(nr, '')

            tweet_texts[i] = ' '.join(filter(lambda x: 'https' not in x, tweet_texts[i].split()))
            tweet_texts[i] = ' '.join(filter(lambda x: 'http' not in x, tweet_texts[i].split()))
            tweet_texts[i] = ' '.join(filter(lambda x: '@' not in x, tweet_texts[i].split()))
            for word in filter(lambda x: x[0] == '#', tweet_texts[i].split()):
                tweet_texts[i] = tweet_texts[i].replace(word,
                                                        re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', word))

            for word in tweet_texts[i].split():
                if not re.match(r, word):
                    tweet_texts[i] = tweet_texts[i].replace(word, '')

            tweet_texts[i] = tweet_texts[i].lower()

            for name_part in name:
                tweet_texts[i] = tweet_texts[i].replace(name_part, '')

    return tweet_texts


# Scrapping and storing tweets of each representative
for index, details in sample_df.iterrows():
    print("For the User: ", details['Data Point'])
    texts = []
    checked_ids = []
    tweets = db[details['Data Point']].find({}, no_cursor_timeout=True)
    for tweet in tweets:
        if 'retweeted_status' in tweet:
            if tweet['retweeted_status'].get('id') not in checked_ids:
                texts.append(tweet['retweeted_status'].get('full_text'))
                checked_ids.append(tweet['retweeted_status'].get('id'))
        else:
            if tweet.get('id') not in checked_ids:
                texts.append(tweet['full_text'])
    texts = refine(texts, details)
    texts = [text for text in texts if text]
    df = pd.DataFrame(texts, columns=["text"])
    csv_name = 'preprocessed_data\\' + details['Data Point'] + '_refined_tweets_.csv'
    df.to_csv(csv_name, index=False)
    tweets.close()
    print("Completed PreProcessing for the data of: ", details['Data Point'])
print("Pre-Processing completed!")
