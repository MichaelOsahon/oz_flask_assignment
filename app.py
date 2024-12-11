from flask import Flask, render_template, request
from spotipydemo import get_playlist
app = Flask(__name__)
@app.route('/')
def index():
	return render_template("index.html")
	
@app.route('/', methods=['POST'])
def index_post():
	user_city = request.form['req_city']
	my_playlist = get_playlist(user_city)
	print (my_playlist)
	return render_template('index.html', playlist=my_playlist, city=user_city)
