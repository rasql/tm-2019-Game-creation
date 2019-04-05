import pygame
from pygame.locals import *
from fonctions import *
from carte import *

pygame.init()

# on choisit la carte
carte = carte_1

# taille de la fenetre
w, h = 1000, 600
taille_fenetre = (w, h)
surface_fenetre = pygame.display.set_mode((taille_fenetre)) # crée la fenetre

BLANC  = (200, 255, 255)
# bleu = (5, 5, 30)
ROUGE  = (255,0,0)

timer = pygame.time.Clock()
# création du cube
cube = pygame.image.load("images/zombie.png").convert_alpha()
cube = pygame.transform.scale(cube, (40, 40))
cube.set_colorkey((255,255,255))
# Position de départ du cube
cube_x, cube_y = (500-20), (h*3/5-20)
# Vitesse du joueur
cube_vx, cube_vy = 0, 0

fond = pygame.image.load("images/foret.jpg")
fond = pygame.transform.scale(fond, (1002,602))

gravite = 0.8

portail = pygame.image.load("images/portail.png")
portail = pygame.transform.scale(portail, (100, 140))

# Boucle pour tout les touches que le joueur peut utiliser
timer_portail = 0
tire = 0
down = 0
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            stop = 1
            continuer = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                stop = 1
                continuer = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_w:
                if cube_vy >= 0 and cube_vy <= 0.8:
                    cube_vy = -15
                    down = 0
        if event.type == KEYDOWN:
            if event.key == K_s:
                cube_vy = 25
                down = 1
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                cube_vy = -3
                cube_x ,cube_y = (460), (380)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                balle = pygame.Surface((14,14))
                balle_x, balle_y = (cube_x+7, cube_y+7)
                balle.fill(ROUGE )
                tire = 300
                cible_x = event.pos[0]
                cible_y = event.pos[1]
                cube_x_fix = cube_x
                cube_y_fix = cube_y

    # Chaque frame = (1/tick sec) ~IPS
    timer.tick(60)
    # touche pour bouger a droite et a gauche(des 0 et des 1)
    touche_appuyer = pygame.key.get_pressed()
    old_x, old_y = cube_x, cube_y
    cube_vx = (touche_appuyer[K_d] - touche_appuyer[K_a]) * 7
    # on applique les déplacement
    cube_vy += gravite
    if down == 0:
        cube_vy = min(16, cube_vy)  # On limite la vitesse de la vitesse de chut
    cube_x += cube_vx
    cube_y += cube_vy
    # mure de l'écran
    cube_y = min(3000, cube_y)
    cube_y = max(-250, cube_y)
    # modifie c'est 4 donner par rapport au collision
    cube_x, cube_y, cube_vx, cube_vy = collision(carte, (old_x, old_y), (cube_x, cube_y), cube_vx, cube_vy)

    if carte == carte_1:
        if cube_x > 1000:
            cube_x = 0
            carte = carte_2
    if carte == carte_2:
        if cube_x < -40:
            cube_x = 960
            carte = carte_1

    if cube_y < -40:
        cube_y = 600
        cube_x = 680
        carte = carte_1

    if cube_y > 600:
        cube_y = -40
        carte = carte_4


    if timer_portail <= 1:
        if carte == carte_2:
            if cube_x >= 580 and cube_x <= 720 and cube_y >= 400 and cube_y <= 580:
                carte = carte_3
                cube_x,cube_y = 480, 100
                timer_portail = 120
    if timer_portail <= 1:
        if carte == carte_3:
            if cube_x >= 410 and cube_x <= 550 and cube_y >= 10 and cube_y <= 190:
                carte = carte_2
                cube_x, cube_y = 650, 490
                timer_portail = 120

    timer_portail -= 1

    surface_fenetre.fill(BLANC )
    surface_fenetre.blit(fond, (-2,-2))

    if tire > 0:

        v_x, v_y = tire_cible(cube_x_fix, cube_y_fix, cible_x, cible_y)
        balle_x += v_x*5.5
        balle_y += v_y*5.5
        tire -= 1
        tire = collision_tire(carte, balle_x, balle_y, tire)
        surface_fenetre.blit(balle, (balle_x, balle_y))

    if carte == carte_2:
        surface_fenetre.blit(portail, (620,440))
    if carte == carte_3:
        surface_fenetre.blit(portail, (450,50))

    creation_carte(surface_fenetre, carte)
    surface_fenetre.blit(cube, (cube_x, cube_y))
    pygame.display.flip()
pygame.quit()