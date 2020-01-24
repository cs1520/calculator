from flask import Flask, render_template
from random import randint


app = Flask(__name__)


@app.route('/')
def root():
    """Generate the homepage

    The render_template function reads an HTML file from the "templates" directory
    and fills in any variables 
    """
    fun_number = randint(45, 121)
    return render_template('index.html', num=fun_number)


@app.route('/syllabus')
def syllabus():
    """Generate a page that contains the course syllabus

    Just like the root() function, but it's annotated with a different route
    """
    return render_template('syllabus.html')


@app.route('/lecture')
def handle_lecture():
    """Generate a page with a list of lectures

    In this iteration, the data is read from a hardcoded list in Python.
    """
    lectures = [
        {"date": "Jan 9, 2020", "title": "HTTP and the Internet", "url": "https://docs.google.com/presentation/d/1Z1TwlIKHDGxMHPhRX1IH0wz6MbfbKGcMvrhAYS2MQLM/edit?usp=sharing"}, 
        {"date": "Jan 9, 2020", "title": "Handling Requests", "url": "https://docs.google.com/presentation/d/1Z1TwlIKHDGxMHPhRX1IH0wz6MbfbKGcMvrhAYS2MQLM/edit?usp=sharing"}, 
        {"date": "Jan 16, 2020", "title": "Intro to Python", "url": "https://docs.google.com/presentation/d/1yrfJdNNvAwKVsGGPGgyGHd-uWT0j3iZNw_PovI8rDIE/edit?usp=sharing"},
        # Each dictionary in this list has three keys, "date", "title", and "url"
        # Because we need all of these keys to render the page, and we will always have them, this could also be a good time to use a define a Python class for "Lecture".
        {"date": "Jan 16, 2020", "title": "Intro to Javascript", "url": "https://docs.google.com/presentation/d/1HUjfcA_fhwb8K5nUSxZGXrtBgGAo2pxkdK68PYz_FqQ/edit?usp=sharing"}]
    return render_template('lectures.html', lectures=lectures)


@app.route('/about')
def handle_about():
    """Generate a page with a description of the inner workings!"""
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
