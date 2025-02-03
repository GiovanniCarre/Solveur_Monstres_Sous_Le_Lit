from pydoc import describe

from pycsp3 import *

def afficherSolution(sol):
    for i in range(4):
        description = "Chambre " + str(i) + " :"
        for j in range(9):
            if (j%3==0) :
                description+="\n"
            description+= str(sol["plateau"][i][j])+"("+str(sol["masques"][i][j])+"),  "
        description = description[:-2]
        print(description)
    print("\n\n")

def afficherDefi(defi) :
    description = "defi : "
    for i in range(len(defi)) :
        description += str(defi[i])+", "
    print(description[:-2])

def defiRealisable(defi):
    unpost()
    satisfy(monstresVisiblesCategorie[i] == defi[i] for i in range(1, nbCategoriesDeMonstres + 1))
    if solve(sols=ALL) is SAT :
        return (n_solutions() == 1)
    return False

if __name__ == "__main__":
    nbCategoriesDeMonstres = 8
    nMasques = 4
    nombreMontresObjectif = [0, 0, 2, 0, 0, 0, 3, 0]#3 singes et 2 yetis (essayer aussi [0, 1, 1, 0, 1, 1, 0, 1, 0])

    masquesSelectionnes = VarArray(size=[4,9], dom=range(2))
    monstresVisibles = VarArray(size=[4,9], dom=range(nbCategoriesDeMonstres+1))
    monstresVisiblesCategorie = VarArray(size = nbCategoriesDeMonstres, dom=range(36))
    chambresVar = VarArray(size=[4,9], dom=range(nbCategoriesDeMonstres+1))
    satisfy(
        (monstresVisibles[i][j] == chambresVar[i][j]*masquesSelectionnes[i][j] for i in range(4) for j in range(9)),
        (Count(monstresVisibles, value=i+1) == monstresVisiblesCategorie[i] for i in range(nbCategoriesDeMonstres)),
        (monstresVisiblesCategorie[i] == nombreMontresObjectif[i] for i in range(nbCategoriesDeMonstres))
    )
    solutions = []
    defis = []
    if solve(sols=10) is SAT and n_solutions():
        print("SAT avec ", n_solutions(), " solutions")
        for k in range(n_solutions()):
            solution = {"plateau" : [], "masques" : []}
            for i in range(4):
                chambrePlateau = []
                chambreMasque = []
                for j in range(10):
                    chambrePlateau.append(value(chambresVar[i][j], sol=k))
                    chambreMasque.append(value(masquesSelectionnes[i][j], sol=k))
                solution["plateau"].append(chambrePlateau)
                solution["masques"].append(chambreMasque)
            solutions.append(solution)
            defi = []
            for i in range(nbCategoriesDeMonstres+1) :
                defi.append(value(monstresVisiblesCategorie[i], sol=k))
            defis.append(defi)
            afficherSolution(solution)
    else :
        print("UNSAT")
