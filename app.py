from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

"""
STATIC_FILE_DIRECTORY = "static"

# Serve os arquivos estáticos
@app.route("/static/<path:filename>")
def serve_specific_file(filename):
    return send_from_directory(STATIC_FILE_DIRECTORY, filename)
"""


# Banco de dados
def init_db():
    conn = sqlite3.connect("livros.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano INTEGER,
            genero TEXT
        )
    """
    )
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():
    conn = sqlite3.connect("livros.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros ORDER BY id DESC LIMIT 4")
    livros = cursor.fetchall()
    conn.close()
    return render_template("index.html", livros=livros)


@app.route("/adicionar", methods=["POST"])
def adicionar():
    titulo = request.form["titulo"]
    autor = request.form["autor"]
    ano = request.form["ano"]
    genero = request.form["genero"]
    conn = sqlite3.connect("livros.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO livros (titulo, autor, ano, genero) VALUES (?, ?, ?, ?)",
        (titulo, autor, ano, genero),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


# Você pode adicionar rotas para editar, deletar e buscar também

if __name__ == "__main__":
    app.run(debug=True)
