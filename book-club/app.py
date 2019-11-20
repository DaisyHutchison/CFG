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

@app.route("/results", methods=["POST"])
def api_example():
    form_data = request.form
    input_book_name = form_data["book"]
    data_nyt = get_nyt_data(input_book_name)
    title = data_nyt["results"][0]["book_title"]
    author = data_nyt["results"][0]["book_author"]
    summary = data_nyt["results"][0]["summary"]
    isbn = data_nyt["results"][0]["isbn13"][0]
    thumbnail = get_thumbnail(isbn)
    return render_template("results.html", thumbnail=thumbnail, user_data=form_data, author=author, title=title, summary=summary)

def get_nyt_data(input_book_name):
    load_dotenv()
    api_key_nyt = os.getenv("NYT_API_KEY") 
    endpoint_nyt = "https://api.nytimes.com/svc/books/v3/reviews.json?title=" + input_book_name
    payload_nyt = {"api-key" :api_key_nyt} 
    response_nyt = requests.get(endpoint_nyt, params=payload_nyt) 
    print "\n",'NYT status code:', response_nyt.status_code, "\n" 
    data_nyt = response_nyt.json()
    print "\n",'DATA NYT:', data_nyt, "\n"
    return data_nyt

def get_thumbnail(isbn):
    load_dotenv()
    api_key_google = os.getenv("GOOGLE_API_KEY")
    endpoint_google = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn
    payload_google = {"api-key" :api_key_google} 
    response_google = requests.get(endpoint_google, params=payload_google) 
    print "\n" ,'Google status code: ',response_google.status_code, "\n" 
    data_google = response_google.json()
    thumbnail = data_google["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
    print "\n",'THUMBNAIL:',thumbnail, "\n"
    print "\n",'DATA GOOGLE:',data_google, "\n"
    return thumbnail


@app.route("/mail")
def mail():
    return render_template("mail.html")



@app.route("/signup", methods=["POST"])
def sign_up():
    form_data = request.form
    email = form_data["email"]
    send_email(email)
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
    return render_template("submit.html", email=email)


def send_email(user_email):
    endpoint = "https://api.mailgun.net/v3/sandbox852093c7507144d8b5decbf5653807fb.mailgun.org/messages"
    api_key = os.getenv("MAILGUN_API_KEY")
    return requests.post(
        endpoint,
        auth=("api", api_key),
        data={"from": "Book Club <mailgun@sandbox852093c7507144d8b5decbf5653807fb.mailgun.org>",
              "to": [user_email],
              "subject": "Welcome to Book Club!",
              "text": "Thank you for joining our newsletter! Watch out for some awesome book recommendations coming to your inbox soon!"})
    


app.run(debug=True)