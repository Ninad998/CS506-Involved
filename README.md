# CS506 Involved

The Project is for Involved - Data Analysis.  The Application analyse the trend in the social media data over the political issues and political representative,
to deduce the most important current issue in the society of a constituency.  
We are working on this project as a part of the Course Project of CS506 - Tools of Data Science, Fall 2018, Computer Science Department, Boston University

## Getting Started

We are trying to address following questions:  
1.	How do we collect tweets from the Massachusetts area and find “Hot Topics” of this area directed to a specific representative?  
2.	Which political topics are being discussed most frequently on social media in the Boston area?  
3.	What are the most popular Boston 311 issues raised by the public, by who and where, and to whom?  
4.	How do we pair the census data and Involved poll data?  

*Development:*

- The configuration keys of Twitter API must be kept in `config.json`.  
	Parameters:  
	* consumer_key
	* consumer_secret
	* access_token
	* access_token_secret  
	*NOTE: **Never** push the API keys to the Repo.*  
- To get the Twitter Data for different representative:
	- Run the source.py 

TBC 

### Prerequisites

* Tech Stack:
	- **Python 3.6**
	- **Mongodb**
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


## Deployment

TBD

## Built With

* [Tweepy](http://docs.tweepy.org/en/v3.5.0/) - Twitter API accessing Library
* [MongoDB](https://www.mongodb.com/) - NoSQL Database for storage

## Contributors

* Ninad Tungare
* Harshad Reddy Nalla
