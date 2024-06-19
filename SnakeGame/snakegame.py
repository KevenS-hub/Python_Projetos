import pygame 
import random

pygame.init()
pygame.display.set_caption("Jogo Snake Python") 
largura, altura = 1000, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()
som_comida = pygame.mixer.Sound('som_comida.mp3')

# cores
preta = (0, 0, 0)
branca = (255, 255, 255)
verdelux = (20, 189, 20)
vermelha = (255, 0, 0)
cinza = (200, 200, 200)

# parametros da cobrinha
tamanho_quadrados = 20
velocidade_snake = 7
velocidade_aumento = 3

def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrados) / float(tamanho_quadrados)) * float(tamanho_quadrados)
    comida_y = round(random.randrange(0, altura - tamanho_quadrados) / float(tamanho_quadrados)) * float(tamanho_quadrados)

    return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, vermelha, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("Helvetica", 35)
    texto = fonte.render(f"Pontos: {pontuacao}", True, verdelux)
    tela.blit(texto, [1, 1])

def selecionar_velocidade(tecla, velocidade_x, velocidade_y):
    if tecla == pygame.K_DOWN and velocidade_y == 0:
        velocidade_x = 0
        velocidade_y = tamanho_quadrados
    elif tecla == pygame.K_UP and velocidade_y == 0:
        velocidade_x = 0
        velocidade_y = -tamanho_quadrados
    elif tecla == pygame.K_RIGHT and velocidade_x == 0:
        velocidade_x = tamanho_quadrados
        velocidade_y = 0
    elif tecla == pygame.K_LEFT and velocidade_x == 0:
        velocidade_x = -tamanho_quadrados
        velocidade_y = 0
    return velocidade_x, velocidade_y

def desenhar_menu(rect_start):
    tela.fill(preta)
    fonte = pygame.font.SysFont("Helvetica", 75)
    titulo = fonte.render("SnakeGame Python", True, verdelux)
    tela.blit(titulo, [largura // 2 - titulo.get_width() // 2, altura // 4])

    fonte_pequena = pygame.font.SysFont("Helvetica", 50)
    mouse_pos = pygame.mouse.get_pos()

    if rect_start.collidepoint(mouse_pos):
        botao_start = fonte_pequena.render("Start", True, cinza)
        rect_start = botao_start.get_rect(center=(largura // 2, altura // 2))
        pygame.draw.rect(tela, preta, rect_start.inflate(10, 10))
    else:
        botao_start = fonte_pequena.render("Start", True, branca)
        rect_start = botao_start.get_rect(center=(largura // 2, altura // 2))

    tela.blit(botao_start, rect_start.topleft)
    pygame.display.update()
    return rect_start

def game_over():
    tela.fill(preta)
    fonte = pygame.font.SysFont("Helvetica", 75)
    mensagem = fonte.render("Game Over!", True, vermelha)
    tela.blit(mensagem, [largura // 2 - mensagem.get_width() // 2, altura // 4])

    fonte_pequena = pygame.font.SysFont("Helvetica", 50)
    botao_reiniciar = fonte_pequena.render("Reiniciar", True, branca)
    rect_reiniciar = botao_reiniciar.get_rect(center=(largura // 2, altura // 2 + 50))
    tela.blit(botao_reiniciar, rect_reiniciar.topleft)

    pygame.display.update()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_reiniciar.collidepoint(evento.pos):
                    return True
                
    return False

def rodar_jogo():
    fim_jogo = False

    x = largura / 2
    y = altura / 2

    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1
    pixels = []

    comida_x, comida_y = gerar_comida()
    velocidade_atual = velocidade_snake

    while not fim_jogo:
        tela.fill(preta)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True

            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key, velocidade_x, velocidade_y)

        # comida
        desenhar_comida(tamanho_quadrados, comida_x, comida_y)

        # atualizar a posicao da cobra
        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_jogo = True

        x += velocidade_x
        y += velocidade_y


        # parte da passagem por paredes
        if x >= largura:
            x = 0
        elif x < 0:
            x = largura - tamanho_quadrados
        elif y >= altura:
            y = 0
        elif y < 0:
            y = altura - tamanho_quadrados

        # desenhar cobra
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        #se a cobrinha bateu no proprio corpo
        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                fim_jogo = True

        desenhar_cobra(tamanho_quadrados, pixels)

        desenhar_pontuacao(tamanho_cobra - 1)
        
         # criar uma nova comida
        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()  
            som_comida.play()

            if tamanho_cobra % 5 == 0:
                velocidade_atual += velocidade_aumento

        relogio.tick(velocidade_atual)
        
        pygame.display.update()
    
    return game_over()

def main():
    fonte_pequena = pygame.font.SysFont("Helvetica", 50)
    botao_start = fonte_pequena.render("Start", True, branca)
    rect_start = botao_start.get_rect(center=(largura // 2, altura // 2))

    menu = True
    while menu:
        rect_start = desenhar_menu(rect_start)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                menu = False
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_start.collidepoint(evento.pos):
                    menu = False

    while True:
        if not rodar_jogo():
            break

if __name__ == "__main__":
    main()

# loop para o jogo
pygame.quit()
