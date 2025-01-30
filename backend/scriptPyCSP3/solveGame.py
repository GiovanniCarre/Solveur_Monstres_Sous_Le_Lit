from pydoc import describe

from pycsp3 import *

def rightRotation(grid):
    grid2 = [[0,0,0],[0,0,0],[0,0,0]]
    grid2[1][1] = grid[1][1]
    for i in range(3):
        grid2[0][2-i] = grid[i][0]
        grid2[i][0] = grid[2][i]
        grid2[2][i] = grid[2-i][2]
        grid2[2-i][2] = grid[0][2-i]
    return grid2

def rotate(grid, n):
    for i in range(n):
        grid = rightRotation(grid)
    return flatten(grid)

def creerChambres():
    dispositionVisuelle = [[[0, 1, 2],
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
    chambres = []
    for chambre in dispositionVisuelle:
        chambres.append(flatten(chambre))
    return chambres

def crerMasques() :
    masquesFixes = \
        [[[0, 1, 0],
        [0, 0, 0],
        [0, 1, 0]],

        [[0, 0, 1],
        [0, 0, 0],
        [1, 0, 0]],

        [[0, 1, 0],
        [0, 1, 0],
        [0, 0, 0]],

        [[0, 0, 1],
        [0, 0, 0],
        [0, 1, 0]]]

    masques = []
    for i in range(4):
        for j in range(4):
            tab = rotate(masquesFixes[i], j)
            tab.append(i)
            if not tab in masques :
                masques.append(tab)
    return masques

def afficherSolution(sol):
    print("[")
    for i in range(4):
        description = "["
        for j in range(9):
            description+= str(sol[i][j])+", "
        description = description[:-2]
        if (i == 3):
            print(description+"]")
        else:
            print(description+"],")
    print("]")
if __name__ == "__main__":
    nbCategoriesDeMonstres = 7
    chambres = creerChambres()
    masques = crerMasques()
    nMasques = len(masques)
    nombreMontresObjectif = [0, 0, 0, 2, 0, 0, 0, 3, 0]#3 singes et 2 yetis (essayer aussi [0, 1, 1, 0, 1, 1, 0, 1, 0])

    masquesVar = VarArray(size=[nMasques,10], dom=range(5))
    masquesSelectionnes = VarArray(size=[4,10], dom=range(5))
    selectionMasques = VarArray(size=4, dom=range(nMasques))
    monstresVisibles = VarArray(size=[4,9], dom=range(nbCategoriesDeMonstres+1))
    satisfy(
        (masquesVar[i] == masques[i] for i in range(nMasques)),
        (masquesSelectionnes[i] == masquesVar[selectionMasques[i]] for i in range(4)),
        (AllDifferent([masquesSelectionnes[i][9] for i in range(4)])),
        (monstresVisibles[i][j] == chambres[i][j]*masquesSelectionnes[i][j] for i in range(4) for j in range(9)),
        (Count(monstresVisibles, value=i) == nombreMontresObjectif[i] for i in range(1, nbCategoriesDeMonstres + 1))
    )

    if solve(sols=ALL) is SAT and n_solutions():
        solution = []
        for k in range(1):
            for i in range(4):
                chambre = []
                for j in range(10):
                    chambre.append(value(masquesSelectionnes[i][j], sol=k))
                solution.append(chambre)
            afficherSolution(solution)
    else :
        print("False")
