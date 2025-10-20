import json
import os

def enviar_dados(dados):
    try:
        if os.path.exists('banco.json'):
            with open('banco.json', "r", encoding="utf-8") as f:
                try:
                    registros = json.load(f)
                    if not isinstance(registros, list):
                        registros = [registros]
                except json.JSONDecodeError:
                    registros = []

        # Adiciona o novo registro
        registros.append(dados)

        # Salva de volta no JSON
        with open('banco.json', "w", encoding="utf-8") as f:
            json.dump(registros, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Ocorreu um erro ao tentar salvar o arquivo: {e}")