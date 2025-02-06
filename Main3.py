from pycsp3 import *

def countZeros(tableau):
    count = 0
    for masque in tableau:
        for ligne in masque:
            count += ligne.count(0)
    return count

def rightRotation(grid):
    grid2 = grid.copy()
    grid2[1][1] = grid[1][1]
    for i in range(3):
        grid2[i][0] = grid[0][3-i]
        grid2[2][i] = grid[i][0]
        grid2[3-i][2] = grid[2][i]
        grid2[0][3-i] = grid[3-i][2]
    return grid2

def rotate(grid, n):
    for i in range(n):
        grid = rightRotation(grid)
    return grid

if __name__ == "__main__":
    nbCategoriesDeMonstres = 4
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


    nombreMonstresObjectif = [5,2,1,0,0]
    sommeNombreMonstres = 0
    for i in nombreMonstresObjectif:
        sommeNombreMonstres += i
    #nombre de cases vides dans notre objectif
    nombreMonstresObjectif[0] = countZeros(masquesOriginaux) + nombreMonstresObjectif[0]


    nombreMonstresObjectif[0] = nombreDeZero - sommeNombreMonstres
    print("Nombre de cases vides: ",nombreMonstresObjectif[0])
    positionMasques = VarArray(size=4, dom=range(4))
    rotationMasques = VarArray(size=4, dom=range(4))
    masquesPlaces = VarArray(size=(4,3,3), dom=range(2))
    masquesPlacesTournes = VarArray(size=(4,3,3), dom=range(2))

    monstresVisibles = VarArray(size=[4,3,3], dom=range(1,nbCategoriesDeMonstres+1))
    satisfy((Count(monstresVisibles, value=i) == nombreMonstresObjectif[i] for i in range(1,nbCategoriesDeMonstres+1)))
    satisfy(
        (masquesPlacesTournes[i] == rotate(masquesPlaces[i], rotationMasques[i]) for i in range(4)),
        (monstresVisibles[i][j][k] == chambres[i][j][k]*masquesPlacesTournes[i][j][k] for i in range(4) for j in range(3) for k in range(3)),
        AllDifferent(positionMasques)
    )

    #Je veux que tu affiches toutes les contraintes
    if solve() is SAT:
        for i in range(nbCategoriesDeMonstres):
            print(value(positionMasques[i]))
        print("SAT")
    else :
        print("UNSAT")
