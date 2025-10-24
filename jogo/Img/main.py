import v2
import EnviarEmail
import enviar_dados

if __name__ == "__main__":
    #dados = {'nome': 'nom', 'email': 'email', 'regi': [(1, {'Criatividade': 10, 'Adaptabilidade': -10}), (2, {'Inteligência Emocional': 10, 'Criatividade': -10}), (3, {'Inteligência Emocional': 10, 'Adaptabilidade': -5}), (4, {'Inteligência Emocional': 15, 'Adaptabilidade': -10}), (5, {'Comunicação': 10, 'Criatividade': -10}), (6, {'Adaptabilidade': 10, 'Comunicação': -10}), (7, {'Comunicação': 10, 'Adaptabilidade': -15}), (8, {'Comunicação': 10, 'Adaptabilidade': -10})]}
    dados = v2.main()
    try:        
        enviar_dados.enviar_dados(dados)
    except IOError as e:
        print(f"Ocorreu um erro ao tentar salvar o : {e}")
    