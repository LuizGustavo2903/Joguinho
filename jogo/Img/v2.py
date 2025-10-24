import pygame
import sys
from datetime import datetime
# ----------------------------
# Configurações iniciais
# ----------------------------
pygame.init()

# ----------------------------
# Imagens dos personagens
# ----------------------------
imagens_personagens = {
    "Marcelo": pygame.image.load("Img/nerd.png"),
    "Ângela": pygame.image.load("Img/garota_confusa.png"),
    "Anderson": pygame.image.load("img/garoto_popular.png"),
    "Leonardo": pygame.image.load("img/lider_sala.png")
}

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Destino")

# Fontes e cores
fonte_titulo = pygame.font.SysFont("timesnewroman", 56, bold=True)
fonte_texto = pygame.font.SysFont("arial", 22)
fonte_pequena = pygame.font.SysFont("arial", 18)
BRANCO = (255, 255, 255)
PRETO = (10, 10, 10)
CINZA = (45, 45, 45)
AZUL = (80, 120, 220)
VERDE = (80, 200, 120)
AMARELO = (230, 200, 60)
VERMELHO = (220, 80, 80)

CLOCK = pygame.time.Clock()
FPS = 60

# ----------------------------
# Atributos do jogador
# ----------------------------
atributos = {
    "Adaptabilidade": 50,
    "Comunicação": 50,
    "Inteligência Emocional": 50,
    "Criatividade": 50
}
ATR_MIN, ATR_MAX = 0, 100


def ajustar_atributos(delta):
    for k, v in delta.items():
        if k in atributos:
            atributos[k] = max(ATR_MIN, min(ATR_MAX, atributos[k] + v))


# ----------------------------
# Perguntas
# ----------------------------
perguntas = [
    # Marcelo
    {
        "personagem": "Marcelo",
        "fala": "Marcelo sugere criar um cronograma com prazos rígidos para o grupo.",
        "opcoes": [
            ("Aceitar", {"Adaptabilidade": +10, "Comunicação": -10}),
            ("Rejeitar", {"Comunicação": +10, "Adaptabilidade": -10})
        ]
    },

    {
        "personagem": "Marcelo",
        "fala": "Ele percebe que alguns colegas não estão acompanhando o ritmo.",
        "opcoes": [
            ("Parar para explicar", {"Comunicação": +15, "Adaptabilidade": -20}),
            ("Continuar sozinho", {"Adaptabilidade": +15, "Inteligência Emocional": -20})
        ]
    },

    {
        "personagem": "Marcelo",
        "fala": "O prazo está apertando. Quer assumir todas as tarefas para garantir.",
        "opcoes": [
            ("Deixar ele assumir", {"Adaptabilidade": +10, "Inteligência Emocional": -15}),
            ("Dividir tarefas igualmente", {"Inteligência Emocional": +15, "Adaptabilidade": -10})
        ]
    },
    {
        "personagem": "Marcelo",
        "fala": "Na apresentação final, ele quer usar gráficos técnicos complicados.",
        "opcoes": [
            ("Manter gráficos", {"Adaptabilidade": +10, "Comunicação": -25}),
            ("Simplificar", {"Comunicação": +15, "Criatividade": -15})
        ]
    },

    # Ângela
    {
        "personagem": "Ângela",
        "fala": "Aparece com uma ideia criativa para o trabalho, mas é arriscada.",
        "opcoes": [
            ("Aceitar", {"Criatividade": +20, "Inteligência Emocional": -10}),
            ("Rejeitar", {"Adaptabilidade": +10, "Criatividade": -10})
        ]
    },
    {
        "personagem": "Ângela",
        "fala": "Ela fica ansiosa porque ninguém entende seu conceito artístico.",
        "opcoes": [
            ("Escutar e adaptar", {"Inteligência Emocional": +25, "Criatividade": -30}),
            ("Insistir na ideia", {"Criatividade": +15, "Inteligência Emocional": -10})
        ]
    },
    {
        "personagem": "Ângela",
        "fala": "Na apresentação, ela se perde tentando explicar o projeto.",
        "opcoes": [
            ("Ajudar a explicar", {"Comunicação": +15, "Criatividade": -15}),
            ("Deixar ela improvisar", {"Criatividade": +10, "Comunicação": -10})
        ]
    },
    {
        "personagem": "Ângela",
        "fala": "Faltam recursos para executar sua proposta.",
        "opcoes": [
            ("Improvisar materiais", {"Criatividade": +10, "Adaptabilidade": -10}),
            ("Voltar ao plano tradicional", {"Adaptabilidade": +10, "Criatividade": -10})
        ]
    },

    # Anderson
    {
        "personagem": "Anderson",
        "fala": "Se oferece para ser o porta-voz do grupo.",
        "opcoes": [
            ("Aceitar", {"Comunicação": +10, "Adaptabilidade": -10}),
            ("Recusar", {"Adaptabilidade": +10, "Comunicação": -10})
        ]
    },
    {
        "personagem": "Anderson",
        "fala": "Ele decide convidar outros colegas de fora para ajudar.",
        "opcoes": [
            ("Permitir", {"Comunicação": +10, "Adaptabilidade": -15}),
            ("Rejeitar", {"Adaptabilidade": +10, "Comunicação": -10})
        ]
    },
    {
        "personagem": "Anderson",
        "fala": "Improvisa uma fala engraçada na apresentação.",
        "opcoes": [
            ("Rir junto", {"Comunicação": +10, "Criatividade": -10}),
            ("Corrigir ele depois", {"Inteligência Emocional": +15, "Comunicação": -15})
        ]
    },
    {
        "personagem": "Anderson",
        "fala": "Após o trabalho, recebe aplausos, mas esquece de citar os outros.",
        "opcoes": [
            ("Reivindicar crédito", {"Adaptabilidade": +15, "Inteligência Emocional": -10}),
            ("Deixar passar", {"Inteligência Emocional": +15, "Comunicação": -10})
        ]
    },

    # Leonardo
    {
        "personagem": "Leonardo",
        "fala": "Um colega sugere uma solução arriscada e criativa.",
        "opcoes": [
            ("Apoiar", {"Criatividade": +10, "Inteligência Emocional": -10}),
            ("Recusar", {"Inteligência Emocional": +10, "Criatividade": -10})
        ]
    },
    {
        "personagem": "Leonardo",
        "fala": "O grupo começa a brigar sobre quem faz o quê.",
        "opcoes": [
            ("divide tarefas igualmente", {"Inteligência Emocional": +10, "Criatividade": -10}),
            ("Deixar eles se resolverem", {"Adaptabilidade": +5, "Inteligência Emocional": -10})
        ]
    },
    {
        "personagem": "Leonardo",
        "fala": "Um membro do grupo está desmotivado e sem ânimo.",
        "opcoes": [
            ("motiva ele", {"Inteligência Emocional": +10, "Adaptabilidade": -5}),
            ("Ignorar", {"Adaptabilidade": +20, "Inteligência Emocional": -15})
        ]
    },
    {
        "personagem": "Leonardo",
        "fala": "Na apresentação, sugere seguir o plano seguro em vez de improvisar.",
        "opcoes": [
            ("Concordar", {"Inteligência Emocional": +10, "Criatividade": -10}),
            ("Improvisar", {"Criatividade": +10, "Adaptabilidade": -10})
        ]
    }
]

# ----------------------------
# Áreas finais (exemplo)
# ----------------------------
areas = {
    "Pesquisador / Técnico": {
        "descricao": "Perfil analítico e resiliente. Ótimo para funções que exigem lógica, precisão e adaptação.",
        "profissoes": "Ex: Analista de Dados, Engenheiro, Pesquisador."
    },
    "Criativo / Designer": {
        "descricao": "Perfil imaginativo e experimental. Ideal para quem busca inovar e criar soluções visuais ou conceituais.",
        "profissoes": "Ex: Designer, Publicitário, Ilustrador."
    },
    "Comunicador / Gestor de Pessoas": {
        "descricao": "Perfil que se destaca em ouvir, articular e liderar. Bom para papéis que exigem mediação e gestão.",
        "profissoes": "Ex: Gestor de Projetos, Jornalista, RH."
    },
    "Emocionalmente Inteligente": {
        "descricao": "Perfil com alta sensibilidade social e autoconsciência, indicado para áreas que lidam com pessoas e suporte emocional.",
        "profissoes": "Ex: Psicólogo, Coach, Professor."
    }
}


# ----------------------------
# Utilitários de UI
# ----------------------------
def render_centered(text, font, y, color=BRANCO):
    surf = font.render(text, True, color)
    tela.blit(surf, (LARGURA // 2 - surf.get_width() // 2, y))


def desenhar_intro_fade():
    # Título
    titulo = fonte_titulo.render("BEM-VINDO", True, BRANCO)
    titulo_rect = titulo.get_rect(center=(LARGURA // 2, 110))

    linhas = [
        "Você foi selecionado!",
        "Parabéns!",
        "Agora que você está nos seus últimos dias",
        "do ensino médio,",
        "queremos que você apenas continue seu dia a dia.",
        "Enquanto isso, vamos avaliar suas ações.",
        "Lembre-se de se divertir!",
        "Pressione ENTER para começar."
    ]

    tela.fill(PRETO)
    tela.blit(titulo, titulo_rect)
    pygame.display.flip()

    # Aparecer linhas uma a uma com fade
    for i, linha in enumerate(linhas):
        texto_surface = fonte_texto.render(linha, True, BRANCO).convert_alpha()
        texto_rect = texto_surface.get_rect(center=(LARGURA // 2, 260 + i * 40))
        start = pygame.time.get_ticks()
        dur = 1500  # ms
        while True:
            now = pygame.time.get_ticks()
            elapsed = now - start
            alpha = min(255, int((elapsed / dur) * 255))
            texto_surface.set_alpha(alpha)
            tela.fill(PRETO)
            tela.blit(titulo, titulo_rect)
            tela.blit(texto_surface, texto_rect)
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit()
            pygame.display.flip()
            CLOCK.tick(FPS)
            if alpha >= 255:
                break


# botão simples
def desenhar_botao(rect, texto, hover):
    color = AZUL if hover else BRANCO
    pygame.draw.rect(tela, color, rect, border_radius=10)

    fonte_ajustada = fonte_texto
    if fonte_texto.size(texto)[0] > rect.width - 20:
        fonte_ajustada = pygame.font.SysFont("arial", 20)
    txt = fonte_ajustada.render(texto, True, PRETO)
    tela.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))


# mostra barras de atributos na parte superior
def desenhar_atributos():
    y0 = 15
    largura_bar = 200
    altura_bar = 18
    espaco_horizontal = 50
    espaco_vertical = 55

    i = 0
    for nome, valor in atributos.items():
        linha = i // 2  # 0 ou 1
        coluna = i % 2  # 0 ou 1
        x = 50 + coluna * (largura_bar + espaco_horizontal)
        y = y0 + linha * espaco_vertical

        # nome
        txt = fonte_pequena.render(nome, True, BRANCO)
        tela.blit(txt, (x, y))
        # barra de fundo
        pygame.draw.rect(tela, CINZA, (x, y + 22, largura_bar, 18), border_radius=8)
        # barra preenchida
        fill_w = int((valor / 100) * largura_bar)
        pygame.draw.rect(tela, VERDE, (x, y + 22, fill_w, 18), border_radius=8)
        # valor numérico
        # texto dentro da barra (centralizado)
        """val_txt = fonte_pequena.render(str(valor), True, PRETO)
        texto_x = x + (largura_bar - val_txt.get_width()) // 2
        texto_y = y + 22  # centralizado verticalmente
        tela.blit(val_txt, (texto_x, texto_y))
        """
        i += 1


# ----------------------------
# Tela de perguntas (com personagem + fala)
# ----------------------------
def tela_perguntas(sequencia):
    respostas = []
    for idx, bloco in enumerate(sequencia):
        personagem = bloco["personagem"]
        fala = bloco["fala"]
        opcoes = bloco["opcoes"]  # lista de tuples (texto, deltas)

        rodando = True
        # retângulos do quadro e botões
        quadro = pygame.Rect(80, 160, LARGURA - 160, 380)
        area_personagem = pygame.Rect(quadro.left + 40, quadro.top + 80, 230, 250)
        # botões posicionados
        botao_w, botao_h = 230, 60
        botao_a = pygame.Rect(LARGURA // 2 - botao_w - 40, quadro.bottom - 70, botao_w, botao_h)
        botao_b = pygame.Rect(LARGURA // 2 + 40, quadro.bottom - 70, botao_w, botao_h)

        while rodando:
            tela.fill(PRETO)
            desenhar_atributos()

            img = imagens_personagens.get(personagem)

            if img:
                img_redimensionada = pygame.transform.scale(img, (area_personagem.width, area_personagem.height))
                tela.blit(img_redimensionada, area_personagem.topleft)
            else:
                # Se não achar a imagem, desenha um quadrado branco como antes
                pygame.draw.rect(tela, BRANCO, area_personagem, border_radius=12)

            # nome do personagem encima da caixa
            nome_surf = fonte_texto.render(personagem, True, BRANCO)
            tela.blit(nome_surf, (area_personagem.left + 6, area_personagem.top - 28))

            # Largura da área da fala
            area_fala_largura = quadro.width - area_personagem.width - 100

            # Quebra do texto
            fala_lines = wrap_text(fala, fonte_texto, area_fala_largura)

            # Se a fala tiver muitas linhas (ou for muito comprida), usa uma fonte menor
            if len(fala_lines) > 3:
                fonte_fala = pygame.font.SysFont("arial", 22)
                fala_lines = wrap_text(fala, fonte_fala, area_fala_largura)
            else:
                fonte_fala = fonte_texto

            # Centraliza verticalmente a fala no quadro
            total_altura = sum([fonte_texto.size(l)[1] + 6 for l in fala_lines])
            y_text = quadro.centery - total_altura // 2

            # Desenha cada linha à direita do personagem
            for line in fala_lines:
                txt_s = fonte_fala.render(line, True, BRANCO)
                rect = txt_s.get_rect(
                    center=(area_personagem.right + 40 + area_fala_largura // 2, y_text)
                )
                tela.blit(txt_s, rect)
                y_text += txt_s.get_height() + 6

            # desenhar botões e hover
            mouse = pygame.mouse.get_pos()
            hover_a = botao_a.collidepoint(mouse)
            hover_b = botao_b.collidepoint(mouse)
            desenhar_botao(botao_a, opcoes[0][0], hover_a)
            desenhar_botao(botao_b, opcoes[1][0], hover_b)

            # dica de índice de pergunta
            indice_txt = fonte_pequena.render(f"Pergunta {idx + 1} / {len(sequencia)}", True, BRANCO)
            tela.blit(indice_txt, (quadro.left + 10, quadro.top - 26))

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if botao_a.collidepoint(ev.pos):
                        ajustar_atributos(opcoes[0][1])
                        respostas.append((idx+1,opcoes[0][1]))
                        rodando = False
                    if botao_b.collidepoint(ev.pos):
                        ajustar_atributos(opcoes[1][1])
                        respostas.append((idx+1, opcoes[1][1]))
                        rodando = False

            pygame.display.flip()
            CLOCK.tick(FPS)
    return respostas


# quebra de linhas para o texto (simples)
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    cur = ""
    for w in words:
        test = cur + (" " if cur else "") + w
        if font.size(test)[0] <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ----------------------------
# Tela final de resultado
# ----------------------------
def tela_resultado():
    # decide a área pelo atributo mais alto
    maior = max(atributos.items(), key=lambda x: x[1])[0]
    if maior == "Criatividade":
        area_chave = "Criativo / Designer"
        area_info = areas.get("Criativo / Designer", {})
    elif maior == "Comunicação":
        area_chave = "Comunicador / Gestor de Pessoas"
        area_info = areas["Comunicador / Gestor de Pessoas"]
    elif maior == "Inteligência Emocional":
        area_chave = "Emocionalmente Inteligente"
        area_info = areas["Emocionalmente Inteligente"]
    else:
        area_chave = "Pesquisador / Técnico"
        area_info = areas["Pesquisador / Técnico"]

    # --- campos de texto ---
    class TextBox:
        def __init__(self, x, y, w, h, placeholder=""):
            self.rect = pygame.Rect(x, y, w, h)
            self.text = ""
            self.placeholder = placeholder
            self.active = False
            self.color_inactive = CINZA
            self.color_active = AZUL
            self.color = self.color_inactive
            self.txt_surface = fonte_texto.render(placeholder, True, (150, 150, 150))

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.rect.collidepoint(event.pos)
                self.color = self.color_active if self.active else self.color_inactive
                if self.active and self.text == "":
                    self.txt_surface = fonte_texto.render("", True, BRANCO)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = self.color_inactive
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Atualiza texto
                display_text = self.text if self.text else self.placeholder
                color = BRANCO if self.text else (150, 150, 150)
                self.txt_surface = fonte_texto.render(display_text, True, color)

        def draw(self, screen):
            pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=6)
            screen.blit(self.txt_surface, (self.rect.x + 8, self.rect.y + 10))

    # --- botão ---
    class Botao:
        def __init__(self, x, y, w, h, texto):
            self.rect = pygame.Rect(x, y, w, h)
            self.texto = texto

        def draw(self, screen, hover=False):
            cor = VERDE if not hover else (100, 255, 100)
            pygame.draw.rect(screen, cor, self.rect, border_radius=10)
            txt = fonte_texto.render(self.texto, True, PRETO)
            screen.blit(txt, (
                self.rect.centerx - txt.get_width() // 2,
                self.rect.centery - txt.get_height() // 2
            ))

        def clicado(self, pos):
            return self.rect.collidepoint(pos)

    nome_box = TextBox(200, 340, 400, 40, "Digite seu nome")
    email_box = TextBox(200, 390, 400, 40, "Digite seu e-mail")
    botao = Botao(330, 440, 140, 45, "Enviar")

    rodando = True
    while rodando:
        tela.fill(PRETO)
        quadro = pygame.Rect(60, 110, LARGURA - 120, ALTURA - 220)
        pygame.draw.rect(tela, CINZA, quadro, border_radius=16)

        # título da área
        titulo_font = pygame.font.SysFont("timesnewroman", 36, bold=True)
        titulo = titulo_font.render(area_chave, True, BRANCO)
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 140))

        # descrição
        desc_lines = wrap_text(area_info["descricao"], fonte_texto, 600)
        y0 = 210
        for line in desc_lines:
            tela.blit(fonte_texto.render(line, True, BRANCO), (100, y0))
            y0 += 30

        # atributos finais
        y_atr = y0 + 20
        maior_nome, maior_valor = max(atributos.items(), key=lambda x: x[1])
        menor_nome, menor_valor = min(atributos.items(), key=lambda x: x[1])
        txt = fonte_pequena.render(f"sua melhor habilidade é {maior_nome}", True, BRANCO)
        tela.blit(txt, (100, y0+20))
        txt = fonte_pequena.render(f"sua a desenvolver habilidade é {menor_nome}", True, BRANCO)
        tela.blit(txt, (100, y0+45))

        # caixas de texto e botão
        nome_box.draw(tela)
        email_box.draw(tela)

        mouse = pygame.mouse.get_pos()
        hover = botao.rect.collidepoint(mouse)
        botao.draw(tela, hover)

        # eventos
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            nome_box.handle_event(ev)
            email_box.handle_event(ev)
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if botao.clicado(ev.pos):
                    nome = nome_box.text.strip()
                    email = email_box.text.strip()
                    if nome and email:
                        # encerra o jogo e retorna
                        return [nome, email]

        pygame.display.flip()
        CLOCK.tick(FPS)


# ----------------------------
# Execução principal
# ----------------------------
def main():
    desenhar_intro_fade()
    esperando = True
    while esperando:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                esperando = False
        CLOCK.tick(FPS)

    import random
    random.shuffle(perguntas)
    registros = tela_perguntas(perguntas[:8])

    [nome,email]= tela_resultado()
    pygame.quit()

    return {"nome":nome,"email":email,"regi":registros}


