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
        host="localhost", user="root", password="", database="biblioteca_python"
    )
    return conexao


# ----- CRUD -----


# --- Criar ---
def adicionar_livro(titulo: str, autor: str, ano_publicacao: int):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = f"INSERT INTO livros(titulo, autor, ano_publicacao) VALUES (%s, %s, %s)"
    valores = (titulo, autor, ano_publicacao)

    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

    print("Livro Adicionado com Sucesso!!!")


# --- Ler/Listar ---
def listar_livros():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * from livros")
    livros = cursor.fetchall()  # Pega todos os resultados
    conexao.close()

    if livros:
        print("Lista de livros:")
        """
        for livro in livros:
            print(f"ID: {livro[0]} | Título: {livro[1]} | Autor: {livro[2]} | Ano de Publicação: {livro[3]}")
        """
        for livro in livros:
            print(f"----- Livro de ID {livro[0]} -----")
            print(f"- Título: {livro[1]}")
            print(f"- Autor: {livro[2]}")
            print(f"- Ano de Publicação: {livro[3]}")
            print(f"")
    else:
        print("Nenhum livro encontrado!")

    return livros


# --- Atualizar ---
def atualizar_livro():
    return


# --- Excluir ---
def excluir_livro():
    return


def popular_db():
    # Se já tiver algum livro no Banco de Dados
    if listar_livros():
        print("📖 Banco de dados já possui livros. Nenhuma adição feita.")
        return

    livros = [
        ("Sherlock Holmes: Um Estudo em Vermelho", "Sir Arthur Conan Doyle", 1887),
        ("Dom Casmurro", "Machado de Assis", 1899),
        ("1984", "George Orwell", 1949),
        ("O Senhor dos Anéis: A Sociedade do Anel", "J.R.R. Tolkien", 1954),
        ("O Pequeno Príncipe", "Antoine de Saint-Exupéry", 1943),
        ("Cem Anos de Solidão", "Gabriel García Márquez", 1967),
        ("Orgulho e Preconceito", "Jane Austen", 1813),
        ("A Revolução dos Bichos", "George Orwell", 1945),
        ("O Hobbit", "J.R.R. Tolkien", 1937),
        ("A Metamorfose", "Franz Kafka", 1915),
        ("O Alquimista", "Paulo Coelho", 1988),
        ("Harry Potter e a Pedra Filosofal", "J.K. Rowling", 1997),
        ("O Código Da Vinci", "Dan Brown", 2003),
        (
            "As Crônicas de Nárnia: O Leão, a Feiticeira e o Guarda-Roupa",
            "C.S. Lewis",
            1950,
        ),
        ("A Menina que Roubava Livros", "Markus Zusak", 2005),
        ("Moby Dick", "Herman Melville", 1851),
        ("O Morro dos Ventos Uivantes", "Emily Brontë", 1847),
        ("O Conde de Monte Cristo", "Alexandre Dumas", 1844),
        ("It: A Coisa", "Stephen King", 1986),
        ("Neuromancer", "William Gibson", 1984),
    ]

    for titulo, autor, ano in livros:
        adicionar_livro(titulo, autor, ano)

    print("Banco de dados populado com sucesso!")
    listar_livros()

    return


if __name__ == "__main__":
    popular_db()
