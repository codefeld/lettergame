from flask import Flask, render_template

game = Flask(__name__)

@game.route("/")
def index():
	return render_template("index.html")

@game.route("/hello/<string:name>/")
def hello(name):
	return render_template("hello.html", name=name)

@game.route("/game/new", methods = ['POST'])
def new_game():
	return render_template("game.html")

@game.route("/clue")
def give_clue():
	return render_template("clue.html")

@game.route("/game/<string:id>/clue", methods = ['POST'])
def new_clue():
	return render_template(".html")

if __name__ == "__main__":
	game.run()
