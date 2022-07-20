from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import os.path
import random
import uuid
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Load the .env file and populate DATABASE_URL
load_dotenv()
DATABASE_URL=os.environ['DATABASE_URL']
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Define the configuration for the Flask app
class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(BaseConfig)

# Create a database and init. Create a migrate to be used by `flask db migrate`
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

EXTRA_LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "w", "y"]

def random_letters(word):
	letters = []
	while len(letters) < 5:
		letter = random.choice(EXTRA_LETTERS).upper()
		if letter not in word:
			if letter not in letters:
				letters.append(letter)
	return letters

class Game(db.Model):
	__tablename__ = 'games'

	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String(255), nullable=False)
	key = db.Column(db.String(255), unique=True, nullable=False)
	clues = db.Column(db.PickleType)
	guesses = db.Column(db.PickleType)

	def __init__(self):
		f = open(os.path.join("data", "words.txt"))
		words = f.readlines()
		w = random.choice(words)
		self.word = w.strip().upper()
		self.key = str(uuid.uuid4())
		self.clues = []
		self.guesses = []

	def add_clue(self, clue):
		self.clues = self.clues + [clue]

	def add_guess(self, guess):
		if self.guesses is None:
			self.guesses = []
		self.guesses = self.guesses + [guess]

	def save(self):
		db.session.add(self)
		db.session.commit()

	def __repr__(self):
		return f'Game is {self.key}'

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/hello/<string:name>/")
def hello(name):
	return render_template("hello.html", name=name)

@app.route("/game/new", methods = ['POST'])
def new_game():
	game = Game()
	clue_url = "/game/{}/clue".format(game.key)
	guess_url = "/game/{}/guess".format(game.key)
	print( "http://127.0.0.1:5000{}".format(clue_url))
	print(game.word)
	game.save()
	return render_template("game.html", clue_url=clue_url, guess_url=guess_url)

@app.route("/game/<string:key>/clue", methods = ['POST', 'GET'])
def give_clue(key):
	game = Game.query.filter_by(key=key).first()
	if request.method == 'GET':
		letters = random_letters(game.word)
		return render_template("clue.html", word=game.word, uuid=game.key, letters=letters)
	elif request.method == 'POST':
		form_data = request.form
		print(form_data)
		game.add_clue(form_data["clue"])
		game.save()
		print(game.clues)
		print("http://127.0.0.1:5000/game/{}/guess".format(game.key))
		return render_template("clue_share.html", clue = form_data["clue"])

@app.route("/game/<string:key>/guess", methods = ['POST', 'GET'])
def guess(key):
	game = Game.query.filter_by(key=key).first()
	clue_url = "/game/{}/clue".format(game.key)
	print(game.word)
	print(game.clues)
	if request.method == "GET":
		return render_template("guess.html", uuid=game.key, clues=game.clues, wrong_guess=False)
	elif request.method == "POST":
		form_data = request.form
		print(form_data)
		guess = form_data["guess"]
		game.add_guess(form_data["guess"])
		game.save()
		if guess.strip().upper() == game.word:
			total_clues = len(game.clues)
			total_guesses = len(game.guesses)
			return render_template("win.html", word=game.word, total_clues=total_clues, total_guesses=total_guesses)
		else:
			return render_template("guess.html", uuid=game.key, clues=game.clues, wrong_guess=True, clue_url=clue_url)

if __name__ == "__main__":
	app.run()
