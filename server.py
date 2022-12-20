"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                    redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View Homepage."""

    return render_template('homepage.html')

@app.route('/users', methods=["POST"])
def register_user():
    """Create new user."""
    
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user:
        flash("User already exists. Please use another email address.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    
    return redirect("/")

@app.route("/login", methods=["POST"])
def process_login():
    """Process User Login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        #Store user email in session to log in.
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")
    
    return redirect("/")

@app.route('/users')
def all_users():
    """Shows all users"""

    users = crud.get_users()

    return render_template("all_users.html", users = users)

@app.route('/users/<user_id>')
def show_user(user_id):
    """Shows detains on particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user = user)

@app.route('/movies')
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template("all_movies.html", movies = movies)

@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie = movie)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
