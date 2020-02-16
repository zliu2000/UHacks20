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

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///textual.db")

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
        #querying based on text name
        textname1 = request.form.get("textname1")
        textname2 = request.form.get("textname2")
        if not textname1 and not textname2:
            return apology("must insert at least one textname", 400)
        texts1 = db.execute("SELECT s_text FROM texts WHERE name = :name",
                name=textname1)
        texts2 = db.execute("SELECT s_text FROM texts WHERE name = :name",
                name=textname2)
        if not texts1 and not texts2:
            return apology("must provide at least one valid name", 400)

        input1 = ""
        input2 = ""
        #iterating over texts in query
        for text in texts1:
            input1 += str(text)
        for text in texts2:
            input2 += str(text)
        l1 = len(input1)
        l2 = len(input2)
        if l1 < l2:
            input2 = input2[:l1]
        else:
            input1 = input1[:l2]
        input = input1 + input2
        # Build the model.
        text_model = markovify.Text(input)

        output = ""
        # Print five randomly-generated sentences
        for i in range(6):
            output += str(text_model.make_sentence())
        ns = db.execute("SELECT DISTINCT name FROM texts")
        if textname1 and textname2:
            textname2 = " and " + textname2
        return render_template("gened.html", out=output,
            names = ns, tname1=textname1, tname2=textname2)
    else:
        """
        inp = pd.read_csv('trump.csv', index_col=False)
        text = ""
        for row in inp['text']:
            text += row
        db.execute("INSERT INTO texts (name, s_text) VALUES(:name, :text)", name="Trump", text=text)
        """
        ns = db.execute("SELECT DISTINCT name FROM texts")
        return render_template("gen.html", names=ns)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        textname = request.form.get("textname")
        input = request.form.get("input")
        if (not textname) or (not input):
            return apology("must have textname and input", 400)
        db.execute("INSERT INTO texts (name, s_text) VALUES(:name, :text)",
                name=textname, text=input)
        return redirect("/")
    else:
        return render_template("add.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
