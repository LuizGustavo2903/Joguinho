import mysql.connector
from mysql.connector import Error
import json


def LerConx():
    
    NOME_ARQUIVO = 'Conx.json' 

    try:
        with open(NOME_ARQUIVO, 'r') as arquivo:
            return json.load(arquivo)
        

        
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{NOME_ARQUIVO}' não foi encontrado.")
        db_config = None
    except json.JSONDecodeError:
        print(f"ERRO: O arquivo '{NOME_ARQUIVO}' contém JSON mal formatado.")
        db_config = None

    if db_config:
        print(f"\nHost extraído: {db_config['host']}")



db_config = LerConx()


# Dicionários para cachear IDs e evitar consultas repetidas
atributo_id_cache = {}
usuario_atributo_id_cache = {}

def get_or_create_atributo(cursor, nome_atributo):
    """
    Verifica se um atributo existe pelo nome. Se não, cria.
    Retorna o ID do atributo.
    """
    if nome_atributo in atributo_id_cache:
        return atributo_id_cache[nome_atributo]

    try:
        # 1. Tenta encontrar o atributo
        cursor.execute("SELECT id_atributo FROM atributo WHERE nome = %s", (nome_atributo,))
        result = cursor.fetchone()
        
        if result:
            id_atr = result[0]
        else:
            # 2. Se não encontrar, cria o atributo
            cursor.execute("INSERT INTO atributo (nome) VALUES (%s)", (nome_atributo,))
            id_atr = cursor.lastrowid
            print(f"Atributo '{nome_atributo}' criado com ID: {id_atr}")
            
        atributo_id_cache[nome_atributo] = id_atr
        return id_atr
        
    except Error as e:
        print(f"Erro ao buscar/criar atributo '{nome_atributo}': {e}")
        raise # Propaga o erro para acionar o rollback

def get_or_create_usuario_atributo(cursor, id_usuario, id_atributo):
    """
    Verifica se a ligação usuario_atributo existe. Se não, cria.
    Retorna o ID da ligação (id_usuario_atributo).
    """
    cache_key = (id_usuario, id_atributo)
    if cache_key in usuario_atributo_id_cache:
        return usuario_atributo_id_cache[cache_key]

    try:
        # 1. Tenta encontrar a ligação
        query = "SELECT id_usuario_atributo FROM usuario_atributo WHERE fk_usuario = %s AND fk_atributo = %s"
        cursor.execute(query, (id_usuario, id_atributo))
        result = cursor.fetchone()
        
        if result:
            id_ua = result[0]
        else:
            # 2. Se não encontrar, cria a ligação
            query_insert = "INSERT INTO usuario_atributo (fk_usuario, fk_atributo) VALUES (%s, %s)"
            cursor.execute(query_insert, (id_usuario, id_atributo))
            id_ua = cursor.lastrowid
            
        usuario_atributo_id_cache[cache_key] = id_ua
        return id_ua

    except Error as e:
        print(f"Erro ao buscar/criar ligação usuario_atributo ({id_usuario}, {id_atributo}): {e}")
        raise # Propaga o erro para acionar o rollback

def inserir_dados(config, dados_usuario):
    """
    Função principal para inserir todos os dados em uma transação.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # --- Início da Transação ---

        # 1. Inserir o Usuário
        sql_usuario = "INSERT INTO usuario (nome, email) VALUES (%s, %s)"
        val_usuario = (dados_usuario['nome'], dados_usuario['email'])
        cursor.execute(sql_usuario, val_usuario)
        id_usuario = cursor.lastrowid
        print(f"Usuário '{dados_usuario['nome']}' inserido com ID: {id_usuario}")

        # 2. Iterar sobre os registros de evolução
        for etapa, atributos_dict in dados_usuario['regi']:
            for nome_atributo, desenvolvimento in atributos_dict.items():
                
                # 2a. Garantir que o atributo existe e pegar o ID
                id_atributo = get_or_create_atributo(cursor, nome_atributo)
                
                # 2b. Garantir que a ligação usuario-atributo existe e pegar o ID
                id_ua = get_or_create_usuario_atributo(cursor, id_usuario, id_atributo)
                
                # 2c. Inserir o registro de evolução
                sql_evolucao = "INSERT INTO evolucao (fk_usuario_atributo, desenvolvimento, etapa) VALUES (%s, %s, %s)"
                val_evolucao = (id_ua, desenvolvimento, etapa)
                cursor.execute(sql_evolucao, val_evolucao)

        # Se tudo deu certo, comita a transação
        connection.commit()
        print(f"\nSucesso! Todos os {len(dados_usuario['regi'])} blocos de registros de evolução foram inseridos para o usuário ID {id_usuario}.")

    except Error as e:
        print(f"\nErro durante a transação: {e}")
        if connection:
            print("Rollback realizado.")
            connection.rollback()
            
    finally:
        # Fecha o cursor e a conexão
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("Conexão com o banco de dados fechada.")

# --- Executar a inserção ---
def enviar_dados(dados):
    inserir_dados(db_config, dados)