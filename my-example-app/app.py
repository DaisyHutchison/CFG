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
	input_movie_name = form_data["movie"]

	results = get_movies(input_movie_name)

	#The second argument of the render_template method lets us send data into our html form
	#You can pass multiple things in - just separate them with commas
	#You can also pass in data in lists, and then pull out items from the list within the.html file itself!
	return render_template("api_example.html", movieresults=results, user_data=form_data)

def get_movies(input_movie_name):
	load_dotenv();
	api_key = os.getenv("OMDB_API_KEY")
	
	endpoint = 'http://www.omdbapi.com'
	payload = {"apikey": api_key, "s":input_movie_name}
	response = requests.get(endpoint, params=payload)

	json_data = response.json()

	#You'll see any printed data in your terminal - helpful to understand what's happening, and to debug
	print "JSON response from the API call:"
	print json_data

	return json_data["Search"]

app.run(debug=True)