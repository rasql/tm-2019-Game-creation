from pygame.locals import *
from fonctions import *
from carte import *

pygame.init()

# taille de la fenetre
w, h = 1280, 720
taille_fenetre = (w, h)
surface_fenetre = pygame.display.set_mode(taille_fenetre)  # crée la fenetre
# surface_fenetre = pygame.display.set_mode(taille_fenetre, pygame.FULLSCREEN)  # (MAC)

# initialisation du text
text = pygame.font.SysFont("monospace", 25)
money = 0

# cx,cy = caméra a la position x et y (w, h)
cx, cy = 0, 0
souris_x, souris_y = 0, 0  # on initiallise les variables de la position

BLANC = (255, 255, 255)
BLEU = (5, 5, 30)
ROUGE = (255, 0, 0)
BRUN = (105, 65, 25)
GRIS = (180, 180, 180)
NOIR = (12, 12, 15)

plan3 = pygame.Surface((12000, 1000))
plan3.fill(BLANC)
plan3.set_colorkey(BLANC)  # rend la partie blanche invisible
plan1 = pygame.Surface((12000, 1000))
plan1.fill(BLANC)
plan1.set_colorkey(BLANC)

timer = pygame.time.Clock()
# création du cube
cube = pygame.image.load("images/zombie.png").convert_alpha()
cube = pygame.transform.scale(cube, (40, 40))
# Position de départ du cube
cube_x, cube_y = (500-20), (h*3/5-20)
# Vitesse du joueur
cube_vx, cube_vy = 0, 0

#  bad = ennemi
bad1 = pygame.image.load("images/triangle.png").convert_alpha()
bad1 = pygame.transform.scale(bad1, (40, 40))
tab_ennemis = []

# création des arrière plans
fond1 = pygame.image.load("images/fond1.jpg")
fond1 = pygame.transform.scale(fond1, (1600, 800))

fond2 = pygame.image.load("images/fond2.jpg")
fond2 = pygame.transform.scale(fond2, (1600, 800))

fond3 = pygame.image.load("images/fond3.jpg")
fond3 = pygame.transform.scale(fond3, (1600, 800))

hud_bas = pygame.Surface((1280, 90))
hud_bas.fill(NOIR)

hud_droit = pygame.Surface((100, 100))
hud_droit.fill(NOIR)

balle = pygame.Surface((14, 14))
balle.fill(ROUGE)
cible_x, cible_y, balle_x, balle_y, depart_x, depart_y = 0, 0, 0, 0, 0, 0

gravite = 0.7
# (0.7)

# création du 3ème plan
plan3.blit(fond1, (-2, -118))
plan3.blit(fond2, (1598, -118))
plan3.blit(fond3, (3198, -118))


# on crée le monde
carte0 = map1a
carte6 = map1g

carte = randome_carte()
carte1 = carte
carte = randome_carte()
carte2 = carte
carte = randome_carte()
carte3 = carte
carte = randome_carte()
carte4 = carte
carte = randome_carte()
carte5 = carte

# crée le monde 1
plan1 = creation_carte(carte0, carte1, carte2, carte3, carte4, carte5, carte6, plan1, tab_ennemis)

# Boucle pour tout les touches que le joueur peut utiliser
timer_portail = 0
tire = 0
down = 0
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                continuer = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_w or event.key == K_UP:
                if cube_vy == 0 or cube_vy == 0.7:
                    cube_vy = -15
                    down = 0
        if event.type == KEYDOWN:
            if event.key == K_s or event.key == K_DOWN:
                cube_vy = 25
                down = 1
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                cube_vy = -3
                cube_x, cube_y = 460, 380
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                tire = 200
                depart_x, depart_y = cube_x + 13, cube_y + 13
                balle_x, balle_y = cube_x + 13, cube_y + 13
                cible_x = event.pos[0] - 7
                cible_y = event.pos[1] - 7
                if cible_x or cible_y == 0:
                    cible_x += 1
                    cible_y += 1
                a, b = int((cible_x - cube_x)/3), int((cube_x - cible_x)/3)
                if a < b:
                    cible_x += random.randint(a, b)
                if a > b:
                    cible_x += random.randint(b, a)
                a, b = int((cible_y - cube_y)/3), int((cube_y - cible_y)/3)
                if a < b:
                    cible_y += random.randint(a, b)
                if a > b:
                    cible_y += random.randint(b, a)
        if event.type == MOUSEMOTION:
            souris_x = event.pos[0]  # envoie les position de la souris à la caméra
            souris_y = event.pos[1]

    money_text = text.render(str(money), 1, BLANC)

    # calcule de la position de la caméra
    cx = cube_x - 20 - 640 - ((1280 - souris_x - 2) - 640)/2
    """cy = (cube_y - 20 - 360 - ((720 - souris_y - 2) - 320)/2) - 80"""

    if cx <= 0:
        cx = 0
    """if cx >= 1280:
        cx = 1280"""
    """if cy >= 0:
        cy = 0"""

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
    if -40 <= cube_x <= 1280:
        cube_x, cube_y, cube_vx, cube_vy = collision(carte0, (old_x, old_y), (cube_x, cube_y), cube_vx, cube_vy)
    if 1240 <= cube_x <= 2560:
        cube_x, cube_y, cube_vx, cube_vy = collision(carte1, (old_x - 1280, old_y), (cube_x - 1280, cube_y), cube_vx, cube_vy)
        cube_x += 1280
    if 2520 <= cube_x <= 3840:
        cube_x, cube_y, cube_vx, cube_vy = collision(carte2, (old_x - 2560, old_y), (cube_x - 2560, cube_y), cube_vx, cube_vy)
        cube_x += 2560
    if 3800 <= cube_x <= 5120:
        cube_x, cube_y, cube_vx, cube_vy = collision(carte3, (old_x - 3840, old_y), (cube_x - 3840, cube_y), cube_vx, cube_vy)
        cube_x += 3840
    if 5080 <= cube_x <= 6400:
        cube_x, cube_y, cube_vx, cube_vy = collision(carte4, (old_x - 5120, old_y), (cube_x - 5120, cube_y), cube_vx, cube_vy)
        cube_x += 5120
    if 6360 <= cube_x <= 7680:
        cube_x, cube_y, cube_vx, cube_vy = collision(carte5, (old_x - 6400, old_y), (cube_x - 6400, cube_y), cube_vx, cube_vy)
        cube_x += 6400
    if 7640 <= cube_x <= 9660:
        cube_x, cube_y, cube_vx, cube_vy = collision(carte6, (old_x - 7680, old_y), (cube_x - 7680, cube_y), cube_vx, cube_vy)
        cube_x += 7680

    if tire > 0:

        balle_vx, balle_vy = tire_cible(depart_x, depart_y, cible_x, cible_y, cx, cy)
        balle_x += balle_vx * 5.5
        balle_y += balle_vy * 5.5
        tire -= 1
        if -40 <= balle_x <= 1280:
            tire = collision_tire(carte0, balle_x, balle_y, tire, tab_ennemis, 0)
        if 1240 <= balle_x <= 2560:
            tire = collision_tire(carte1, balle_x - 1280, balle_y, tire, tab_ennemis, 1)
        if 2520 <= balle_x <= 3840:
            tire = collision_tire(carte2, balle_x - 2560, balle_y, tire, tab_ennemis, 2)
        if 3800 <= balle_x <= 5120:
            tire = collision_tire(carte3, balle_x - 3840, balle_y, tire, tab_ennemis, 3)
        if 5080 <= balle_x <= 6400:
            tire = collision_tire(carte4, balle_x - 5120, balle_y, tire, tab_ennemis, 4)
        if 6360 <= balle_x <= 7680:
            tire = collision_tire(carte5, balle_x - 6400, balle_y, tire, tab_ennemis, 5)
        if 7640 <= balle_x <= 9660:
            tire = collision_tire(carte6, balle_x - 7680, balle_y, tire, tab_ennemis, 6)

    #  plan3, plan2, plan1 = 3ème plan, 2ème plan, 1er plan
    #  affiche à l'écran tout les object a afficher
    surface_fenetre.fill(BLANC)
    surface_fenetre.blit(plan3, (- cx / 3, - cy / 2))
    if tire > 0:
        surface_fenetre.blit(balle, (balle_x - cx, balle_y - cy))
    afficher_ennemis(surface_fenetre, tab_ennemis, bad1, cx, cy)
    surface_fenetre.blit(cube, (cube_x - cx, cube_y - cy))
    surface_fenetre.blit(plan1, (-cx, -cy))
    surface_fenetre.blit(hud_bas, (0, 630))
    surface_fenetre.blit(hud_droit, (1180, 0))
    surface_fenetre.blit(money_text, (1230, 20))
    pygame.display.flip()

    # Chaque frame = (1/tick sec) ~IPS
    timer.tick(60)

pygame.quit()
