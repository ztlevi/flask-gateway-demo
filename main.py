#!/usr/bin/env python3

from flask import Flask, send_from_directory, redirect, url_for, request
from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse
import requests

# Serve static web assets
app = Flask(__name__, static_url_path="/web", static_folder="static")

# serve static web assets
# The following is equalivant to `static_url_path='web', static_folder="static"`
# @app.route('/web/<path:path>')
# def send_report(path):
#     return send_from_directory('static', path)


@app.route("/")
def hello_world():
    user = request.args.get("name", "")
    return "<p>Hello, World! {}!</p>".format(user)


@app.route("/route1", methods=["POST", "GET"])
def route_local():
    if request.method == "POST":
        name = request.form["name"]
        return redirect(url_for("hello_world", name=name))
    else:
        user = request.args.get("name")
        return redirect(url_for("hello_world", name=user))

# You can use local DB or other server here, e.g. a InfluxDB http://127.0.0.1:8086
@app.route("/route2", methods=["POST", "GET"])
def route_external():
    if request.method == "POST":
        user = request.form["name"]
        job = request.form["job"]
        res = requests.post("https://reqres.in/api/users", json={"user":user, "job": job})
        return res.json()
    else:
        page= str(request.args.get("page"))
        url_parts = list(urlparse("https://reqres.in/api/users"))
        query = dict(parse_qsl(url_parts[4]))
        query.update({"page":page})
        url_parts[4] = urlencode(query)
        return redirect(urlunparse(url_parts))

