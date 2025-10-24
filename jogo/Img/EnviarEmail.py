import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import matplotlib.pyplot as plt
import os # Importação útil para verificar se os arquivos existem

# ----------------------------
# Função de envio de E-mail (CORRIGIDA)
# ----------------------------
def enviar_email(nome, email, assunto, corpo_email, caminho_pizza, caminho_linha):
    # Configurações do e-mail
    # !!! MUDAR AQUI: Seu e-mail e a "Senha de App" (App Password) gerada pelo Google !!!
    remetente = "seuemail@gmail.com" 
    senha = "suasenhaoutoken"  

    # 'related' é melhor para embutir imagens no corpo do e-mail
    msg = MIMEMultipart('related') 
    msg['From'] = remetente
    msg['To'] = email
    msg['Subject'] = assunto

    # Corpo do e-mail (HTML)
    msg.attach(MIMEText(corpo_email, 'html'))

    # Adicionando o gráfico de pizza
    if os.path.exists(caminho_pizza):
        with open(caminho_pizza, 'rb') as f:
            img_pizza = MIMEImage(f.read(), name="grafico_pizza.png")
            # O 'Content-ID' '<pizza>' deve ser usado no HTML para referência: <img src="cid:pizza">
            img_pizza.add_header('Content-ID', '<pizza>') 
            msg.attach(img_pizza)
    else:
        print(f"Aviso: Arquivo de gráfico de pizza não encontrado em {caminho_pizza}")

    # Adicionando o gráfico de linha
    if os.path.exists(caminho_linha):
        with open(caminho_linha, 'rb') as f:
            img_linha = MIMEImage(f.read(), name="grafico_linha.png")
            # O 'Content-ID' '<linha>' deve ser usado no HTML para referência: <img src="cid:linha">
            img_linha.add_header('Content-ID', '<linha>')  
            msg.attach(img_linha)
    else:
        print(f"Aviso: Arquivo de gráfico de linha não encontrado em {caminho_linha}")

    # Enviar o e-mail com os gráficos (CONFIGURAÇÃO GMAIL)
    try:
        # Use o servidor SMTP do Gmail
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, email, msg.as_string()) # Usamos remetente e email diretamente
        print(f"E-mail enviado com sucesso para {email}!")
    except Exception as e:
        print(f"Erro ao enviar e-mail para {email}: {e}")

# ----------------------------
# Função para gerar os gráficos
# ----------------------------
def gerar_graficos(atributos, registros):
    # Dicionário de atributos pode ter keys diferentes do array, então usamos as keys do dict
    labels = list(atributos.keys())
    sizes = list(atributos.values())

    # Gráfico de Pizza - Atributos Finais
    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    plt.title("Distribuição Final dos Atributos")
    plt.axis('equal') 
    pie_chart_path = "grafico_pizza.png"
    plt.savefig(pie_chart_path)
    plt.close()

    # Gráfico de Linha - Evolução dos Atributos
    atributos_nome = ["Criatividade", "Comunicação", "Inteligência Emocional", "Adaptabilidade"]
    tempos = sorted(list(set(registro['temp'] for registro in registros))) 
    evolucoes = {atributo: [] for atributo in atributos_nome}
    
    # Mapeia as mudanças para os atributos, assumindo que 'registros' tem a evolução
    # Nota: Este bloco de lógica de agregação precisa ser robusto conforme o formato dos seus 'registros'
    valores_iniciais = [20, 20, 20, 20] # Assumindo um valor inicial para cada atributo
    valores_atuais = list(valores_iniciais)

    for temp in tempos:
        for i, atributo_nome in enumerate(atributos_nome):
            # Busca a alteração no registro para o tempo atual
            alteracao = 0
            for registro in registros:
                if registro.get('temp') == temp:
                    # Mapeia o índice do registro para o nome do atributo (1=Criatividade, 2=Comunicação...)
                    if str(i+1) in registro.get('altera', {}):
                        alteracao = registro['altera'][str(i+1)]
                        break # Assume uma alteração por tempo para simplificar
            
            valores_atuais[i] = valores_atuais[i] + alteracao # Calcula o novo valor
            evolucoes[atributo_nome].append(valores_atuais[i])

    # Ajusta os tempos para corresponder ao número de pontos de evolução
    tempos_plot = [temp for temp in tempos if any(evolucoes[a] for a in atributos_nome)]
    
    plt.figure(figsize=(10, 6))
    for atributo, valores in evolucoes.items():
        # Apenas plota se houver dados de evolução para evitar erros
        if valores:
            plt.plot(tempos_plot[:len(valores)], valores, label=atributo)

    plt.title("Evolução dos Atributos ao Longo do Tempo")
    plt.xlabel("Tempo")
    plt.ylabel("Valor dos Atributos")
    plt.legend()
    line_chart_path = "grafico_linha.png"
    plt.savefig(line_chart_path)
    plt.close()

    return pie_chart_path, line_chart_path

# ----------------------------
# Recomendações (CORRIGIDA e EXPANDIDA)
# ----------------------------
def obter_recomendacoes(maior_atributo, menor_atributo):
    mensagens_recomendacao = {
        "Criatividade": {
            "maior": """Com sua alta criatividade, recomendamos explorar áreas como Design Gráfico, Publicidade, Arquitetura e Engenharia Criativa. 
Profissões recomendadas: Designer Gráfico, Diretor de Arte, Designer de Produtos, Roteirista.""",
            "menor": """Vimos que sua criatividade não é seu ponto forte. Considere áreas mais técnicas ou analíticas, ou concentre-se em desenvolver esta habilidade.
Áreas a evitar: Design Gráfico, Marketing Criativo, Diretor de Arte."""
        },
        "Comunicação": {
            "maior": """Sua alta habilidade em comunicação é um grande trunfo! Recomendamos carreiras que dependem da interação e persuasão, como Vendas, Relações Públicas, Jornalismo e Recursos Humanos.
Profissões recomendadas: Vendedor de Soluções, Relações Públicas, Professor/Treinador, Consultor.""",
            "menor": """Sua comunicação está entre os atributos mais baixos. Isso pode dificultar carreiras que exigem negociação constante ou apresentações públicas.
Recomendamos focar em papéis onde a comunicação escrita ou a interação individual sejam mais comuns, enquanto desenvolve suas habilidades de oratória.
Áreas a evitar: Vendas de Alto Volume, Relações Públicas, Porta-voz da Empresa."""
        },
        "Inteligência Emocional": {
            "maior": """Sua alta Inteligência Emocional indica que você lida bem com relações interpessoais e pressão. Isso é essencial em papéis de liderança e gestão de equipes.
Profissões recomendadas: Gerente de Projetos, Recursos Humanos, Terapeuta, Mediador de Conflitos.""",
            "menor": """Sua Inteligência Emocional é uma área de desenvolvimento. Focar em escuta ativa e gerenciamento de estresse será crucial.
Áreas a evitar: Papéis de liderança direta ou gestão de crises, Terapia/Psicologia, Vendas Complexas."""
        },
        "Adaptabilidade": {
            "maior": """Sua alta adaptabilidade significa que você prospera em ambientes de mudança e incerteza. Isso é ideal para startups e carreiras em tecnologia.
Profissões recomendadas: Desenvolvedor de Software (Especialmente Full-Stack), Consultor de Inovação, Gerente de Startup, Analista de Mudança Organizacional.""",
            "menor": """Sua baixa adaptabilidade sugere que você se sente mais confortável em ambientes estáveis e estruturados.
Áreas a evitar: Startups em estágio inicial, Tecnologia em constante mudança (a menos que seja uma área de nicho estável), Funções de Gerenciamento de Crise."""
        }
    }
    
    recomendacao_maior = mensagens_recomendacao.get(maior_atributo, {}).get("maior", f"Recomendação positiva para {maior_atributo} não encontrada.")
    recomendacao_menor = mensagens_recomendacao.get(menor_atributo, {}).get("menor", f"Recomendação de cautela para {menor_atributo} não encontrada.")
    
    return recomendacao_maior, recomendacao_menor

# ----------------------------
# Exemplo de Execução (Simulação após o jogo)
# ----------------------------

# 1. Dados Finais do Jogo (Simulação)
nome = "Nome do Jogador"
email = "seu.email.destino@exemplo.com" # !!! Mude para um e-mail válido para testar
atributos = {
    "Criatividade": 25,
    "Comunicação": 35, # Maior
    "Inteligência Emocional": 20,
    "Adaptabilidade": 10 # Menor
}
# 'registros' deve ser uma lista que representa o histórico
registros = [
    {"temp": 1, "altera": {"1": 5, "2": 5}}, # Criatividade (+5), Comunicação (+5)
    {"temp": 2, "altera": {"3": 10, "4": 5}}, # IE (+10), Adaptabilidade (+5)
    {"temp": 3, "altera": {"1": 0, "2": 10}}, # Criatividade (0), Comunicação (+10)
    {"temp": 4, "altera": {"4": -15}}, # Adaptabilidade (-15) - Baixando de 25 para 10
]

if nome and email:
    # 2. Gerar os gráficos
    pie_chart_path, line_chart_path = gerar_graficos(atributos, registros)

    # 3. Determinar atributos de foco
    maior_atributo = max(atributos, key=atributos.get)
    menor_atributo = min(atributos, key=atributos.get)
    
    # 4. Obter as recomendações
    recomendacao_maior, recomendacao_menor = obter_recomendacoes(maior_atributo, menor_atributo)

    # 5. Construir o corpo do e-mail (HTML)
    corpo_email_html = f"""
    <html>
    <head></head>
    <body>
        <h1 style="color: #004d99;">Parabéns, {nome}! Seu Relatório de Atributos</h1>
        <p>Obrigado por jogar! Abaixo você encontra a análise do seu desempenho e as recomendações de carreira baseadas nas suas habilidades.</p>
        
        <h2>Seus Atributos Finais</h2>
        <p>Abaixo está a representação gráfica da distribuição:</p>
        <img src="cid:pizza" alt="Gráfico de Pizza - Distribuição Final dos Atributos" width="450" style="display: block; margin: 20px 0;"/>
        
        <h2>Evolução dos Atributos</h2>
        <p>Veja como suas habilidades evoluíram ao longo do tempo de jogo:</p>
        <img src="cid:linha" alt="Gráfico de Linha - Evolução dos Atributos" width="600" style="display: block; margin: 20px 0;"/>
        
        <h2 style="color: #28a745;">Seu Maior Ponto Forte: {maior_atributo}</h2>
        <p>{recomendacao_maior.replace('\n', '<br>')}</p>
        
        <h2 style="color: #dc3545;">Área de Atenção: {menor_atributo}</h2>
        <p>{recomendacao_menor.replace('\n', '<br>')}</p>
        
        <p>Atenciosamente,<br/>
        Sua Equipe de Desenvolvimento de Habilidades.</p>
    </body>
    </html>
    """
    
    # 6. Chamar a função de envio de e-mail
    assunto_email = "Seu Relatório de Desempenho e Recomendações de Carreira"
    enviar_email(nome, email, assunto_email, corpo_email_html, pie_chart_path, line_chart_path)

else:
    print("Nome ou e-mail do jogador não fornecidos. O relatório não pode ser enviado.")

def main():
    print("irado")