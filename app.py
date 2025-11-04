from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os


app = Flask(__name__)
HOST = "0.0.0.0"
PORT = 5000


# ----- Auxiliares -----


def limpar_terminal(aguardar: bool = False):
    """
    Limpa o terminal.
    Se aguardar=True, o terminal só limpa depois do usuário pressionar ENTER.
    """

    if aguardar:
        input("\nPressione ENTER para continuar...")

    # Windows usa "cls", Linux/mac usa "clear"
    os.system("cls" if os.name == "nt" else "clear")


# ----- Banco de Dados -----


def inicializar_banco_de_dados():
    # 1) Conecta sem o parâmetro "database"
    print('''1) Conecta sem o parâmetro "database"''')
    conexao = mysql.connector.connect(host="localhost", user="root", password="")
    cursor = conexao.cursor(dictionary=True)

    # 2) Cria o banco de dados se não existir
    print("""2) Cria o banco de dados se não existir""")
    cursor.execute("CREATE DATABASE IF NOT EXISTS biblioteca_python")
    cursor.execute("USE biblioteca_python")

    # 3) Cria a tabela se não existir
    print("""3) Cria a tabela se não existir""")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS livros (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(100) NOT NULL,
            autor VARCHAR(100) NOT NULL,
            ano_publicacao INT,
            src_imagem VARCHAR(2000) NOT NULL
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
def adicionar_livro(titulo: str, autor: str, ano_publicacao: int, src_imagem: str):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = f"INSERT INTO livros(titulo, autor, ano_publicacao, src_imagem) VALUES (%s, %s, %s, %s)"
    valores = (titulo, autor, ano_publicacao, src_imagem)

    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

    print("Livro Adicionado com Sucesso!!!")


# --- Ler/Listar ---
def listar_livros():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * from livros")
    livros = cursor.fetchall()  # Pega todos os resultados
    conexao.close()

    if livros:
        print("Livro encontrado!")
    else:
        print("Nenhum livro encontrado!")

    return livros


# --- Atualizar ---
def atualizar_livros(id_livro, novo_titulo, novo_autor, novo_ano):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

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
    cursor = conexao.cursor(dictionary=True)

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
        (
            "Sherlock Holmes: Um Estudo em Vermelho",
            "Sir Arthur Conan Doyle",
            1887,
            "https://m.media-amazon.com/images/I/61GFsO7j0ZL._AC_UF1000,1000_QL80_.jpg",
        ),
        (
            "Dom Casmurro",
            "Machado de Assis",
            1899,
            "https://m.media-amazon.com/images/I/61x1ZHomWUL.jpg",
        ),
        (
            "1984",
            "George Orwell",
            1949,
            "https://m.media-amazon.com/images/I/61t0bwt1s3L._AC_UF1000,1000_QL80_.jpg",
        ),
        (
            "O Senhor dos Anéis: A Sociedade do Anel",
            "J.R.R. Tolkien",
            1954,
            "https://m.media-amazon.com/images/I/81hCVEC0ExL.jpg",
        ),
        (
            "O Pequeno Príncipe",
            "Antoine de Saint-Exupéry",
            1943,
            "https://m.media-amazon.com/images/I/81SVIwe5L9L._UF1000,1000_QL80_.jpg",
        ),
        (
            "Cem Anos de Solidão",
            "Gabriel García Márquez",
            1967,
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1ofwq-sF2P4IN0_3uKa0hPRMY-4wzKYcqwQ&s",
        ),
        (
            "Orgulho e Preconceito",
            "Jane Austen",
            1813,
            "https://m.media-amazon.com/images/I/719esIW3D7L.jpg",
        ),
        (
            "A Revolução dos Bichos",
            "George Orwell",
            1945,
            "https://image.isu.pub/240308195141-ea3bec1fe1822568527e6b862a841023/jpg/page_1_social_preview.jpg",
        ),
        (
            "O Hobbit",
            "J.R.R. Tolkien",
            1937,
            "https://harpercollins.com.br/cdn/shop/files/9788595086081_1200x1200.jpg?v=1754636796",
        ),
        (
            "A Metamorfose",
            "Franz Kafka",
            1915,
            "https://d1b6q258gtjyuy.cloudfront.net/Custom/Content/Products/07/49/0749_https-www-escala-com-br-a-metamorfose-franz-kafka-p2036-_z1_637957496052979369.webp",
        ),
        ("O Alquimista", "Paulo Coelho", 1988, "alquimista.jpg"),
        ("Harry Potter e a Pedra Filosofal", "J.K. Rowling", 1997, "harry_potter1.jpg"),
        (
            "O Código Da Vinci",
            "Dan Brown",
            2003,
            "https://upload.wikimedia.org/wikipedia/pt/6/6b/DaVinciCode.jpg",
        ),
    ]

    for titulo, autor, ano, src_imagem in livros:
        adicionar_livro(titulo, autor, ano, src_imagem)

    print("✅ Banco de dados populado com sucesso!")
    listar_livros()


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
        limpar_terminal()
        print("----- Inicializando Banco de Dados -----")
        inicializar_banco_de_dados()
        print("----- Populando Banco de Dados -----")
        popular_db()
    app.run(host=HOST, port=PORT, debug=True)
