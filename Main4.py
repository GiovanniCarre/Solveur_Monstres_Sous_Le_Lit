from pydoc import describe

from pycsp3 import *

def countZeros(tableau):
    count = 0
    for masque in tableau:
        for ligne in masque:
            count += ligne.count(0)
    return count

def rightRotation(grid):
    grid2 = [[0,0,0],[0,0,0],[0,0,0]]
    grid2[1][1] = grid[1][1]
    for i in range(3):
        grid2[0][2-i] = grid[i][0]
        grid2[i][0] = grid[2][i]
        grid2[2][i] = grid[2-i][2]
        grid2[2-i][2] = grid[0][2-i]
    return grid2

def display(grid):
    for ligne in grid:
        print(ligne)
    print("")

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

def crerMasquesOriginaux() :
    masquesOriginauxFixes = \
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

    masquesOriginaux = []
    for i in range(4):
        for j in range(4):
            tab = rotate(masquesOriginauxFixes[i], j)
            tab.append(i)
            masquesOriginaux.append(tab)

    return masquesOriginaux, countZeros(masquesOriginauxFixes)

def fonctionDeDorian(objectif):
    sommeNombreMonstres = 0
    for i in objectif:
        sommeNombreMonstres += i
    objectif[0] = nMasquesOrginauxFixes + objectif[0]
    print("Nombre de cases vides: ", objectif[0])

def afficherSolution(sol):
    #print(sol)
    for i in range(4):
        description = "Le masque " + str(i) + " est placé sur la chambre " + str(sol[i]["position"]) + " et est de la forme :"
        for j in range(9):
            if (j%3==0) :
                description+="\n"
            description+= str(sol[i]["rotations"][j])+", "
        description = description[:-2]
        print(description)

if __name__ == "__main__":
    nbCategoriesDeMonstres = 7
    chambres = creerChambres()

    masquesOriginaux, nMasquesOrginauxFixes = crerMasquesOriginaux()
    nMasques = len(masquesOriginaux)
    nombreMontresObjectif = [0, 0, 0, 2, 0, 0, 0, 3, 0]#3 singes et 2 yetis (essayer aussi [0, 1, 1, 0, 1, 1, 0, 1, 0])

    #fonctionDeDorian(nombreMontresObjectif)

    positionMasques = VarArray(size=4, dom=range(4))
    selectionMasques = VarArray(size=4, dom=range(nMasques))
    masquesOriginauxVar = VarArray(size=[nMasques,10], dom=range(5))
    masquesSelectionnes = VarArray(size=[4,10], dom=range(5))
    monstresVisibles = VarArray(size=[4,9], dom=range(nbCategoriesDeMonstres+1))
    satisfy(
        (masquesOriginauxVar[i] == masquesOriginaux[i] for i in range(nMasques)),
        (masquesSelectionnes[i] == masquesOriginauxVar[selectionMasques[i]] for i in range(4)),
        (positionMasques[i] == masquesSelectionnes[i][9] for i in range(4)),
        (monstresVisibles[i][j] == chambres[i][j]*masquesSelectionnes[i][j] for i in range(4) for j in range(9)),
        (AllDifferent(positionMasques)),
        (Count(monstresVisibles, value=i) == nombreMontresObjectif[i] for i in range(1, nbCategoriesDeMonstres + 1))
    )

    solutions = []
    nSolutionsTrouves = 0
    maxSolutions = 3
    while solve() is SAT and nSolutionsTrouves < maxSolutions:
        nSolutionsTrouves += 1
        solution = []
        for i in range(4):
            masque = {}
            masque["position"]=i
            masque["rotations"] = []
            for j in range(9):
                masque["rotations"].append(value(monstresVisibles[i][j]))
            solution.append(masque)
        if (solution in solutions) :
            print("SAT, solution déjà trouvée")
        else :
            print("SAT")
            solutions.append(solution)

    print("\n--- AFFICHAGE DES SOLUTIONS ---")
    for i, sol in enumerate(solutions) :
        print("Solution "+str(i)+" : ")
        afficherSolution(sol)
        print("\n")
