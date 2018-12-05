import os
import random
import operator
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from string import punctuation
from gensim.corpora import HashDictionary
from gensim.models import TfidfModel
from wordcloud import WordCloud

# Global Variable
custom_stop_words = [word for line in open('custom_stop_words', 'r') for word in line.split(',')]
stop_words = stopwords.words('english') + list(punctuation) + custom_stop_words


def consider_acronyms(weighted_words):
    acr = pd.read_csv("Common Acronyms - Sheet1.csv")
    acr = acr.dropna()
    for w in acr['Acronym'].str.lower():
        if w in weighted_words.keys():
            weighted_words[w] = max(weighted_words.values()) - random.uniform(1, 5)
            weighted_words[acr.loc[acr['Acronym'] == w.upper(), 'Definition'].iloc[0]] = weighted_words[w]
            del weighted_words[w]
    return weighted_words


def tokenize(text):
    words = word_tokenize(text)
    words = [w.lower() for w in words]
    words = [w for w in words if w not in custom_stop_words]
    words = [w for w in words if w not in stop_words and not w.isdigit()]

    # Stemming
    # stem = PorterStemmer()
    # words = [stem.stem(w) for w in words]

    # Lemmatization
    wnl = WordNetLemmatizer()
    words = [wnl.lemmatize(w) for w in words]

    return words


def analyse():
    for filename in os.listdir('preprocessed_data'):
        try:
            print("Working on: ", filename)
            dictionary = HashDictionary()
            temp_name = 'preprocessed_data\\' + str(filename)
            if os.path.isfile(temp_name):
                list_of_text = pd.read_csv(temp_name)['text'].values.tolist()
                list_of_text = [tokenize(text) for text in list_of_text]
                dictionary.add_documents(list_of_text)

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

            freq = consider_acronyms(freq)
            sorted_x = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
            freq_df = pd.DataFrame(sorted_x, columns=['words', 'weights'])
            freq_df.to_csv('weights//' + str(filename.split('_')[0]) + '.csv', index=False)

            wc = WordCloud(
                background_color="white",
                max_words=2000,
                width=1024,
                height=720,
                stopwords=stop_words
            )

            wc.generate_from_frequencies(freq)
            wc.to_file("word_clouds//" + str(filename.split('_')[0]) + ".png")
        except Exception as e:
            print("Broken File", filename)
            print(e)


if __name__ == "__main__":
    analyse()