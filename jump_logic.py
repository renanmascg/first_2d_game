import pygame

# definição de cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# CONTROLE DE FRAMES
controle_FPS = pygame.time.Clock()

# definição do tamanho da tela
LARGURA = 500
ALTURA = 480

# define a altura maxima do pulo
ALTURA_MAXIMA_PULO = 8

imgs_andar_direita = [pygame.image.load('GameImages/R{}.png'.format(i)) for i in range(1, 10)]
imgs_andar_esquerda = [pygame.image.load('GameImages/L{}.png'.format(i)) for i in range(1, 10)]
img_personagem = pygame.image.load('GameImages/standing.png')
background = pygame.image.load('GameImages/bg.jpg')

try:
    pygame.init()
except:
    print("Algo inesperado ocorreu ao iniciar o pygame.")

sair_jogo = False

tela = pygame.display.set_mode([LARGURA, ALTURA])
pygame.display.set_caption("Jump Logic")


class Player:
    def __init__(self, pos_x, pos_y, largura, altura):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.largura = largura
        self.altura = altura
        self.velocidade = 5
        self.is_pulando = False
        self.direita = False
        self.esquerda = False
        self.altura_pulo_atual = ALTURA_MAXIMA_PULO
        self.transicao_de_imagem = 0
        self.parado = True

    def movimentar_personagem(self, key_pressed):
        if key_pressed[pygame.K_RIGHT]:
            self.pos_x += player.velocidade
            self.direita = True
            self.esquerda = False
            self.parado = False

        elif key_pressed[pygame.K_LEFT]:
            self.pos_x -= player.velocidade
            self.direita = False
            self.esquerda = True
            self.parado = False
        else:
            self.parado = True
            self.transicao_de_imagem = 0

        if key_pressed[pygame.K_SPACE]:
            self.is_pulando = True

        if self.is_pulando:
            if player.altura_pulo_atual >= -ALTURA_MAXIMA_PULO:
                fl_caindo = 1

                if self.altura_pulo_atual < 0:  # inversao para o personagem cair
                    fl_caindo = -1

                self.pos_y -= (self.altura_pulo_atual ** 2) / 2 * fl_caindo
                self.altura_pulo_atual -= 1

            else:
                self.altura_pulo_atual = ALTURA_MAXIMA_PULO
                self.is_pulando = False

    def desenhar_personagem(self, tela):
        if self.transicao_de_imagem + 1 == 27:
            self.transicao_de_imagem = 0

        if not self.parado:

            if self.direita:
                tela.blit(imgs_andar_direita[self.transicao_de_imagem // 3], (self.pos_x, self.pos_y))
                self.transicao_de_imagem += 1

            elif self.esquerda:
                tela.blit(imgs_andar_esquerda[self.transicao_de_imagem // 3], (self.pos_x, self.pos_y))
                self.transicao_de_imagem += 1

        else:

            if self.direita:
                tela.blit(imgs_andar_direita[0], (self.pos_x, self.pos_y))
            else:
                tela.blit(imgs_andar_esquerda[0], (self.pos_x, self.pos_y))


def redesenhar_tela():
    controle_FPS.tick(27)
    tela.blit(background, (0, 0))

    player.desenhar_personagem(tela)

    pygame.display.update()


player = Player(300, 410, 64, 64)
while not sair_jogo:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair_jogo = True

    key_pressed = pygame.key.get_pressed()

    player.movimentar_personagem(key_pressed)

    redesenhar_tela()

pygame.quit()
