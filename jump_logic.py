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

VELOCIDADE_DE_ATAQUE = 5

# define a altura maxima do pulo
ALTURA_MAXIMA_PULO = 8

# MÁXIMO DE PROJETEIS NA TELA
MAX_PROJETEIS = 5

# IMAGENS PRESENTES NA TELA
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
        self.projeteis = []
        self.hitbox = (self.pos_x + 17, self.pos_y + 11, 29, 52)
        self.vel_ataque = VELOCIDADE_DE_ATAQUE

    def acoes_personagem(self, key_pressed):

        if self.vel_ataque < VELOCIDADE_DE_ATAQUE:
            self.vel_ataque -= 1

        if self.vel_ataque == 0:
            self.vel_ataque = VELOCIDADE_DE_ATAQUE

        if key_pressed[pygame.K_SPACE] and len(self.projeteis) < MAX_PROJETEIS and \
                self.vel_ataque == VELOCIDADE_DE_ATAQUE:
            self.adicionar_projetil()
            self.vel_ataque -= 1

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

        if key_pressed[pygame.K_UP]:
            self.is_pulando = True

        if self.is_pulando:
            if player.altura_pulo_atual >= -ALTURA_MAXIMA_PULO:
                fl_caindo = 1

                if self.altura_pulo_atual < 0:  # inversao para o personagem cair
                    fl_caindo = -1

                self.pos_y -= (self.altura_pulo_atual ** 2) // 2 * fl_caindo
                self.altura_pulo_atual -= 1

            else:
                self.altura_pulo_atual = ALTURA_MAXIMA_PULO
                self.is_pulando = False

    def adicionar_projetil(self):
        proj_pos_x = self.pos_x + self.largura // 2
        proj_pos_y = self.pos_y + self.altura // 2

        if self.direita:
            direcao = 1
        else:
            direcao = -1

        self.projeteis.append(Projectile(proj_pos_x, proj_pos_y, 5, AZUL, direcao))

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
        self.hitbox = (self.pos_x + 17, self.pos_y + 11, 29, 52)
        pygame.draw.rect(tela, VERMELHO, self.hitbox, 2)

    def atualizar_projetil(self):
        for proj in self.projeteis:
            if proj.pos_x < 0 or proj.pos_x > LARGURA:
                self.projeteis.pop(self.projeteis.index(proj))
            else:
                proj.pos_x += proj.velocidade

    def atingiu_inimigo(self, inimigo):
        for proj in self.projeteis:
            if proj.colidir_com(inimigo):
                inimigo.hit()
                self.projeteis.remove(proj)


class Projectile:
    def __init__(self, pos_x, pos_y, raio, cor, direcao):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.raio = raio
        self.cor = cor
        self.direcao = direcao
        self.velocidade = 8 * direcao

    def desenhar_projetil(self, tela):
        pygame.draw.circle(tela, self.cor, (self.pos_x, self.pos_y), self.raio)

    def colidir_com(self, objeto):
        if self.pos_x + self.raio > objeto.hitbox[0] and self.pos_x - self.raio < objeto.hitbox[0] + objeto.hitbox[2] \
                and self.pos_y + self.raio > objeto.hitbox[1] and self.pos_y - self.raio < objeto.hitbox[1] + \
                objeto.hitbox[3]:
            return True
        return False


class Enemy:
    inimigos_imgs_direita = [pygame.image.load('GameImages/R{}E.png'.format(i)) for i in range(1, 12)]
    inimigos_imgs_esquerda = [pygame.image.load('GameImages/L{}E.png'.format(i)) for i in range(1, 12)]

    def __init__(self, pos_x, pos_y, largura, altura, pos_final):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.largura = largura
        self.altura = altura
        self.pos_final = pos_final
        self.caminho_percorrer = [pos_x, pos_final]
        self.velocidade = 3
        self.transicao_imagens = 0
        self.hitbox = (self.pos_x + 17, self.pos_y + 2, 31, 57)

    def desenhar_inimigo(self, tela):
        if self.transicao_imagens + 1 > 33:
            self.transicao_imagens = 0

        if self.velocidade > 0:
            tela.blit(self.inimigos_imgs_direita[self.transicao_imagens // 3], (self.pos_x, self.pos_y))
        else:
            tela.blit(self.inimigos_imgs_esquerda[self.transicao_imagens // 3], (self.pos_x, self.pos_y))

        self.transicao_imagens += 1

        self.hitbox = (self.pos_x + 17, self.pos_y + 2, 31, 57)
        pygame.draw.rect(tela, VERMELHO, self.hitbox, 2)

    def move(self):
        # andar para a direita - verificar se chegou no limite
        if self.velocidade > 0:
            if self.pos_x + self.velocidade < self.caminho_percorrer[1] - self.largura // 2:
                self.pos_x += self.velocidade
            else:
                self.velocidade *= -1
                self.transicao_imagens = 0
        else:
            if self.pos_x - self.velocidade > self.caminho_percorrer[0]:
                self.pos_x += self.velocidade
            else:
                self.velocidade *= -1
                self.transicao_imagens = 0

    def hit(self):
        print("hit")


def redesenhar_tela():
    controle_FPS.tick(27)
    tela.blit(background, (0, 0))

    player.desenhar_personagem(tela)

    goblin.desenhar_inimigo(tela)

    for projetil in player.projeteis:
        projetil.desenhar_projetil(tela)

    pygame.display.update()


player = Player(300, 410, 64, 64)
goblin = Enemy(100, 410, 64, 64, 450)
while not sair_jogo:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair_jogo = True

    key_pressed = pygame.key.get_pressed()

    player.acoes_personagem(key_pressed)

    player.atualizar_projetil()

    player.atingiu_inimigo(goblin)

    goblin.move()

    redesenhar_tela()

pygame.quit()
