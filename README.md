# Data Analyses for Involved
The Project is for Involved - Data Analysis.  The Application analyse the trend in the social media data over the political issues and political representative,
to deduce the most important current issue in the society of a constituency.  
We are working on this project as a part of the Course Project of CS506 - Tools of Data Science, Fall 2018, Computer Science Department, Boston University

## Getting Started

We are trying to address following questions:  
1.	How do we collect tweets from the Massachusetts area and find “Hot Topics” of this area directed to a specific representative?  
2.	Which political topics are being discussed most frequently on social media in the Boston area?  
3.	What are the most popular Boston 311 issues raised by the public, by who and where, and to whom?  
4.	How do we pair the census data and Involved poll data?  

*How to Run:*

- The configuration keys of Twitter API must be kept in `config.json`.  
	Parameters:  
	* consumer_key
	* consumer_secret
	* access_token
	* access_token_secret  
	* mongo_db  
	*NOTE: **Never** push the API keys to the Repo.*  
- To get the Twitter Data for different representative:
	- Run the '[source.py](Code/source.py)' with config.json containing appropriate Twitter API Keys and a csv file
	named [Involve_x_Spark_Sheet1.csv](Code/Involved_x_Spark_Sheet1.csv) containing Name(Twitter Handle Name) and Data Point(Twitter Handle).  
- To generate the word cloud from the Twitter data collected:
    - First run the '[data_preprocessing.py](Code/data_preprocessing.py)' to clean the data.
    - Then run the '[train.py](Code/train.py)' to analyse and generate word clouds.
        - Provide common acronyms to map them within analyse data by passing acronyms in csv file "[Common Acronyms](Code/Common%20Acronyms%20-%20Sheet1.csv)".
        
- To run the Boston 311 analyses:
    - Execute "[Boston 311.ipynb](Code/Boston%20311.ipynb)"  jupyter notebook with Boston Data "[311.csv](https://data.boston.gov/dataset/311-service-requests)".
    - The Boston 311 dataset is readily available at [Boston 311](https://data.boston.gov/dataset/311-service-requests) for download.

*Files Description:*

- [source.py](Code/source.py): Application to collected/scrape data from Twitter for handle given in [Involved Dataset](Code/Involved_x_Spark_Sheet1.csv) based upon certain criteria:
    * Twitter: Given a Twitter handle/name we collect 4
types of tweets per handle:
        1. Tweets sent by the handle
        2. Tweets/comments on the tweets sent by the handle
        3. Tweets which mention the account
        4. Tweets which are comments and mentions the account
    
- [Involved Dataset](Code/Involved_x_Spark_Sheet1.csv): CSV Dataset containing Twitter Handle for which data has to be collected. Columns:Name,Data Point.
- [Config.json](Code/config.json): configuration key json files which should contain twitter api keys such as consumer_key,consumer_secret,access_token,access_token_secret and mongo_db.
- [Data_Preprocessing.py](Code/data_preprocessing.py): Application to clean the twitter data collected by performing various necessary actions.
- [Train.py](Code/train.py): Application to run Tf-idf word weight analyses and generate word cloud for the twitter data.
- [Common acronym](Code/Common%20Acronyms%20-%20Sheet1.csv): CSV Dataset contain common acronym which are to be replaced in word weight with there expansion.
- [Custom Stop word](Code/custom_stop_words): Text files containing word which are to be neglected from word tokens while performing Tf-idf word weights analyses.
- [Boston 311 analyses](Code/Boston%20311.ipynb): Jupyter Notebook using Boston 311 Data [311.csv](https://data.boston.gov/dataset/311-service-requests) to perform analysis and generate various visualizations. 
- [Presentation Notebook](Code/presentation_script.ipynb): Jupyter Notebook with proper explanation and few example for each analyses performed in the project.

### Prerequisites

* Tech Stack:
	- **Python 3.6**
	- **Mongodb**
	- **Gensim**
	- **Nltk**
	- **Wordcloud**
	- **Folium**
	- **Plotly**
* Clone the Project  
* Setup a Virtual Environment for Development:
	- Install Python Virtualenv:    
		`pip install virtualenv`  
	- In Windows:    
        `virtualenv venv`   
        `venv\Scripts\activate`   
    - In Mac and Linux:  
        `virtualenv venv`  
        `source venv/bin/activate`
* Install the requirement packages:  
	`pip install -r requirements.txt`

## Built With

* [Tweepy](http://docs.tweepy.org/en/v3.5.0/) - Twitter API accessing Library
* [MongoDB](https://www.mongodb.com/) - NoSQL Database for storage
* [Pandas](https://pandas.pydata.org/) - Pandas Dataframe for data processing 
* [Gensim](https://pypi.org/project/gensim/) - Gensim for Tf-IDF model
* [Nltk](https://www.nltk.org/) - nltk for Word tokenizer
* [Folium](https://python-visualization.github.io/folium/) - Visualization tool
* [Plotly](https://plot.ly/) -Visualization analytics in graphs

## Contributors

* [Ninad Tungare](https://github.com/Ninad998)
* [Harshad Reddy Nalla](https://github.com/harshad16)

## Acknowledgment

* Prof Andrei Lapets (Boston University)
* Caleb McDermott (Involved)
* BU Spark (Boston University)