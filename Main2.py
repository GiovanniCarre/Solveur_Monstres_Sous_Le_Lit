from pycsp3 import *



def countZeros(tableau):
    count = 0
    for masque in tableau:
        for ligne in masque:  # Parcours des lignes de chaque masque
            count += ligne.count(0)
    return count

def constructModel():
    #====================== Paramètres de base =================

    nbCategoriesDeMonstres = 4 #nombre de familles de monstres

    #====================== Variables qui sont "statiques" pour le modèle =======================
    chambres = [
        [[0, 1, 2],
         [3, 0, 4],
         [5, 0, 0]],

        [[1, 6, 0],
         [0, 3, 4],
         [5, 7, 0]],

        [[1, 2, 7],
         [3, 4, 0],
         [7, 6, 8]],

        [[0, 0, 0],
         [6, 1, 8],
         [3, 7, 4]]]

    '''
    vide 0
    champi 1
    dino 2
    yeti 3
    chauvesouris 4
    jaune 5
    rose 6
    singe 7
    doudou 8
    '''

    #Forme des 4 masques => Les 0 correspondent à un masque et 1 c'est des trous
    masquesOriginaux = \
                [[[1, 0, 0],
                 [0, 0, 1],
                 [0, 0, 0]],

                [[0, 0, 1],
                 [0, 0, 0],
                 [1, 0, 0]],

                [[0, 0, 0],
                 [0, 1, 1],
                 [0, 0, 0]],

                [[0, 1, 0],
                 [0, 0, 0],
                 [0, 1, 0]],
                ]


    #Donne le nombre de monstres ATTENTION LA 1ERE CASE EST UNE ABSENCE DE MONSTRE
    nombreMonstresObjectif = [0, 2, 1, 0, 0]

    sommeNombreMonstres = 0
    for i in nombreMonstresObjectif:
        sommeNombreMonstres += i

    #nombre de cases vides dans notre objectif
    nombreMonstresObjectif[0] = 4*3*3 - countZeros(masquesOriginaux) - sommeNombreMonstres
    print("Objectif: ", nombreMonstresObjectif)


    #========================== Variables de la solution =====================================================
    positionMasques = VarArray(size=4, dom=range(4))
    rotationMasques = VarArray(size=4, dom=range(4))


    #============================================= Envoi au modèle ===============================================


    #======================= Contraintes =======================
    #Correspond aux monstres ce qu'on voit
    monstresVisibles = VarArray(size=[4,3,3], dom=range(nbCategoriesDeMonstres+1))
    #print(monstresComptesSurLaCarte[0], " - ", nombreMonstresObjectif[0])

    masquesPlacesTournes = VarArray(size=(4,3,3), dom=range(2))
    print("Nombre de cases vides: ", nombreMonstresObjectif[0])

    #La position des masques doivent être différentes
    satisfy(
        (monstresVisibles[i][j][k] == chambres[i][j][k] * masquesPlacesTournes[i][j][k] for i in range(4) for j in
         range(3) for k in range(3)),
        #Objectif des monstres doivent être bons
        *[Count(monstresVisibles, value=i) == nombreMonstresObjectif[i] for i in range(nbCategoriesDeMonstres+1)],
        #Position des masques différents
        AllDifferent(positionMasques)
    )

    if solve() is SAT:
        print("Fait")

        for i in range(nbCategoriesDeMonstres):
            print(value(positionMasques[i]))
            print(value(rotationMasques[i]))
    else:
        print("Pas fait")

    #On va compter les monstres


if __name__ == "__main__":
    constructModel()