import argparse


def analyser_commande():
    #fonction 1: fait appel au module argparse pour traiter la ligne de commande. Elle
    #retourne l'objet produit par la fonction parse_args qui inclue le nom du joueur
    #associé à la clé idul.
    parser = argparse.ArgumentParser(description="Jeu quoridor - Phase 1")
    parser.add_argument('-l', '--lister', action='store_true', 
                        help='Lister les identifiants de vos 20 dernières parties.')
    parser.add_argument('idul', metavar='idul', type=str, help='IDUL du joueur')
    #parser.add_argument('bar', type=str, help='Argument positionnel de la sous-commande acheter')
    return parser.parse_args()

def line_namer(i):
    r = []
    if (((i+1) // 2)+1) < 10:
        r = ["{} |".format(((i+1) // 2) + 1)]
    else:
        r = ["{}|".format(((i+1) // 2) + 1)]
    return r

def afficher_damier_ascii(grille):
    #fonction 2: accepte en argument le dictonnaire d'un état du jeu et affiche
    #le damier correspondant en art ascii.
    grille = {"joueurs": [{"nom": "idul", "murs": 7, "pos":[5, 5]},
                          {"nom": "automate", "murs": 3, "pos": [8, 6]}
                         ],
              "murs": {
                   "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
                   "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7]]
                      }
             }

    positions_grille = 9
    espace_horizontale = ((positions_grille * 4) - 1)
#tableau d'équivalences entre les adresses du jeu et notre tableau
    position_jeu_x = range(1, (positions_grille * 4), 4)
    position_jeu_y = range(((positions_grille - 1) * 2), -1, -2)
#création du tableau de jeu
    légende = "légende: "
    board = [légende]
#grille de jeu
    for i in reversed(range((positions_grille * 2) - 1)):
        if (i % 2) == 0:
            board += line_namer(i)
            board += [' ', '.']
            board += ([' ', ' ', ' ', '.']*(positions_grille - 1))
            board += [' ', '|\n']
        else:
            board += ["  |"]
            board += ([' ']* espace_horizontale)
            board += ['|\n']
#ligne du bas de la grille
    board += "--|" + ('-' * espace_horizontale) + '\n'
#chiffre de la ligne du bas
    board += (' ' * 2) + '| '
    for i in range(1, positions_grille):
        board += str(i) + (' ' * 3)
    board += "{}\n".format(positions_grille)
#ajout des joueurs dans la grille de jeu
    for num, joueur in enumerate(grille["joueurs"]):
        #ajout du joueur à la légende du tableau
        légende += "{}={}".format((num + 1), joueur['nom du joueur'])
        #obtention de la position en [x,y] du joueur
        position = joueur["pos"]
        #vérification que la position est dans les contraintes
        if ((0 > position[0] > positions_grille) or
                (0 > position[1] > positions_grille)):
            raise IndexError("Adresse du joueur invalide!")
    #calcul du décallage relatif au tableau
    indice = (position_jeu_x[(position[0] - 1)]+
              (position_jeu_y[(position[1] - 1)] * espace_horizontale))
    decallage = ((((indice + 1) // espace_horizontale) * 2) + 2)
    indice += decallage
    #insertion du personnage dans le tableau du jeu
    board[indice] = str(num + 1)
    #complétion de la légende du tableau
    board[0] = légende + '\n' + (' ' * 3) + ('-' * espace_horizontale) + '\n'
    #ajout des murs horizontaux dans board
    for murh in grille["murs"]["horizontaux"]:
        #vérification que la position est dans les contraintes
        if ((1 > murh[0] > (positions_grille - 1)) or (2 > murh[1] > positions_grille)):
            raise IndexError("Position du mur horizontal invalide!")
        indice = ((position_jeu_x[(murh[0] - 1)] - 1) +
                  ((position_jeu_y[(murh[1] - 1)] + 1) * espace_horizontale))
        decallage = ((((indice + 1) // espace_horizontale) * 2) + 2)
        indice += decallage
    #itérer pour placer les 5 murs
    for i in range(7):
        board[(indice + i)] = '-'
    #insertion des murs verticaux
    for murv in grille["murs"]["verticaux"]:
        #vérification que la position est dans les contraintes
        if (2 > murv[0] > positions_grille) or (1 > murv[1] > positions_grille):
            raise IndexError("Position du mur vertival invalide!")
        indice = ((position_jeu_x[(murv[0] - 1)] - 2) +
                  ((position_jeu_y[(murv[1] - 1)]) * espace_horizontale))
        decallage = ((((indice + 1) // espace_horizontale) * 2) + 2)
        indice += decallage
        #itérer pour placer les 3 murs
        for i in range(3):
            board[(indice - (i * (espace_horizontale + 2)))] = '|'
    #afficher le jeu sous forme d'une chaîne de caractères
    print(''.join(board))
