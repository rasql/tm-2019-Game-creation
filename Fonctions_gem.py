import random


class Gems:
    # class pour tout les gems

    def __init__(self, pos_x, pos_y, valeur, couleur):

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.valeur = valeur
        self.couleur = couleur


def creation_gems(carte, rouge, bleu, verte, violet, orange, puissance):
    # crée tout les gems de la partie

    list_gems = []  # on initiallise la list des gems

    for i in range(1000):

        stop = 0
        couleur = verte
        valeur = 10

        #  position aléatoire de la gems
        pos_x = random.randint(0, 2560)
        pos_y = random.randint(0, 685)

        x = random.randint(1, 40)  # x = rareté du minérait

        pos_y += x * 685 - 685
        pos_y += 640

        # test de collision avec le carte
        posx, posy, posx2, posy2 = pos_x, pos_y - 480, pos_x + 20, pos_y - 460

        posy = int(posy / 80)
        posx = int(posx / 80)

        m = 32 * posy
        m += posx
        m = carte[m]

        posx, posy, posx2, posy2 = pos_x, pos_y - 480, pos_x + 20, pos_y - 460

        posy = int(posy / 80)
        posx2 = int(posx2 / 80)

        n = 32 * posy
        n += posx2
        n = carte[n]

        posx, posy, posx2, posy2 = pos_x, pos_y - 480, pos_x + 20, pos_y - 460

        posy2 = int(posy2 / 80)
        posx = int(posx / 80)

        p = 32 * posy2
        p += posx
        p = carte[p]

        posx, posy, posx2, posy2 = pos_x, pos_y - 480, pos_x + 20, pos_y - 460

        posy2 = int(posy2 / 80)
        posx2 = int(posx2 / 80)

        o = 32 * posy2
        o += posx2
        o = carte[o]

        if puissance == 1:
            if 2 <= m <= 4 or 2 <= n <= 4 or 2 <= p <= 4 or 2 <= o <= 4:
                stop = 1
        if puissance == 2:
            if 3 <= m <= 4 or 3 <= n <= 4 or 3 <= p <= 4 or 3 <= o <= 4:
                stop = 1
        if puissance == 3:
            if m == 4 or n == 4 or p == 4 or o == 4:
                stop = 1

        # test les collision avec d'autre gems
        for k in range(len(list_gems)):
            posx = list_gems[k].pos_x
            posy = list_gems[k].pos_y

            posx2, posy2, = posx + 20, posy + 20

            if posx < pos_x < posx2 and posy < pos_y < posy2:
                stop = 1
                break
            if posx < pos_x + 20 < posx2 and posy < pos_y < posy2:
                stop = 1
                break
            if posx < pos_x < posx2 and posy < pos_y + 20 < posy2:
                stop = 1
                break
            if posx < pos_x + 20 < posx2 and posy < pos_y + 20 < posy2:
                stop = 1
                break

        if stop == 0:

            # choisit la couleur de la gems
            n = random.randint(1, x)

            if 1 <= n <= 3:
                couleur = orange
                valeur = 15
            if 4 <= n <= 7:
                couleur = violet
                valeur = 30
            if 8 <= n <= 12:
                couleur = verte
                valeur = 50
            if 13 <= n <= 19:
                couleur = bleu
                valeur = 80
            if 20 <= n <= 40:
                couleur = rouge
                valeur = 150

            # crée la gem
            gem = Gems(pos_x, pos_y, valeur, couleur)
            list_gems.append(gem)

    return list_gems


def affichage_gems(fenetre, list_gems, cx, cy, mineur_x):
    # affiche les gemmes a l'écran

    for i in range(len(list_gems)):
        z = mineur_x
        if -20 < list_gems[i].pos_y - cy < 720:

            z += 1280
            if z < 0:
                z = -z
                z += 2560
                x = int(z / 2560)
                x = -x
            else:
                x = int(z / 2560)

            fenetre.blit(list_gems[i].couleur, ((2560 * x) - 2560 + list_gems[i].pos_x - cx, list_gems[i].pos_y - cy))
            fenetre.blit(list_gems[i].couleur, ((2560 * x) + list_gems[i].pos_x - cx, list_gems[i].pos_y - cy))


def collision_gems(list_gems, argent, valeur_gems, ax, ay, bx, by, cx, cy, son_collecter):
    # test les collision du mineur avec les gems

    x = 0
    if ax < 0:
        a_x = -ax
        a_x += 2560
        x = int(a_x / 2560)
        x = -x
    if ax > 2560:
        x = int(ax / 2560)
    ax -= 2560 * x
    x = 0
    if bx < 0:
        b_x = -bx
        b_x += 2560
        x = int(b_x / 2560)
        x = -x
    if bx > 2560:
        x = int(bx / 2560)
    bx -= 2560 * x
    x = 0
    if cx < 0:
        c_x = -cx
        c_x += 2560
        x = int(c_x / 2560)
        x = -x
    if cx > 2560:
        x = int(cx / 2560)
    cx -= 2560 * x

    couleur = 0
    for k in range(len(list_gems)):
        col = 0

        posx = list_gems[k].pos_x
        posy = list_gems[k].pos_y

        posx2, posy2, = posx + 20, posy + 20

        if posx < ax < posx2 and posy < ay < posy2:
            col = 1
        if posx < bx < posx2 and posy < by < posy2:
            col = 1
        if posx < cx < posx2 and posy < cy < posy2:
            col = 1

        if col == 1:
            son_collecter.play()
            argent += list_gems[k].valeur * valeur_gems
            couleur = list_gems[k].valeur
            list_gems.remove(list_gems[k])
            break

    return argent, couleur
