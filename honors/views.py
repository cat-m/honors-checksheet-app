from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", title="Home")
  
@app.route('/contact')
def contact():
    return render_template("contact.html", title="Contact")

@app.route('/404')
def errorpage():
    return render_template("404.html", title="404")