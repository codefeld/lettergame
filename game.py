from django.shortcuts import render
from flask import Flask, render_template, request
import os.path
import random
import uuid

EXTRA_LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "w", "y"]

def random_letters(word):
	letters = []
	while len(letters) < 5:
		letter = random.choice(EXTRA_LETTERS).upper()
		if letter not in word:
			if letter not in letters:
				letters.append(letter)
	return letters

class Game:
	def __init__(self):
		f = open(os.path.join("data", "words.txt"))
		words = f.readlines()
		w = random.choice(words)
		self.word = w.strip().upper()
		self.key = str(uuid.uuid4())
		self.clues = []

	def add_clue(self, clue):
		self.clues.append(clue)

app = Flask(__name__)
games = {}

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/hello/<string:name>/")
def hello(name):
	return render_template("hello.html", name=name)

@app.route("/game/new", methods = ['POST'])
def new_game():
	game = Game()
	games[game.key] = game
	print("http://localhost:5000/game/{}/clue".format(game.key))
	print(game.word)
	return render_template("game.html")

@app.route("/game/<string:key>/clue", methods = ['POST', 'GET'])
def give_clue(key):
	game = games[key]
	if request.method == 'GET':
		letters = random_letters(game.word)
		return render_template("clue.html", word=game.word, uuid=game.key, letters=letters)
	elif request.method == 'POST':
		form_data = request.form
		print(form_data)
		game.add_clue(form_data["clue"])
		print("http://localhost:5000/game/{}/guess".format(game.key))
		return render_template("clue_share.html", clue = form_data["clue"])

@app.route("/game/<string:key>/guess", methods = ['POST', 'GET'])
def guess(key):
	game = games[key]
	if request.method == "GET":
		return render_template("guess.html", uuid=game.key, clues=game.clues, wrong_guess=False)
	elif request.method == "POST":
		form_data = request.form
		print(form_data)
		guess = form_data["guess"]
		if guess.strip().upper() == game.word:
			return render_template("win.html", word=game.word)
		else:
			return render_template("guess.html", uuid=game.key, clues=game.clues, wrong_guess=True)

if __name__ == "__main__":
	app.run()
