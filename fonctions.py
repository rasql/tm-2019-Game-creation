import pygame
from pygame.locals import *

# création de "mur"
mur = pygame.Surface((20, 20))
brun = (117, 89, 60)
mur.fill(brun)

# on crée la carte selectionner
def creation_carte(surface, carte):
    for k, ligne in enumerate(carte):
        for i, case in enumerate(ligne):
            if case == 1:
                surface.blit(mur, (i * 20, k * 20))

# indique ou ce situe notre cube sur la carte
def position_cube(position):

    cube_x, cube_y = position
    i = max(0, int(cube_x // 20))
    k = max(0, int(cube_y // 20))
    return i, k

# envoie les zone concérner par la collision
def zone_collision_cube(carte, i_cube, k_cube):

    blocks = list()
    for k in range(k_cube, k_cube + 4):
        for i in range(i_cube, i_cube + 4):
            if k <= 29 and i <= 49:
                if carte[k][i] == 1:
                    topleft = i * 20, k * 20
                    blocks.append(pygame.Rect((topleft), (20, 20)))
    return blocks

# la ou se passe tout la collision
def collision(carte, old_position, new_position, cube_vx, cube_vy):

    old_rect = pygame.Rect(old_position, (40, 40))
    new_rect = pygame.Rect(new_position, (40, 40))
    i, k = position_cube(new_position)
    collide_later = list() # on crée un tableau vide
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

# calcule la direction est la vitesse des tire du cube
def tire_cible(cube_x, cube_y, cible_x, cible_y):

    cube_x += 13
    cube_y += 13
    cible_x -= 7
    cible_y -= 7
    v_x = cible_x - cube_x
    v_y = cible_y - cube_y
    k = 1/((v_x**2 + v_y**2)**(1/2))
    v_x = k * v_x
    v_y = k * v_y
    return v_x, v_y

# detecte si le cube est sur un mure et si oui le supprime
def collision_tire(carte, balle_x, balle_y, tire):

    x_1, x_2 = balle_x, balle_x + 14
    y_1, y_2 = balle_y, balle_y + 14

    x_1 = int(x_1 / 20)
    x_2 = int(x_2 / 20)
    y_1 = int(y_1 / 20)
    y_2 = int(y_2 / 20)

    n1 = carte[y_1][x_1]
    n2 = carte[y_2][x_1]
    n3 = carte[y_1][x_2]
    n4 = carte[y_2][x_2]

    if n1 == 1 or n2 == 1 or n3 == 1 or n4 == 1:
        return 0
    else:
        return tire
