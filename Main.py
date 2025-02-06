from pycsp3 import *
from pyscipopt import Model



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
    nombreMonstresObjectif = [0,2,1,0,0]

    sommeNombreMonstres = 0
    for i in nombreMonstresObjectif:
        sommeNombreMonstres += i

    #nombre de cases vides dans notre objectif
    nombreMonstresObjectif[0] = nombreDeZero - sommeNombreMonstres



    #========================== Variables de la solution =====================================================
    positionMasques = VarArray(size=4, dom=range(4))
    rotationMasques = VarArray(size=4, dom=range(4))




    #============================================= Envoi au modèle ===============================================

    #Création du modèle
    model = Model("Exemple")
    #model.printStatistics()



    #======================= Contraintes =======================
    #Correspond aux monstres ce qu'on voit
    monstresVisibles = VarArray(size=[4,3,3], dom=range(nbCategoriesDeMonstres+1))
    monstresComptesSurLaCarte = VarArray(size=[nbCategoriesDeMonstres+1])
    #print(monstresComptesSurLaCarte[0], " - ", nombreMonstresObjectif[0])

    #La position des masques doivent être différentes
    satisfy(
        #Ici il faut vérifierque que monstresComptesSurLaCarte[0] == nombreMonstresObjectif[0]*
        AllDifferent(positionMasques)
    )

    #On va compter les monstres

    return locals()


#Affiche le résultat sous forme 2D
def printSolution(model):
    pass



if __name__ == "__main__":
    model = constructModel()
    #print(model)