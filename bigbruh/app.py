import os
#Credit to Harvard's CS 50 Class
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

#credit to Abdul Majed Raja
#https://datascienceplus.com/natural-language-generation-with-markovify-in-python/
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import markovify #Markov Chain Generator

from helpers import apology

#API_KEY
#pk_53b5c4f1c3664a5190f6ed7dc603f94e

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route("/")
@app.route("/gen", methods=["GET", "POST"])
def gen():
    if request.method == "POST":
        # Get raw text as string from request
        text = request.form.get("input");
        if not text:
            return apology("no text given", 400)
        # Build the model.
        text_model = markovify.Text(text)

        output = ""
        # Print five randomly-generated sentences
        for i in range(5):
            output += str(text_model.make_sentence())

        # Print three randomly-generated sentences of no more than 280 characters
        for i in range(3):
            output += str(text_model.make_short_sentence(280))
        return render_template("gened.html", out=output)
    else:
        return render_template("gen.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
