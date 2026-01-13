import re

def menu():
    print("Veuillez rentrer un choix : ")
    print("1 / Calculer" )
    print("2 / Afficher l'historique")
    print("3 / Effacer l'historique")
    choix=(input("Rentrez votre choix : "))
    return choix

def calculer():
    priorite = {'(':0, '+': 1, '-': 1, '*': 2, '/': 2}
    nombres=[]
    operateur=[]
    calcul=input("Veuillez rentrer votre calcul : ")
    liste_calcul = re.findall(r"\d+\.?\d*|[-+*/()]", calcul)
    for i in liste_calcul:
        if i.replace(".", "", 1).isdigit():
            nombres.append(i)

        elif i in priorite:
            while operateur and priorite[operateur[-1]] >= priorite[i]:
                nombres.append(operateur.pop())
            operateur.append(i)
        
        elif i == '(':
            operateur.append(i)
        
        elif i == ')' : 
            while operateur and priorite[operateur[-1]] != '(':
                nombres.append(operateur.pop())
            if operateur:
                operateur.pop()
    
    while operateur:
        nombres.append(operateur.pop())
    
    calcul_final = []
    for i in nombres:
        if i.replace(".", "", 1).isdigit():
            calcul_final.append(float(i))
        else: # On ne calcule QUE si c'est un opérateur
            nb1 = calcul_final.pop() # Chiffre de droite
            nb2 = calcul_final.pop() # Chiffre de gauche

            if i == '+': calcul_final.append(nb2 + nb1)
            elif i == '-': calcul_final.append(nb2 - nb1)
            elif i == '*': calcul_final.append(nb2 * nb1)
            elif i == '/': calcul_final.append(nb2 / nb1)

    return calcul_final[0]

def main():
    choix_menu=menu()
    if choix_menu=="1":
        print(calculer())

main()