#These modules are all from flask
from flask import Flask, render_template, request
#This module is from dotenv
from dotenv import load_dotenv
#These are python provided modules
import requests, os

app = Flask("MyExampleApp")

@app.route("/")
def home_page():
	return render_template("index.html")

@app.route("/otherpage")
def other_page():
	return render_template("other_page.html")

@app.route("/apiexample", methods=["POST"])
def api_example():
	#We use the request module to easily collect all the data input into the form
	form_data = request.form
	print form_data
	input_book_name = form_data["book"]

	results = get_book(input_book_name)

	#The second argument of the render_template method lets us send data into our html form
	#You can pass multiple things in - just separate them with commas
	#You can also pass in data in lists, and then pull out items from the list within the.html file itself!
	return render_template("api_example.html", bookresults=results, user_data=form_data)

# def get_movies(input_movie_name):
# 	load_dotenv();
# 	api_key = os.getenv("OMDB_API_KEY")
	
# 	endpoint = 'http://www.omdbapi.com'
# 	payload = {"apikey": api_key, "s":input_movie_name}
# 	response = requests.get(endpoint, params=payload)

# 	json_data = response.json()

# 	#You'll see any printed data in your terminal - helpful to understand what's happening, and to debug
# 	print "JSON response from the API call:"
# 	print json_data

# 	return json_data["Search"]


def get_book (input_book_name):
	#This code will go and seach on the NYT server for a book, return some information about it
	#It will then search for the same book from Google Books, to get an image of the cover
	load_dotenv() #add the variables from the .env file to this file
	#Set up the API keys
	api_key_nyt = os.getenv( "NYT_API_KEY" ) 
	api_key_google = os.getenv( "GOOGLE_API_KEY" ) 
	#Do the NYT request
	endpoint_nyt = "https://api.nytimes.com/svc/books/v3/reviews.json?title=" + input_book_name
	payload_nyt = {"api-key" :api_key_nyt} 
	response_nyt = requests.get(endpoint_nyt, params=payload_nyt) 
	print "\n",'NYT status code:', response_nyt.status_code, "\n" 
	data_nyt = response_nyt.json()

	#Save some data about the book
	title = data_nyt["results"][0]["book_title"] #we've got a 0 in here to just return the first record
	author = data_nyt["results"][0]["book_author"]
	summary = data_nyt["results"][0]["summary"]
	isbn = data_nyt["results"][0]["isbn13"][0]
	print isbn

	#Do the Google request
	endpoint_google = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn #where the data is that we want to fetch
	payload_google = {"api-key" :api_key_google} 
	response_google = requests.get(endpoint_google, params=payload_google) 
	print "\n" ,'Google status code: ',response_google.status_code, "\n" 
	data_google = response_google.json()
	thumbnail = data_google["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"] #Get the image of the book
	print thumbnail
	print data_google
	print author
	return data_google["Author"]


@app.route("/<name>")
def hello_someone(name):
    return render_template("mail.html")

@app.route("/signup", methods=["POST"])
def sign_up():
    form_data = request.form
    print form_data["email"]
    
    name1 = request.form.get('genre1')
    if name1:
        print form_data["genre1"]

    name2 = request.form.get('genre2')
    if name2:
        print form_data["genre2"]

    name3 = request.form.get('genre3')
    if name3:
        print form_data["genre3"]

    name4 = request.form.get('genre4')
    if name4:
        print form_data["genre4"]

    name5 = request.form.get('genre5')
    if name5:
        print form_data["genre5"]

    name6 = request.form.get('genre6')
    if name6:
        print form_data["genre6"]

    print form_data["frequency"]
    return render_template("submit.html")

app.run(debug=True)