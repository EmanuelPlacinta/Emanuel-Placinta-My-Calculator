import re
from collections import deque
import os
import time

# L'historique doit être défini à l'extérieur pour être accessible partout
historique = deque(maxlen=10)

def menu():
    print("\n--- MENU ---")
    print("1 / Calculer" )
    print("2 / Afficher l'historique")
    print("3 / Effacer l'historique")
    print("4 / Quitter")
    choix = input("Rentrez votre choix : ")
    return choix

def afficher_historique():
    os.system('clear')
    if not historique:
        print("Aucun calcul dans l'historique")
        time.sleep(2)
        os.system('clear')
    else:
        os.system('clear')
        print("\n--- Historique (10 derniers) ---")
        for i, (c, r) in enumerate(historique, 1):
            print(f"{i}. {c} = {r}")
        input("Appuyer sur entrée pour continuer...")

def calculer(expression_a_calculer): # On donne un nom clair à l'entrée
    priorite = {'(':0, '+': 1, '-': 1, '*': 2, '/': 2, '**':3, 'v':5}
    nombres = []
    operateur = []
    
    # Utilisation de l'expression passée en argument
    liste_calcul = re.findall(r"v|\d+\.?\d*|[-+*/()]", expression_a_calculer)
    
    for index, i in enumerate(liste_calcul):
        if i.replace(".", "", 1).isdigit():
            nombres.append(i)

        elif i == '-':
            # Cas 1 : Le calcul commence par "-" (ex: -5 + 2)
            # Cas 2 : Le "-" est juste après une parenthèse (ex: 5 * (-2))
            if index == 0 or liste_calcul[index-1] == '(':
                nombres.append('0') # On insère un 0 virtuel
            
            # Puis on traite le "-" comme un opérateur normal
            while operateur and priorite[operateur[-1]] >= priorite[i]:
                nombres.append(operateur.pop())
            operateur.append(i)       

        elif i == '(':
            operateur.append(i)

        elif i == ')': 
            while operateur and operateur[-1] != '(':
                nombres.append(operateur.pop())
            if operateur:
                operateur.pop()

        elif i in priorite:
            while operateur and priorite[operateur[-1]] >= priorite[i]:
                nombres.append(operateur.pop())
            operateur.append(i)
    
    while operateur:
        symbole = operateur.pop()
        if symbole != '(':
            nombres.append(symbole)
    
    # Calcul final
    calcul_final = []
    for i in nombres:

        if i.replace(".", "", 1).isdigit():
            calcul_final.append(float(i))
        else: 
            nb1 = calcul_final.pop()
            if i == 'v':
                calcul_final.append(nb1**0.5)
            else :
                nb2 = calcul_final.pop()

            if i == '+': calcul_final.append(nb2 + nb1)
            elif i == '-': calcul_final.append(nb2 - nb1)
            elif i == '*': calcul_final.append(nb2 * nb1)
            elif i == '/': calcul_final.append(nb2 / nb1)
            elif i == '**': calcul_final.append(nb2**nb1)

    return calcul_final[0]

def main():
    while True: # La boucle englobe tout le menu
        os.system('clear')
        choix_menu = menu()
        
        if choix_menu == "1":
            saisie = input("Veuillez rentrer votre calcul : ")
            try:
                resultat = calculer(saisie)
                print(f"Résultat : {resultat}")
                input("Appuyez sur entrée pour continuer...")
                historique.append((saisie, resultat)) # On ajoute directement à la deque
            except Exception as e:
                print(f"Erreur dans le calcul : {e}")
            
        elif choix_menu == "2":
            afficher_historique()
            
        elif choix_menu == "3":
            historique.clear()
            print("Historique effacé")
            
        elif choix_menu == "4":
            print("Au revoir !")
            break

if __name__ == "__main__":
    main()