from flask import Flask, render_template, request, redirect, url_for
import mysql.connect

app = Flask(__name__)

"""
STATIC_FILE_DIRECTORY = "static"

# Serve os arquivos estáticos
@app.route("/static/<path:filename>")
def serve_specific_file(filename):
    return send_from_directory(STATIC_FILE_DIRECTORY, filename)
"""