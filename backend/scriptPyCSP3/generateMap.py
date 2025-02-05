from pydoc import describe
from pycsp3 import *
import json
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
    monster_data = json.loads(sys.argv[1])
    nbCategoriesDeMonstres = 8
    nMasques = 4
    nombreMontresObjectif = monster_data

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
    if solve(sols=1) is SAT and n_solutions():
        for k in range(n_solutions()):
            solution = {"plateau" : [], "masques" : []}
            for i in range(4):
                chambrePlateau = []
                chambreMasque = []
                for j in range(9):
                    typeMonstre = value(chambresVar[i][j], sol=k)
                    if typeMonstre == 0 :
                        chambrePlateau.append(0)
                    else :
                        chambrePlateau.append(typeMonstre+1)
                    chambreMasque.append(value(masquesSelectionnes[i][j], sol=k))
                solution["plateau"].append(chambrePlateau)
                solution["masques"].append(chambreMasque)
            solutions.append(solution)
            json_format = json.dumps(solution)

            print(solution)
    else :
        print("False")
