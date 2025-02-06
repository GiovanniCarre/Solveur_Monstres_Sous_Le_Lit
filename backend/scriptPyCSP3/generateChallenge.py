from pycsp3 import *
import json
from pydoc import describe

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
    with open("map/dispositionVisuelle.json", "r") as fichier:
                dispositionVisuelle = json.load(fichier)
    chambres = []
    for chambre in dispositionVisuelle:
        chambres.append(flatten(chambre))
    return chambres

def crerMasques() :
    with open("map/masquesFixes.json", "r") as fichier:
            masquesFixes = json.load(fichier)


    masques = []
    for i in range(4):
        for j in range(4):
            tab = rotate(masquesFixes[i], j)
            tab.append(i)
            if not tab in masques :
                masques.append(tab)
    return masques

def afficherSolution(sol):
    for i in range(4):
        description = "Sur la chambre " + str(i) + " est placé le masque " + str(sol[i][9]) + " :"
        for j in range(9):
            if (j%3==0) :
                description+="\n"
            description+= str(sol[i][j])+", "
        description = description[:-2]
        print(description)
    print("\n")

def afficherDefi(defi) :
    description = ""
    for i in range(1,len(defi)) :
        description += str(defi[i])+", "
    print(description[:-2])

def defiRealisable(defi):
    unpost()
    satisfy(monstresVisiblesCategorie[i] == defi[i] for i in range(1, nbCategoriesDeMonstres + 1))
    if solve(sols=ALL) is SAT :
        return (n_solutions() == 1)
    return False

def hashDefi(defi) :
    result = ""
    for i in range(len(defi)) :
        result += str(defi[i])+","
    return result

def compterDefis(defis) :
    comptage = {}
    for defi in defis :
        if hashDefi(defi) in comptage :
            comptage[hashDefi(defi)] += 1
        else :
            comptage[hashDefi(defi)] = 1
    return comptage

if __name__ == "__main__":
    nbCategoriesDeMonstres = 8
    chambres = creerChambres()
    masques = crerMasques()
    nMasques = len(masques)

    masquesVar = VarArray(size=[nMasques,10], dom=range(5))
    masquesSelectionnes = VarArray(size=[4,10], dom=range(5))
    selectionMasques = VarArray(size=4, dom=range(nMasques))
    monstresVisibles = VarArray(size=[4,9], dom=range(nbCategoriesDeMonstres+1))
    monstresVisiblesCategorie = VarArray(size = nbCategoriesDeMonstres+1, dom=range(36))
    satisfy(
        (masquesVar[i] == masques[i] for i in range(nMasques)),
        (masquesSelectionnes[i] == masquesVar[selectionMasques[i]] for i in range(4)),
        (AllDifferent([masquesSelectionnes[i][9] for i in range(4)])),
        (monstresVisibles[i][j] == chambres[i][j]*masquesSelectionnes[i][j] for i in range(4) for j in range(9)),
        (Count(monstresVisibles, value=i) == monstresVisiblesCategorie[i] for i in range(1, nbCategoriesDeMonstres + 1))
    )
    solutions = []
    defis = []
    if solve(sols=ALL) is SAT and n_solutions():
        #print("SAT avec ", n_solutions(), " solutions")
        for k in range(n_solutions()):
            solution = []
            for i in range(4):
                chambre = []
                for j in range(10):
                    chambre.append(value(masquesSelectionnes[i][j], sol=k))
                solution.append(chambre)
            solutions.append(solution)
            defi = []
            for i in range(nbCategoriesDeMonstres+1) :
                defi.append(value(monstresVisiblesCategorie[i], sol=k))
            defis.append(defi)

    nonRealisables = 0
    defisRealisable = []
    compteDefis = compterDefis(defis)
    for i, defi in enumerate(defis):
        if compteDefis[hashDefi(defi)] == 1:
            defisRealisable.append(defi)
            #afficherDefi(defi)
            #afficherSolution(solution)
        else :
            nonRealisables += 1
            #afficherDefi(defis[i])
            #afficherSolution(solution)

    print("[")
    for i in range(len(defisRealisable)):
        print("[")
        afficherDefi(defisRealisable[i])
        if i >= len(defisRealisable)-1:
            print("]")
        else:
            print("],")
    print("]")
