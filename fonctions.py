from carte import *
import random


class Ennemis1:
    #  donne à l'objet ennemis ça position initiale et c'est point de vie

    def __init__(self, pos_x, pos_y):

        self.vie = 50
        self.pos_x = pos_x
        self.pos_y = pos_y


def ennemis_vivant(tab_ennemis):
    #  regarde si les ennemis ne sont pas mort(le fait a chaque fois qu'il prenne des dégat)

    for i in range(len(tab_ennemis)):
        print(tab_ennemis[i].vie)
        if tab_ennemis[i].vie < 0:
            del tab_ennemis[i]
            break


def afficher_ennemis(surface_fenetre, tab_ennemis, bad1, cx, cy):
    #  affiche les ennemis a chaque frame

    for i in range(len(tab_ennemis)):
        surface_fenetre.blit(bad1, (tab_ennemis[i].pos_x - cx, tab_ennemis[i].pos_y - cy))


def creation_ennemis(tab_ennemis, pos_x, pos_y):
    #  crée un nouvelle ennemis chauqe fois que cette fonction est appelé

    ennemis = Ennemis1(pos_x, pos_y)
    tab_ennemis.append(ennemis)
    return tab_ennemis


def position_cube(position):
    # indique ou ce situe notre cube sur la carte

    cube_x, cube_y = position
    i = max(0, int(cube_x // 40))
    k = max(0, int(cube_y // 40))
    return i, k


def zone_collision_cube(carte, i_cube, k_cube):
    # envoie les zone concérner par la collision

    blocks = list()
    for k in range(k_cube, k_cube + 4):
        for i in range(i_cube, i_cube + 4):
            if 0 <= k <= 15 and 0 <= i <= 31:
                if carte[k][i] >= 1:
                    topleft = i * 40, k * 40
                    blocks.append(pygame.Rect(topleft, (40, 40)))

    return blocks


def collision(carte, old_position, new_position, cube_vx, cube_vy):
    # la ou se passe tout la collision

    old_rect = pygame.Rect(old_position, (40, 40))
    new_rect = pygame.Rect(new_position, (40, 40))
    i, k = position_cube(new_position)
    collide_later = list()  # on crée un tableau vide
    blocks = zone_collision_cube(carte, i, k)
    for block in blocks:
        if not new_rect.colliderect(block):
            continue

        dx_correction, dy_correction = compute_penetration(block, old_rect, new_rect)
        # Dans cette première phase, on n'ajuste que les pénétrations sur un seul axe.
        if dx_correction == 0.0:
            new_rect.top += dy_correction
            cube_vy = 0.0
        elif dy_correction == 0.0:
            new_rect.left += dx_correction
            cube_vx = 0.0
        else:
            collide_later.append(block)

    # Collision pour les blocks qui en posséde sur les 2 axes.
    for block in collide_later:
        dx_correction, dy_correction = compute_penetration(block, old_rect, new_rect)
        if dx_correction == dy_correction == 0.0:
            # Finalement plus de pénétration. Le new_rect a bougé précédemment
            # lors d'une résolution de collision
            continue
        if abs(dx_correction) < abs(dy_correction):
            # Faire la correction que sur l'axe X (plus bas)
            dy_correction = 0.0
        elif abs(dy_correction) < abs(dx_correction):
            # Faire la correction que sur l'axe Y (plus bas)
            dx_correction = 0.0
        if dy_correction != 0.0:
            new_rect.top += dy_correction
            cube_vy = 0.0
        elif dx_correction != 0.0:
            new_rect.left += dx_correction
            cube_vx = 0.0

    cube_x, cube_y = new_rect.topleft
    return cube_x, cube_y, cube_vx, cube_vy


def compute_penetration(block, old_rect, new_rect):
    dx_correction = dy_correction = 0.0
    if old_rect.bottom <= block.top < new_rect.bottom:
        dy_correction = block.top - new_rect.bottom
    elif old_rect.top >= block.bottom > new_rect.top:
        dy_correction = block.bottom - new_rect.top
    if old_rect.right <= block.left < new_rect.right:
        dx_correction = block.left - new_rect.right
    elif old_rect.left >= block.right > new_rect.left:
        dx_correction = block.right - new_rect.left
    return dx_correction, dy_correction


def tire_cible(balle_x, balle_y, cible_x, cible_y, cx, cy):
    # calcule la direction est la vitesse des tire du cube

    v_x = cible_x - (balle_x - cx)
    v_y = cible_y - (balle_y - cy)
    k = 1/((v_x**2 + v_y**2)**(1/2))
    v_x = k * v_x
    v_y = k * v_y
    return v_x, v_y


def collision_tire(carte, balle_x, balle_y, tire, tab_ennemis, k):
    # detecte si le cube est sur un mur et si oui le supprime ou un ennemis

    balle_x_non_corriger = balle_x + k * 1280

    for i in range(len(tab_ennemis)):
        if tab_ennemis[i].pos_x + 40 > balle_x_non_corriger > tab_ennemis[i].pos_x - 14:
            if tab_ennemis[i].pos_y + 40 > balle_y > tab_ennemis[i].pos_y - 14:
                tab_ennemis[i].vie -= 30
                ennemis_vivant(tab_ennemis)
                return 0

    x_1, x_2 = balle_x, balle_x + 14
    y_1, y_2 = balle_y, balle_y + 14

    x_1 = int(x_1 / 40)
    x_2 = int(x_2 / 40)
    y_1 = int(y_1 / 40)
    y_2 = int(y_2 / 40)

    if x_1 >= 0 and x_2 <= 31 and y_1 >= 0 and y_2 <= 15:

        n1 = carte[y_1][x_1]
        n2 = carte[y_2][x_1]
        n3 = carte[y_1][x_2]
        n4 = carte[y_2][x_2]
    else:
        return tire

    if n1 >= 1 or n2 >= 1 or n3 >= 1 or n4 >= 1:
        return 0
    else:
        return tire


def randome_carte():
    # Envoie une carte aléatoire

    # randome = random.randint(0, 4)
    # if randome == 0:
    #     carte = map1b
    # if randome == 1:
    #     carte = map1c
    # if randome == 2:
    #     carte = map1d
    # if randome == 3:
    #     carte = map1e
    # if randome == 4:
    #     carte = map1f

    #  return carte
    maps = [map1b, map1c, map1d, map1e, map1f]
    map = random.choice(maps)
    return map


def creation_carte(carte0, carte1, carte2, carte3, carte4, carte5, carte6, plan1, tab_ennemis):
    #  crée le 1er plan
    x = 0
    carte = carte0
    boucle = 0

    while boucle <= 6:
        for k, ligne in enumerate(carte):
            for i, case in enumerate(ligne):
                if case == 1:
                    plan1.blit(mur1, ((i * 40) + x, k * 40))
                if case == 2:
                    plan1.blit(mur2, ((i * 40) + x, k * 40))
                if case == 3:
                    plan1.blit(mur3, ((i * 40) + x, k * 40))
                if case == -3:
                    creation_ennemis(tab_ennemis, i * 40 + x, k * 40)
        boucle += 1
        x += 1280
        if boucle == 1:
            carte = carte1
        if boucle == 2:
            carte = carte2
        if boucle == 3:
            carte = carte3
        if boucle == 4:
            carte = carte4
        if boucle == 5:
            carte = carte5
        if boucle == 6:
            carte = carte6

    return plan1

if __name__ == '__main__':
    print(randome_carte())
