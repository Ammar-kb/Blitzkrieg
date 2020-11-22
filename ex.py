from tkinter import *    
from tkinter import messagebox
import webbrowser
import os    
import pandas as pd
import numpy as np
import wikipedia
import datetime
import wolframalpha
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

root = Tk()
root.geometry("810x570")
photo = PhotoImage(file="nf.png")
root.configure(background="Black")
label = Label(root,image = photo)
label.pack()
global movie_user_likes
Label(root,bg = "black",text = "").pack()
Label(root,bg = "black",fg= "white",text = "Enter the Movie Name: ").pack(side = "top")

movie = StringVar()
movie1 =  Entry(root,textvariable = movie).pack()
global sorted_similar_movies
global similar_movies
global movie_index
global movie_user_likes
###### helper functions. Use them when needed #######
def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]
##################################################

##Step 1: Read CSV File
df = pd.read_csv("movie_dataset.csv")
#print df.columns
##Step 2: Select Features

features = ['keywords','cast','genres','director']
##Step 3: Create a column in DF which combines all selected features
for feature in features:
	df[feature] = df[feature].fillna('')

def combine_features(row):
	try:
		return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]
	except:
		print ("Error:", row)	

df["combined_features"] = df.apply(combine_features,axis=1)

#print "Combined Features:", df["combined_features"].head()

##Step 4: Create count matrix from this new combined column
cv = CountVectorizer()

count_matrix = cv.fit_transform(df["combined_features"])

##Step 5: Compute the Cosine Similarity based on the count_matrix
cosine_sim = cosine_similarity(count_matrix)
def act():
    movie_user_likes = movie.get()
    
    
## Step 6: Get index of this movie from its title
    movie_index = get_index_from_title(movie_user_likes)

    similar_movies =  list(enumerate(cosine_sim[movie_index]))

## Step 7: Get a list of similar movies in descending order of similarity score
    sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)
    
## Step 8: Print titles of first 50 movies
    i=0
    for element in sorted_similar_movies:
                    print (get_title_from_index(element[0]))
                    i=i+1
                    if i>5:
                            break
    
    root = Tk()
    root.geometry("300x300")
    root.configure(background= "Black")
    root.title("Movie Recommendation System")
    label = Label(text = "Zaboosh Movie Recom", bg= "black" , height="3", width = "45",fg= "white",font = ('Helvetica ',14)).pack()
    Label(root,text="",bg = "black",fg = "white").pack()
    listbox = Listbox(root)
    listbox.pack()
    i=0
    for element in sorted_similar_movies:
        listbox.insert(0,get_title_from_index(element[0]))
        i=i+1    
        if i>5:
                break
        
    string = movie.get()
    if (' Avatar' or 'Spectre' )in string:
            webbrowser.open('www.google.co.in')

    elif (' John Carter' or 'Tangled' )in string:
            webbrowser.open('www.google.co.in')
            
    results = wikipedia.summary(string, sentences=2)
    print(' ')
    print('WIKIPEDIA says - ')
    print(results)
		
Label(root,bg = "black",text = "").pack()
a = Button(text="Submit",height="1", width='20',command = act).pack()
Label(root,bg = "black",text = "").pack()
root.mainloop()
