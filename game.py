from flask import Flask, render_template, request
import os.path
import random
import uuid

class Game:
	def __init__(self):
		f = open(os.path.join("data", "words.txt"))
		words = f.readlines()
		w = random.choice(words)
		self.word = w.strip().upper()
		self.key = str(uuid.uuid4())

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
		return render_template("clue.html", word=game.word)
	elif request.method == 'POST':
		form_data = request.form
		print(form_data)
		return render_template("clue_share.html", clue = form_data["clue"])

if __name__ == "__main__":
	app.run()
