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
    chambres = [[[3, 3, 3],
                 [3, 3, 3],
                 [3, 3, 3]],

                [[3, 3, 3],
                 [3, 3, 3],
                 [3, 3, 3]],

                [[3, 3, 3],
                 [3, 3, 3],
                 [3, 3, 3]],

                [[3, 3, 3],
                 [3, 3, 3],
                 [3, 3, 3]],
                ]


    #Forme des 4 masques => Les 0 correspondent à un masque et 1 c'est des trous
    masquesOriginaux = \
                [[ [1, 0, 0],
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


    nombreDeZero = countZeros(masquesOriginaux)
    #Donne le nombre de monstres ATTENTION LA 1ERE CASE EST UNE ABSENCE DE MONSTRE
    nombreMontresObjectif = [0,2,1,0,0]

    sommeNombreMonstres = 0
    for i in nombreMontresObjectif:
        sommeNombreMonstres += i

    #nombre de cases vides dans notre objectif
    nombreMontresObjectif[0] = nombreDeZero - sommeNombreMonstres



    #========================== Variables de la solution =====================================================
    positionMasques = VarArray(size=4, dom=range(4))
    rotationMasques = VarArray(size=4, dom=range(4))




    #============================================= Envoi au modèle ===============================================




    #======================= Contraintes =======================
    #Correspond aux monstres ce qu'on voit
    monstresVisibles = VarArray(size=[4,3,3], dom=range(nbCategoriesDeMonstres+1))
    #print(monstresComptesSurLaCarte[0], " - ", nombreMontresObjectif[0])

    #La position des masques doivent être différentes
    satisfy(
        #Objectif des monstres doivent être bons
        *[Count(monstresVisibles, value=i) == nombreMontresObjectif[i] for i in range(nbCategoriesDeMonstres+1)],
        #Position des masques différents
        AllDifferent(positionMasques)
    )

    if solve() is SAT:
        print("Fait")

    #On va compter les monstres








if __name__ == "__main__":
    constructModel()