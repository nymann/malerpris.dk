from flask import render_template

from project.admin import admin


@admin.route("/")
def index():
    return render_template("errors/internal_server_error.html")


@admin.route("/login")
def login():
    pass