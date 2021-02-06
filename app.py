from flask import Flask, render_template, redirect
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer 
import random

# Loading the bag of soup dataframe
main_df = pd.read_csv("big_movies_csv/the_main_df.csv")

# Turning the bag_of_words into a matrix
count = CountVectorizer()
count_matrix = count.fit_transform(main_df['bag_of_words'])
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# Turning title column into a series
indices = pd.Series(main_df['title'])

# Create the equation function
def recommend(title, cosine_sim = cosine_sim):
    
    recommended_movies = []
    idx = indices[indices == title].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_10_indices = list(score_series.iloc[1:11].index)
    
    for i in top_10_indices:
        recommended_movies.append(list(main_df['title'])[i])
        
    return recommended_movies

app = Flask(__name__)

@app.route("/")
def index():
	all_movies = main_df.to_json(orient='index') 
	return render_template("index.html", all_movies=all_movies)

@app.route("/random")
def random_movie():
    x = random.randint(0, len(main_df))
    single_movie = main_df['title'][x]

    recommend_list = recommend(single_movie)

    return render_template("title.html", recommend_list=recommend_list, title=single_movie)

@app.route("/title/<title>")
def title(title):

	# First we want to make sure the title exists in the dataset

	if len(main_df.loc[main_df['title']==title, :]) > 0:
		recommend_list = recommend(title)
	else:
		# See if we can locate similar titles
		title_result = main_df[main_df['title'].str.contains(title, case=False)]
		recommend_list = title_result['title'].values.tolist()
		title = "Couldn't Locate '" + title + "'. We Did Find:"

	return render_template("title.html", recommend_list=recommend_list, title=title)

if __name__ == "__main__":
	app.run(debug=True)