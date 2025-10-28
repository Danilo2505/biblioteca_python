import mysql.connector
import os


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


def menu():
    limpar_terminal(aguardar=False)
    while True:
        print("--- Sistema Biblioteca ---")
        print("1 - Adicionar")
        print("2 - Listar Livros")
        print("3 - Atualizar Livros")
        print("4 - Excluir Livros")
        print("0 - Sair")
        print("")

        opcao = str(input("Escolha uma opção: "))

        match opcao:
            # Adicionar
            case "1":
                titulo = input("Título: ")
                autor = input("Autor: ")
                ano_publicacao = int(input("Ano de Publicação: "))

                adicionar_livro(titulo, autor, ano_publicacao)
            # Listar Livros
            case "2":
                listar_livros()
            # Atualizar Livros
            case "3":
                listar_livros()

                id_livro = int(input("ID do Livro: "))
                novo_titulo = input("Novo Título: ")
                novo_autor = input("Novo Autor: ")
                novo_ano = int(input("Novo Ano de Publicação: "))

                atualizar_livros(id_livro, novo_titulo, novo_autor, novo_ano)
            # Excluir Livros
            case "4":
                listar_livros()

                id_livro = int(input("ID do Livro: "))

                excluir_livro(id_livro)
            # Sair
            case "0":
                limpar_terminal(aguardar=False)
                return 0
            case _:
                opcao = str(input("Escolha uma opção:"))
        limpar_terminal(aguardar=True)


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
    inicializar_banco_de_dados()
    popular_db()
    menu()
