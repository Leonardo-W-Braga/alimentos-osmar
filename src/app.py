import mysql.connector

# ---------------------------------------------------
# CONEXÃO COM BANCO
# ---------------------------------------------------
def conectar():
    """Estabelece a conexão com o banco de dados MySQL."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="estoque_frutas"
        )

        inicializar_banco(conn)  # garante tabela + dados seed
        return conn

    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        return None


# ---------------------------------------------------
# CRIA TABELA E INSERE DADOS PARA TESTES (SEED)
# ---------------------------------------------------
def inicializar_banco(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS frutas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sec VARCHAR(4),
            grupo_id VARCHAR(1),
            fruta VARCHAR(50),
            codigo_completo VARCHAR(10)
        )
    """)

    # verifica se já existem dados
    cursor.execute("SELECT COUNT(*) FROM frutas")
    total = cursor.fetchone()[0]

    # se estiver vazio → insere dados iniciais
    if total == 0:
        print("Inserindo dados iniciais na tabela frutas...")

        dados = [
            ("0001", "A", "Banana"),
            ("0002", "A", "Maçã"),
            ("0001", "B", "Laranja"),
            ("0002", "B", "Uva")
        ]

        cursor.executemany(
            "INSERT INTO frutas (sec, grupo_id, fruta) VALUES (%s, %s, %s)",
            dados
        )

        conn.commit()

    cursor.close()


# ---------------------------------------------------
# GERA PRÓXIMO SEC
# ---------------------------------------------------
def obter_proximo_sec(cursor, grupo_id):

    if not grupo_id:
        raise ValueError("Grupo inválido")

    query = "SELECT MAX(CAST(sec AS UNSIGNED)) FROM frutas WHERE grupo_id = %s"
    cursor.execute(query, (grupo_id,))
    resultado = cursor.fetchone()[0]

    novo_numero = (resultado + 1) if resultado else 1
    return str(novo_numero).zfill(4)


# ---------------------------------------------------
# CADASTRAR FRUTA (INTERATIVO)
# ---------------------------------------------------
def cadastrar_fruta():
    db = conectar()
    if not db:
        return

    cursor = db.cursor()

    print("\n--- NOVO CADASTRO ---")
    fruta_nome = input("Digite o nome da fruta: ").strip().capitalize()
    grupo_letra = input("Digite a letra do Grupo ID: ").strip().upper()

    if not fruta_nome or not grupo_letra:
        print("Erro: Nome da fruta e Grupo são obrigatórios.")
        db.close()
        return

    try:
        query_busca = "SELECT codigo_completo FROM frutas WHERE fruta = %s AND grupo_id = %s"
        cursor.execute(query_busca, (fruta_nome, grupo_letra))
        registro = cursor.fetchone()

        if registro:
            print(f"BLOQUEADO: A fruta '{fruta_nome}' já está cadastrada no Grupo '{grupo_letra}' (Código: {registro[0]}).")
        else:
            sec_final = obter_proximo_sec(cursor, grupo_letra)

            sql_insert = "INSERT INTO frutas (sec, grupo_id, fruta) VALUES (%s, %s, %s)"
            cursor.execute(sql_insert, (sec_final, grupo_letra, fruta_nome))
            db.commit()

            print(f"Sucesso! Item cadastrado com o código: BR{sec_final}{grupo_letra}")

    except mysql.connector.Error as err:
        print(f"Erro inesperado: {err}")

    finally:
        cursor.close()
        db.close()


# ---------------------------------------------------
# EXECUÇÃO MANUAL
# ---------------------------------------------------
if __name__ == "__main__":
    print("========================================")
    print("   SISTEMA DE GESTÃO DE FRUTAS (BR)     ")
    print("========================================")

    while True:
        cadastrar_fruta()
        opcao = input("\nDeseja cadastrar outra fruta? (S/N): ").strip().upper()
        if opcao != 'S':
            print("\nEncerrando sistema... Cadastro finalizado!")
            break