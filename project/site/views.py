from flask import render_template

from project.site import site


@site.route('/')
def index():
    return render_template('site/index.html')
