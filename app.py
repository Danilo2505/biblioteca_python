from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

"""
STATIC_FILE_DIRECTORY = "static"

# Serve os arquivos estáticos
@app.route("/static/<path:filename>")
def serve_specific_file(filename):
    return send_from_directory(STATIC_FILE_DIRECTORY, filename)
"""

def conectar():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="aluno123",
        database="biblioteca_python"
    )
    return conexao

def adicionar_livro(titulo: str, autor: str, ano_publicacao: int):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = f"INSERT INTO livros(titulo, autor, ano_publicacao) VALUES (%s, %s, %s)"

    valores = (titulo, autor, ano_publicacao)

    cursor.excecute(sql, valores)

    print("Livro Adicionado com Sucesso!!!")
