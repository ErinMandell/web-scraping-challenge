# import necessary libraries
from flask import Flask, render_template
import pymongo

# create instance of Flask app
app = Flask(__name__)



# create route that renders index.html template
@app.route("/")
def scrape():
    return render_template("index.html", text="Serving up cool text from the Flask server!!")

# flask calls the echo function for us when that page is loaded.  It 
# automatically calls the index html, which then calls back to this 'text'
# the client asks for the html file, and flask honors that request by 'serving' that request

# in class we have been using 'live server' in place of flask.  live server cannot access a 
# database, but flask can


if __name__ == "__main__":
    app.run(debug=True)