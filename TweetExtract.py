from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import pandas as pd
import csv
import re #regular expression
from textblob import TextBlob
import string
import preprocessor as p
from pathlib import Path


class TweetExtract:

	#declare file paths as follows for three files
	storage_dir = "./data/"

	#columns of the csv file
	COLS = ['id', 'created_at', 'source', 'original_text','clean_text', 'sentiment','polarity',
	'subjectivity', 'lang','favorite_count', 'retweet_count', 'original_author',
	'possibly_sensitive', 'hashtags','user_mentions', 'place', 'place_coord_boundaries']

	#HappyEmoticons
	emoticons_happy = set([':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD',
		'=-D', '=D','=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P',
		':P', 'X-P','x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)',
		'>;)', '>:-)','<3'])
	# Sad Emoticons
	emoticons_sad = set([':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', 
		':<',':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
		':c', ':{', '>:\\', ';('])

	#Emoji patterns - emoticons, symbols, transport and map symbols, and flags (iOS)
	emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"
	u"\U0001F300-\U0001F5FF"
	u"\U0001F680-\U0001F6FF"
	u"\U0001F1E0-\U0001F1FF"
	u"\U00002702-\U000027B0"
	u"\U000024C2-\U0001F251"
	"]+", flags=re.UNICODE)

	#combine sad and happy emoticons
	emoticons = emoticons_happy.union(emoticons_sad)

	my_topic = ""

	def __init__(self,topic):
		#Twitter credentials for the app
		my_keys = self.getKeys()
		try:
			consumer_key = my_keys['consumer_key']
			consumer_secret = my_keys['consumer_secret']
			access_key= my_keys['access_key']
			access_secret = my_keys['access_secret']
		except:
			print("Credential fetch failed. Please ensure that the file is correctly formatted")
			raise SystemExit
			
		my_topic = topic

	def write_tweets():
		#TODO - Add the function to load and store the actual tweeets as a CSV
		#pass twitter credentials to tweepy
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_key, access_secret)
		api = tweepy.API(auth)

		my_filename = self.my_topic+"_data.csv"
		my_tweet_csv = self.storage_dir+my_filename
		self.download_tweets(my_tweet_csv)

	def download_tweets(csv_dir):
		print("Loading data connected to#{} to the directory{}".format(self.my_topic, csv_dir))

	def getKeys(self):
		my_keys = {}
		path = "./my_credentials.json"
		config = Path(path)
		if config.is_file():
			with open(path) as json_file:
				data = json.load(json_file) 
				for key,value in data.items():
					my_keys[key] = value
			return my_keys
		else:
			print("Credential fetch failed. Please ensure that a my_credentials.json file exists in the source directory of this project")
			raise SystemExit

