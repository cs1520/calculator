from flask import Flask, render_template
from random import randint


app = Flask(__name__)


@app.route('/')
def root():
    """Generate the homepage

    The render_template function reads an HTML file from the "templates" directory
    and fills in any variables 
    """
    return render_template('index.html')


@app.route('/lecture')
def handle_lecture():
    """Generate a page with a list of lectures

    The list of lectures is a Python list of links
    """
    lectures = [{"date": "Jan 9, 2020", "topic": "HTTP and the Internet"}, {"date": "Jan 16, 2020", "topic": "Python and Javascript"}]
    return render_template('lectures.html', lectures=lectures)

@app.route('/syllabus')
def users(user=None):
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
