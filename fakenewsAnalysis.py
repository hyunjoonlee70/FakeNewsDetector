import numpy as np
import pandas as pd
import seaborn as sb
from textblob import TextBlob
import csv
import string
import time
import nltk
import os
import sys
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
import Tkinter
import tkMessageBox

# Normalize by lemmatization. Credit to:
# https://sites.temple.edu/tudsc/2017/03/30/measuring-similarity-between-texts-in-python/
lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
	return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
	return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# To reduce bias in political articles, we include these political figures to our stop words, which
# will be filtered. Optimally, we hope to include all political figures.
politicians = set(['Barack', 'Obama', 'Hilary', 'Clinton', 'Donald', 'Trump', 'Bernie', 'Sanders'])
stop_words = text.ENGLISH_STOP_WORDS.union(politicians)
TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=stop_words)
# Cosine Similarity. Credit to:
# https://sites.temple.edu/tudsc/2017/03/30/measuring-similarity-between-texts-in-python/
def cos_similarity(textlist):
	tfidf = TfidfVec.fit_transform(textlist)
	return (tfidf * tfidf.T).toarray()
# Helper function that outputs the average sentiment polarity given a dataset of
# fake news.
def fakenews_sentiment_avg(fakenews):
	articles = fakenews['text']
	fakenews_sentiment_polarity = []
	for text in articles:
		try:
			tb = TextBlob(text)
			fakenews_sentiment_polarity.append(tb.sentiment.polarity)
		except UnicodeDecodeError:
			pass
	fakenews_sentiment_polarity = np.array(fakenews_sentiment_polarity)
	avg = np.mean(fakenews_sentiment_polarity)
	std = np.std(fakenews_sentiment_polarity)
	return avg

def main():
	isItFake = False;
	inputfile = "fake.csv"
	fakenews = pd.read_csv(inputfile, encoding='latin1')
	#Drop any dataframe with null values to prevent error.
	fakenews = fakenews.dropna(how='any')

	groupby_author = fakenews.groupby('author')
	fakenews_by_author = []
	for name, group in groupby_author:
		fakenews_by_author.append(group['text'].values)
	# Filter fake news author with less than 5 articles.
	fakenews_by_author = list(filter(lambda x: len(x) >= 5, fakenews_by_author))

	with open('out.txt', 'r') as output:
		input_article = output.read().replace('\n', '')
	# Average sentiment of our fake news. If using different fakenews dataset,
	# use this helper function to get new fake_sentiment.
	# fakenews_sentiment_avg(fakenews)
	avg_fake_sentiment = 0.0709092493836

	# Separate similarity values among fake news, and similarty values between
	# fake news and our input article.
	for list_fakenews in fakenews_by_author:
		list_fakenews = np.append(list_fakenews, input_article)
		similarity_matrix = np.array(cos_similarity(list_fakenews))

		fake_similarity = []
		for x in range(0, similarity_matrix.shape[0]-1):
		    for y in range(0, similarity_matrix.shape[1]):
		    	if x > y:
		    		fake_similarity.append(similarity_matrix[x, y])

		input_similarity = np.array(similarity_matrix[0:similarity_matrix.shape[1]-1,similarity_matrix.shape[0]-1])

		# We had to come up with the threshold when detecting fake news. There wasn't a specific
		# threshold set for cosine similarity. We set our alpha to 0.5, which gave us the best
		# accuracy in our test scripts.
		if 0.5*sum(fake_similarity)/float(len(fake_similarity)) < np.mean(input_similarity) :
			t = TextBlob(input_article)
			# If it is similar and the sentiment is lower than the average sentiment of the fake news,
			# we conclude that the article is fake. Since, disinformative and biased articles generally
			# have negative sentiment polarity.
			if t.sentiment.polarity < avg_fake_sentiment:
				isItFake = True
				break
	with open('result.txt', 'w') as myfile:
		myfile.write(str(isItFake))



if __name__ == '__main__':
	main()
