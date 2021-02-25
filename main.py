from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/registration')
def registration():
    return render_template('registration.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
