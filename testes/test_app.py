import pytest
from unittest.mock import MagicMock
from src.app import obter_proximo_sec
from src.app import conectar
import mysql.connector
import os


def conectar():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root"),
            database=os.getenv("DB_NAME", "alimentos"),
            port=3306
        )
        return conn

    except Exception as e:
        print("Erro de conexão:", e)
        return None


def test_sec_primeiro_registro():
    """Testa quando não existe nenhum registro no grupo."""

    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (None,)

    resultado = obter_proximo_sec(cursor_mock, "A")

    assert resultado == "0001"


def test_sec_incremento_normal():
    """Testa incremento quando já existem registros."""

    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (5,)

    resultado = obter_proximo_sec(cursor_mock, "A")

    assert resultado == "0006"


def test_sec_formatacao_quatro_digitos():
    """Testa se o código mantém 4 dígitos."""

    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (9,)

    resultado = obter_proximo_sec(cursor_mock, "A")

    assert resultado == "0010"


def teste_ver_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM frutas")
    resultados = cursor.fetchall()

    print("CONTEUDO TABELA")
    for linha in resultados:
        print(linha)
    cursor.close()
    conn.close()

    assert True


'''
def test_sec_falha_exemplo():
    """Teste propositalmente errado para demonstrar falha."""

    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (5,)

    resultado = obter_proximo_sec(cursor_mock, "A")

    # esperado errado de propósitoOOOO
    assert resultado == "0005"

'''


print("")