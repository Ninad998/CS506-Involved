import os
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
stop_words = stopwords.words('english') + list(punctuation)


def tokenize(text):
    words = word_tokenize(text)
    words = [w.lower() for w in words]
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
        print(filename)
        try:
            dictionary = HashDictionary()
            temp_name = 'preprocessed_data\\' + str(filename)
            if os.path.isfile(temp_name):
                list_of_text = pd.read_csv(temp_name)['text'].values.tolist()
                list_of_text = [tokenize(text) for text in list_of_text]
                dictionary.add_documents(list_of_text)

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

            sorted_x = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
            freq_df = pd.DataFrame(sorted_x, columns=['words', 'weights'])
            freq_df.to_csv('weights//' + str(filename.split('_')[0]) + '.csv', index=False)

            wc = WordCloud(
                background_color="white",
                max_words=2000,
                width=1024,
                height=720,
                stopwords=stopwords.words("english")
            )

            wc.generate_from_frequencies(freq)
            wc.to_file("word_clouds//" + str(filename.split('_')[0]) + ".png")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    analyse()
