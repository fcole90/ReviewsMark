from flask import Flask, render_template, url_for

app= Flask(__name__)

@app.route('/home')
def index():
	url_for('static', filename='css/bootstrap.css', _external=True)
	return render_template('index.html')
@app.errorhandler(404)
def error(e):
	url_for('static', filename='css/404.css', _external=True)
	return render_template('404.html'), 404


if __name__ == '__main__':
	app.run(host='0.0.0.0')
