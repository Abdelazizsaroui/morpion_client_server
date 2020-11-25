
def genererDamier(n):
    damier=[]
    for i in range(n):
        ligne=[]
        for j in range(n):
            ligne.append(0)
        damier.append(ligne)
    return damier

def afficher(damier):
    n=len(damier)
    for i in range(2*n+1):
        print('-',end='')
    print()
    for i in range(n):
        for j in range(n):
            if damier[i][j]==0:
                print("| ",end='')
            if damier[i][j]==1:
                print("|X",end='')
            if damier[i][j]==2:
                print("|O",end='')
        print("|")
    for i in range(2*n+1):
        print('-',end='')
    print()

def jouer(damier, numCase, joueur):
    n=len(damier)
    numCase
    if numCase<1 or numCase>n*n or damier[(numCase-1)//n][(numCase-1)%n]!=0:
        return False
    else:
        damier[(numCase-1)//n][(numCase-1)%n]=joueur
        return True

def combienDansLaDirection(damier, numCase, delta_l, delta_c, joueur):
    combien=0;
    n=len(damier)
    lig=(numCase-1)//n
    col=(numCase-1)%n
    while (lig>=0 and lig<n and col>=0 and col<n):
        if (damier[lig][col]!=joueur):
            return combien
        if ((lig+delta_l)<0 or (lig+delta_l)>=n or (col+delta_c)<0 or (col+delta_c)>=n):
            return combien
        if (damier[lig+delta_l][col+delta_c]==joueur):
            combien=combien+1
        lig=lig+delta_l
        col=col+delta_c
    return combien

def testGagne(damier, numCase, joueur):
    gagne=False
    if (combienDansLaDirection(damier, numCase, 0, -1, joueur)+combienDansLaDirection(damier, numCase, 0, 1, joueur) >=2):
        gagne=True
    if (combienDansLaDirection(damier, numCase, -1, 0, joueur)+combienDansLaDirection(damier, numCase, 1, 0, joueur) >=2):
        gagne=True
    if (combienDansLaDirection(damier, numCase, -1, -1, joueur)+combienDansLaDirection(damier, numCase, 1, 1, joueur) >=2):
        gagne=True
    if (combienDansLaDirection(damier, numCase, 1, -1, joueur)+combienDansLaDirection(damier, numCase, -1, 1, joueur) >=2):
        gagne=True
    return gagne


n=int(input("Quelle taille de damier"))
d=genererDamier(n)
afficher(d)

gagne=False
joueur=1
nbCasesJouees=0

while gagne==False and nbCasesJouees<n*n:
    while True:
        numCases=int(input("Quelle cases ? "))
        if jouer(d,numCases,joueur):
            break

    nbCasesJouees=nbCasesJouees+1
    afficher(d)
    gagne=testGagne(d,numCases,joueur)
    if gagne:
        print("Joueur",joueur,"a gagné !")
    if joueur==1:
        joueur=2
    else:
        joueur=1
if nbCasesJouees==n*n and gagne==False:
    print("match nul !")