from flask import Flask, render_template, request, redirect, url_for
import mysql.connector


app = Flask(__name__)


# ----- Banco de Dados -----


def inicializar_banco_de_dados():
    # 1) Conecta sem o parâmetro "database"
    conexao = mysql.connector.connect(host="localhost", user="root", password="")
    cursor = conexao.cursor()

    # 2) Cria o banco de dados se não existir
    cursor.execute("CREATE DATABASE IF NOT EXISTS biblioteca_python")
    cursor.execute("USE biblioteca_python")

    # 3) Cria a tabela se não existir
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS livros (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(100) NOT NULL,
            autor VARCHAR(100) NOT NULL,
            ano_publicacao INT
        )
    """
    )

    conexao.commit()
    conexao.close()


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
            print("")
    else:
        print("Nenhum livro encontrado!")

    return livros


# --- Atualizar ---
def atualizar_livros(id_livro, novo_titulo, novo_autor, novo_ano):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE livros
    SET titulo = %s, autor = %s, ano_publicacao = %s
    WHERE id = %s
    """
    valores = (novo_titulo, novo_autor, novo_ano, id_livro)

    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()


# --- Excluir ---
def excluir_livro(id_livro):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM livros WHERE id = %s", (id_livro,))
    conexao.commit()
    conexao.close()

    print("Livro Excluído com Sucesso!!!")


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


# ----- Rotas -----
# --- Páginas ---
# Ler/Listar
@app.route("/")
def index():
    # Faz uma requisição por todos os livros
    livros = listar_livros()

    return render_template("index.html", livros=livros)


# Criar
@app.route("/adicionar.html")
def adicionar_html():

    # Faz uma requisição por todos os bimestres
    bimestres = query_db(
        """
        SELECT 
            bimestres.id_bimestre, 
            bimestres.nome
        FROM bimestres
        ORDER BY bimestres.nome;"""
    )

    # Faz uma requisição por todas as disciplinas
    disciplinas = query_db(
        """
        SELECT 
            disciplinas.id_disciplina, 
            disciplinas.nome
        FROM disciplinas
        ORDER BY disciplinas.nome;"""
    )

    # Faz uma requisição por todas as salas
    salas = query_db(
        """
        SELECT 
            salas.id_sala, 
            salas.nome
        FROM salas
        ORDER BY salas.nome;"""
    )

    # Faz uma requisição por todas as notas
    notas = query_db(
        """
        SELECT 
            notas.id_nota, 
            notas.valor, 
            -- Cria aliases
            alunos.nome AS nome_aluno,
            disciplinas.nome AS nome_disciplina,
            bimestres.nome AS nome_bimestre
        FROM notas
        -- Une notas.id_aluno, notas.id_disciplina e notas.id_bimestre
        JOIN alunos ON notas.id_aluno = alunos.id_aluno
        JOIN disciplinas ON notas.id_disciplina = disciplinas.id_disciplina
        JOIN bimestres ON notas.id_bimestre = bimestres.id_bimestre
        ORDER BY notas.id_nota;"""
    )

    return render_template(
        "adicionar.html",
        bimestres=bimestres,
        disciplinas=disciplinas,
        salas=salas,
        notas=notas,
    )


# Excluir
@app.route("/excluir.html")
def excluir_html():
    # Faz uma requisição por todos os bimestres
    bimestres = query_db(
        """
        SELECT 
            bimestres.id_bimestre, 
            bimestres.nome
        FROM bimestres
        ORDER BY bimestres.nome;"""
    )

    # Faz uma requisição por todas as disciplinas
    disciplinas = query_db(
        """
        SELECT 
            disciplinas.id_disciplina, 
            disciplinas.nome
        FROM disciplinas
        ORDER BY disciplinas.nome;"""
    )

    # Faz uma requisição por todas as salas
    salas = query_db(
        """
        SELECT 
            salas.id_sala, 
            salas.nome
        FROM salas
        ORDER BY salas.nome;"""
    )

    # Faz uma requisição por todos os alunos
    alunos = query_db(
        """
        SELECT 
            alunos.id_aluno, 
            alunos.nome, 
            salas.nome AS nome_sala -- Cria um alias
        FROM alunos
        -- Une alunos.id_sala a salas.id_sala
        JOIN salas ON alunos.id_sala = salas.id_sala
        ORDER BY salas.nome;"""
    )

    # Faz uma requisição por todas as notas
    notas = query_db(
        """
        SELECT 
            notas.id_nota, 
            notas.valor, 
            -- Cria aliases
            alunos.nome AS nome_aluno,
            disciplinas.nome AS nome_disciplina,
            bimestres.nome AS nome_bimestre
        FROM notas
        -- Une notas.id_aluno, notas.id_disciplina e notas.id_bimestre
        JOIN alunos ON notas.id_aluno = alunos.id_aluno
        JOIN disciplinas ON notas.id_disciplina = disciplinas.id_disciplina
        JOIN bimestres ON notas.id_bimestre = bimestres.id_bimestre
        ORDER BY alunos.nome;"""
    )

    return render_template(
        "excluir.html",
        bimestres=bimestres,
        disciplinas=disciplinas,
        salas=salas,
        alunos=alunos,
        notas=notas,
    )


# Atualizar
@app.route("/atualizar.html")
def atualizar_html():

    # Faz uma requisição por todos os bimestres
    bimestres = query_db(
        """
        SELECT 
            bimestres.id_bimestre, 
            bimestres.nome
        FROM bimestres
        ORDER BY bimestres.nome;"""
    )

    # Faz uma requisição por todas as disciplinas
    disciplinas = query_db(
        """
        SELECT 
            disciplinas.id_disciplina, 
            disciplinas.nome
        FROM disciplinas
        ORDER BY disciplinas.nome;"""
    )

    # Faz uma requisição por todas as salas
    salas = query_db(
        """
        SELECT 
            salas.id_sala, 
            salas.nome
        FROM salas
        ORDER BY salas.nome;"""
    )

    # Faz uma requisição por todos os alunos
    alunos = query_db(
        """
        SELECT 
            alunos.id_aluno, 
            alunos.nome, 
            salas.nome AS nome_sala -- Cria um alias
        FROM alunos
        -- Une alunos.id_sala a salas.id_sala
        JOIN salas ON alunos.id_sala = salas.id_sala
        ORDER BY salas.nome;"""
    )

    # Faz uma requisição por todas as notas
    notas = query_db(
        """
        SELECT 
            notas.id_nota, 
            notas.valor, 
            -- Cria aliases
            alunos.nome AS nome_aluno,
            disciplinas.nome AS nome_disciplina,
            bimestres.nome AS nome_bimestre
        FROM notas
        -- Une notas.id_aluno, notas.id_disciplina e notas.id_bimestre
        JOIN alunos ON notas.id_aluno = alunos.id_aluno
        JOIN disciplinas ON notas.id_disciplina = disciplinas.id_disciplina
        JOIN bimestres ON notas.id_bimestre = bimestres.id_bimestre
        ORDER BY alunos.nome;"""
    )

    return render_template(
        "atualizar.html",
        bimestres=bimestres,
        disciplinas=disciplinas,
        salas=salas,
        alunos=alunos,
        notas=notas,
    )


if __name__ == "__main__":
    with app.app_context():
        inicializar_banco_de_dados()
        popular_db()
    app.run(host="0.0.0.0", debug=True)
