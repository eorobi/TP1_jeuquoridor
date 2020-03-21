import json
import requests


def lister_parties(idul):
    #fonction 3 : permet d'obtenir la liste des dernières parties démarrées ou terminées par le joueur de l'idul. 
    #Accepte en entrée l'idul du joueur dont on souhaite avoir l'historique des partie. 
    #Aucun return mais affiche à la console un json. 
    #paramètre de l'idul: chaîne de caractères associée au dossier du joueur

    url_lister = 'https://python.gel.ulaval.ca/quoridor/api'
    try:
        resultat = requests.get(url_lister, params={'idul': idul})
        if resultat.status_code == 200:
            resultat = resultat.text
            json_var = json.loads(resultat)
            jason_str = json.dumps(json_var, indent=2)
            print(json_var)
        else:
            print("Le GET sur '{}' a produit le code d'erreur {}.".format(
                url_lister, resultat.status_code
            ))
    except RuntimeError as error:
        print(error)

def initialiser_partie(idul):
    #fonction 4: démarre une partie contre le robot du serveur. Elle accepte en entrée l'idul du joueur
    #qui souhaite débuter la partie. Elle retourne un tuple qui contient l'identifiant de la partie et
    #l'état initale du jeu. En cas de message d'erreur: elle soulève une exception de type RuntimeError.
    url_initiale = 'https://python.gel.ulaval.ca/quoridor/api/initialiser/'
    try:
        resultat = requests.post(url_initiale, data = {'idul': idul})
        if resultat.status_code == 200:
            json_res = resultat.json()
            return json_res['id'], json_res['état']
        else:
            print("Le POST sur '{}' a produit le code d'erreur {}".format(
                url_initiale, resultat.status_code
            ))
    except RuntimeError as error:
        print(error)

def jouer_coup(id_partie, type_coup, position):
    #fonction 5: elle permet au joueur de jouer un pion contre le robot du serveur
    #la fonction reçoit en argument 3 choses:
    # 1- id_partie : il s'agit de l'identifant de la partie qui est défini avec la fonction
    #précédente qui permet de débuter une nouvelle partie. 
    # 2- type_coup: il s'agir du type de coup que veut faire le participant: 
    # 'D' pour déplacer le jeton; 'MH' pour déplacer les murs horizontales
    # 'MV' pour déplacer les murs verticales et finalement la position (x, y) du déplacement. 
    #Cette fonction retourne le damier de l'état actuel du jeu. Advenant une erreur de commande
    #la fonction retourne également une exception du type 'RuntimeError'. 
    #Lorsqu'un joueur gagne la partie, celle-ci prend fin et la fonction soulève une exception
    # du type 'StopIteration' avec le nom de la personne gagnante. 
    url_coup = 'https://python.gel.ulaval.ca/quoridor/api/jouer'
    try:
        resultat = requests.post(url_coup, data={
            'id': id_partie, 'type': type_coup, 'position': position
        })
        if resultat.status_code == 200:
            json_res = resultat.json()
            if 'gagnant' in json_res:
                raise StopIteration(json_res['gagnant'])
            elif 'message' in json_res:
                print(json_res['message'])
            else:
                return json_res
        else:
            print("Le POST sur '{}' a produit le code d'erreur{}.".format(
                url_coup, resultat.status_code
            ))
    except RuntimeError as error:
        print(error)
