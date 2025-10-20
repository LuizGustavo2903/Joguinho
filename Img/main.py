import v2
import Enviar_dados

if __name__ == "__main__":
    
    dados = v2.main()
    
    #dados = {'nome': 'nom', 'email': 'email', 'regi': [(1, {'Criatividade': 10, 'Adaptabilidade': -10}), (2, {'Inteligência Emocional': 10, 'Criatividade': -10}), (3, {'Inteligência Emocional': 10, 'Adaptabilidade': -5}), (4, {'Inteligência Emocional': 15, 'Adaptabilidade': -10}), (5, {'Comunicação': 10, 'Criatividade': -10}), (6, {'Adaptabilidade': 10, 'Comunicação': -10}), (7, {'Comunicação': 10, 'Adaptabilidade': -15}), (8, {'Comunicação': 10, 'Adaptabilidade': -10})]}
    try:
        regi = dados["regi"]
        novo_dados= [];
        for i in range(len(regi)):
            TempDic={};
            for key in regi[i][1].keys():
                val=0
                if(key == 'Comunicação'):
                    val=regi[i][1]["Comunicação"]
                    TempDic["1"]=val
                elif(key == "Inteligência Emocional"):
                    val=regi[i][1]["Inteligência Emocional"]
                    TempDic["2"]=val
                elif(key == "Adaptabilidade"):
                    val = regi[i][1]["Adaptabilidade"]
                    TempDic['3']=val
                elif(key == "Criatividade"):
                    val = regi[i][1]["Criatividade"]
                    TempDic['4']=val 
            novo_dados.append({"temp": regi[i][0], "altera":TempDic.copy()})
            
        dados["regi"]=novo_dados
        Enviar_dados.enviar_dados(dados)
    except IOError as e:
        print(f"Ocorreu um erro ao tentar salvar o arquivo: {e}")
