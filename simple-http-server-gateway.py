#!/usr/bin/env python3

# Equalivant to main.py written with Flask
import functools
import http.server
import json
import os
import socketserver
from urllib.parse import parse_qs, parse_qsl, urlencode, urlparse, urlsplit, urlunsplit
import requests
import argparse
import stat
import subprocess
import sys

PORT = 5000
LOCAL_HOST = "127.0.0.1"


def get_url_last_slash_part(url: str):
    return url.split('?', 1)[0]


class MyHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        return super().end_headers()

    def do_GET(self):
        if get_url_last_slash_part(self.path) == '/route1':
            query = dict(parse_qsl(urlparse(self.path).query))
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"name": query["name"]}).encode("utf-8"))
            self.wfile.flush()

            # self.send_response(200)
            # self.send_header("Content-type", "application/json")
            # self.end_headers()
            # self.wfile.write(json.dumps({'is_rpc': self.is_rpc}).encode("utf-8"))
            # self.wfile.flush()
        elif get_url_last_slash_part(self.path) == '/route2':
            query = dict(parse_qsl(urlparse(self.path).query))
            scheme, netloc, path, query_string, fragment = urlsplit(self.path)
            url_params = parse_qs(query_string)
            res = requests.get("https://reqres.in/api/users", params=url_params)
            if res.status_code == 200:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(res.json()).encode("utf-8"))
                self.wfile.flush()
            else:
                self.send_response(res.status_code)
        # Server at `/` to match the uri
        else:
            self.directory = os.path.dirname(__file__) + "/static"
            os.chdir(self.directory)
            return super().do_GET()

    def do_POST(self):
        pass


def start_server() -> int:
    Handler = functools.partial(MyHTTPHandler)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((LOCAL_HOST, PORT), Handler) as httpd:
        print("Server started on: http://" + LOCAL_HOST + ":" + str(PORT))
        print("Press Ctrl+C to quit")
        httpd.serve_forever()
    return 0


def main():
    try:
        start_server()
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    exit(main())
