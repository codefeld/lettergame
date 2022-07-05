from flask import Flask, render_template, request

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

@game.route("/clue", methods = ['POST', 'GET'])
def give_clue():
	if request.method == 'GET':
		return render_template("clue.html")
	elif request.method == 'POST':
		form_data = request.form
		print(form_data)
		return render_template("clue_share.html", clue = form_data["clue"])

if __name__ == "__main__":
	game.run()
