import os.path
import pandas as pd

from nltk import word_tokenize
from nltk.corpus import stopwords
from string import punctuation

from gensim.corpora import HashDictionary
from gensim.models import TfidfModel, LsiModel

from wordcloud import WordCloud

list_of_files = "after_test_*.csv"

stop_words = stopwords.words('english') + list(punctuation)

print(stopwords)


def tokenize(text):
    words = word_tokenize(text)
    words = [w.lower() for w in words]
    return [w for w in words if w not in stop_words and not w.isdigit()]


i = 0

dictionary = HashDictionary()

while (True):
    temp_name = list_of_files.replace("*", str(i))

    if os.path.isfile(temp_name):
        print("here")
        list_of_text = pd.read_csv(temp_name)['text'].values.tolist()
        list_of_text = [tokenize(text) for text in list_of_text]
        dictionary.add_documents(list_of_text)
    else:
        break

list_of_text = pd.read_csv(temp_name)['text'].values.tolist()
list_of_text = [tokenize(text) for text in list_of_text]

vectors = [dictionary.doc2bow(text) for text in list_of_text]

tfidf = TfidfModel(vectors)

weights = tfidf[vectors]

freq = dict()
for doc in weights:
    for pair in doc:
        list_of_words = list(dictionary[pair[0]])
        for word in list_of_words:
            if word in freq:
                freq[word] += pair[1]
            else:
                freq[word] = pair[1]

print(freq)

# wc = WordCloud(
#     background_color="white",
#     max_words=2000,
#     width = 1024,
#     height = 720,
#     stopwords=stopwords.words("english")
# )

# wc.generate_from_frequencies(freq)

# wc.to_file("word_cloud.png")
