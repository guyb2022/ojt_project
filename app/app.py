import os
from flask import Flask, request, render_template, Response
from flask_cors import CORS, cross_origin

execution_path = os.getcwd()

app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route("/", methods= ['GET','POST'])
@cross_origin()
def homepage(): # Redirecting to home page
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)



