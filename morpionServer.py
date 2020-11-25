from socket import *


hostname = 'localhost' 
serverPort = 6666
serverAddress=(hostname, serverPort)
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddress)
print ('server is ready to receive')


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
    d = ""
    for i in range(2*n+1):
    	d += "-"
    d += "\n"
    for i in range(n):
        for j in range(n):
            if damier[i][j]==0:
                d += "| "
            if damier[i][j]==1:
                d += "|X"
            if damier[i][j]==2:
                d += "|O"
        d += "|\n"
    for i in range(2*n+1):
        d += "-"
    d += "\n"
    return d


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

 
alias1, clientAddress = serverSocket.recvfrom(1024)
print("Joueur 1 :", alias1.decode(), "a rejoint !")
serverSocket.sendto("S".encode("UTF-8"), clientAddress)
serverSocket.sendto(f"[ En attente du joueur 2 .. ]".encode("UTF-8"), clientAddress)
alias2 = str(input("Entrer votre alias : "))
serverSocket.sendto("S".encode("UTF-8"), clientAddress)
serverSocket.sendto(f"Joueur 2 : {alias2} a rejoint !".encode("UTF-8"), clientAddress)

serverSocket.sendto("S".encode("UTF-8"), clientAddress)
serverSocket.sendto("Quelle taille de damier ? ".encode("UTF-8"), clientAddress)
serverSocket.sendto("R".encode("UTF-8"), clientAddress)
print("[ En attente de", alias1.decode(), ".. ]")
size, clientAddress = serverSocket.recvfrom(1024)
n=int(size.decode())
d=genererDamier(n)
print(afficher(d))
serverSocket.sendto("S".encode("UTF-8"), clientAddress)
serverSocket.sendto(afficher(d).encode("UTF-8"), clientAddress)


gagne=False
joueur=1
nbCasesJouees=0

while gagne==False and nbCasesJouees<n*n:
    while True:
        if joueur == 1:
            serverSocket.sendto("S".encode("UTF-8"), clientAddress)
            serverSocket.sendto("Quelle cases ? ".encode("UTF-8"), clientAddress)
            serverSocket.sendto("R".encode("UTF-8"), clientAddress)
            print("[ En attente de", alias1.decode(), ".. ]")
            message, clientAddress = serverSocket.recvfrom(1024)
            numCases=int(message.decode())
        else:
            serverSocket.sendto("S".encode("UTF-8"), clientAddress)
            serverSocket.sendto(f"[ En attente de {alias2} .. ]".encode("UTF-8"), clientAddress)
            numCases=int(input("Quelle cases ? "))
        if jouer(d,numCases,joueur):
            break

    nbCasesJouees=nbCasesJouees+1
    print(afficher(d))
    serverSocket.sendto("S".encode("UTF-8"), clientAddress)
    serverSocket.sendto(afficher(d).encode("UTF-8"), clientAddress)
    gagne=testGagne(d,numCases,joueur)
    if gagne:
        print("Joueur",joueur,"a gagné !")
        serverSocket.sendto("S".encode("UTF-8"), clientAddress)
        serverSocket.sendto(f"Joueur {joueur} a gagné !".encode("UTF-8"), clientAddress)
        serverSocket.sendto("S".encode("UTF-8"), clientAddress)
        serverSocket.sendto("exit".encode("UTF-8"), clientAddress)
        serverSocket.close()
    if joueur==1:
        joueur=2
    else:
        joueur=1
if nbCasesJouees==n*n and gagne==False:
    print("match nul !")
    serverSocket.sendto("S".encode("UTF-8"), clientAddress)
    serverSocket.sendto("match nul !".encode("UTF-8"), clientAddress)
    serverSocket.sendto("S".encode("UTF-8"), clientAddress)
    serverSocket.sendto("exit".encode("UTF-8"), clientAddress)
    serverSocket.close()