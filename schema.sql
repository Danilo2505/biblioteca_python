# Cria o banco de dados biblioteca
## CREATE database biblioteca_python;

# Define o banco de dados biblioteca como o
# banco de dados padrão para a sessão atual
## USE biblioteca_python;

# Cria as tabelas
/*
CREATE table livros(
	id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    ano_publicacao INT
);
*/

# Seleciona todos os livros
SELECT * FROM livros;