"""

    Simple Streamlit webserver application for serving developed classification
	models.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within this directory for guidance on how to use this script
    correctly.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend the functionality of this script
	as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies

import streamlit as st
import joblib, os
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

#
from PIL import Image

# Data dependencies
import pandas as pd
import  numpy as np

#NLP Pkgs
from PIL import Image

from nltk import pos_tag
import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
#import spacy
#nlp=TextBlob.load("en")

# Vectorizer
news_vectorizer = open("resources/vect_CountVector(1).pkl","rb")
tweet_cv = joblib.load(news_vectorizer) # loading your vectorizer from the pkl file

# Load your raw data
raw = pd.read_csv("resources/train.csv")

#load our models here
def get_keys(val,my_dict):
	for key,value in my_dict.items():
		if val == value:
			return key
# The main function where we will build the actual app
def main():
	"""Tweet Classifier App with Streamlit """

	# Creates a main title and subheader on your page -
	# these are static across all pages
	st.title("Tweet Classifer")
	st.subheader("Climate change tweet classification")

	# Creating sidebar with selection box -
	# you can create multiple pages this way
	options = ["Prediction", "Information","Visuals"]
	selection = st.sidebar.selectbox("Choose Option", options)
   
	# Building out the "Information" page
	if selection == "Information":
		st.info("General Information")


		# You can read a markdown file from supporting resources folder
	
		st.markdown("Climate change is already and is going to continue to be the issue (crisis) of our time. The coronavirus pandemic has only further highlighted just how massive of an issue climate change is going to become in the next few decades.")
		st.markdown("Thus, businesses looking to grow and succeed in this new normal, and in a turbulent economic environment, need to be acutely aware of the causes and symptoms of climate change. ")
		st.markdown("This can be done by better understanding the sentiment of people in general towards climate change. Essentially if companies can effectively tailor their marketing and branding efforts to suit their audience then it could bode very well for their business sustainability and ensure they grow a loyal customer base.")

		st.subheader("Raw Twitter data and label")
		if st.checkbox('Show raw data'): # data is hidden if box is unchecked
			st.write(raw[['sentiment', 'message']]) # will write the df to the page

	# Building out the predication page
	if selection == "Prediction":
		st.info("Prediction with ML Models")
		# Creating a text box for user input

		all_ml_model=["LogisticRegression","Naive_Bayes"]
		tweet_text = st.text_area("Enter Text","Type Here")
		model_choice=st.selectbox("Choose ML Model",all_ml_model)
		prediction_labels={"Do not believe":-1,"believe but Neutral":0,"Believe":1,"Strongly Believe":2}
		

		if st.button("Classify"):
			# Transforming user input with vectorizer
			vect_text = tweet_cv.transform([tweet_text]).toarray()
			if model_choice =="LogisticRegression":
				predictor=joblib.load(open(os.path.join("resources/logreg(1).pkl"),"rb"))
				prediction = predictor.predict(vect_text)
				st.write(prediction)
				final_result=get_keys(prediction,prediction_labels)
			if model_choice =="Naive_Bayes":
				predictor=joblib.load(open(os.path.join("resources/naive_bayes (1).pkl"),"rb"))
				prediction = predictor.predict(vect_text)
				st.write(prediction)
				final_result=get_keys(prediction,prediction_labels)
			#vect_tweet = tweet_cv.sklearn.transform(tweet_text).toarray()
			# Load your .pkl file with the model of your choice + make predictions
			# Try loading in multiple models to give the user a choice
			#predictor = joblib.load(open(os.path.join("resources/logreg(1).pkl"),"rb"))
			#prediction = predictor.predict(vect_text)

			# When model has successfully run, will print prediction
			# You can use a dictionary or similar structure to make this output
			# more human interpretable.
			st.success("Text Categorized as: {}".format(get_keys(prediction,prediction_labels)))
          #building the section for Natural processing space

	if	selection == "Visuals":
		st.markdown("The visual below show our EDA in this project")
		st.markdown("wordcloud show the most frequest word used in the text")
		image=Image.open('resources/imgs/wordcloud.png')
		st.image(image,caption='caption below image')

		st.markdown("The bargraph below show the most frequest Hashtags in the tweet")
		image=Image.open('resources/imgs/frequent_hashtags.png')
		st.image(image,caption='caption below imgae')

		st.markdown("THOSE WHO STRONGLY BELIEVE ")
		image=Image.open('resources/imgs/hashtag_sentiment_two.png')
		st.image(image,caption='caption below imgae')

		st.markdown("THOSE WHO DO NOT BELIEVE ")
		image=Image.open('resources/imgs/hashtags_sentiment_neg.png')
		st.image(image,caption='caption below imgae')


# Required to let Streamlit instantiate our web app.  
if __name__ == '__main__':
	main()
