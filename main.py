from fonctions import (
    evaluer_expression,
    ajouter_historique,
    obtenir_historique,
    effacer_historique,
)

def afficher_menu() -> None:
    print("\n=== Calculatrice Python ===")
    print("1. Calculer une expression")
    print("2. Afficher l'historique")
    print("3. Effacer l'historique")
    print("4. Quitter")

def boucle_principale() -> None:
    while True:
        afficher_menu()
        choix = input("Votre choix : ").strip()

        if choix == "1":
            expr = input("Entrez une expression (ex: 2+3*(4-1)) : ").strip()
            try:
                resultat = evaluer_expression(expr)
                print(f"Résultat : {resultat}")
                ajouter_historique(expr, str(resultat))
            except Exception as e:
                print(f"Erreur : {e}")

        elif choix == "2":
            hist = obtenir_historique()
            if not hist:
                print("Historique vide.")
            else:
                print("\n--- Historique ---")
                for ligne in hist:
                    print(ligne)

        elif choix == "3":
            confirmation = input(
                "Effacer tout l'historique ? (o/n) : "
            ).lower()
            if confirmation == "o":
                effacer_historique()
                print("Historique effacé.")

        elif choix == "4":
            print("Au revoir.")
            break

        else:
            print("Choix invalide, veuillez réessayer.")


if __name__ == "__main__":
    boucle_principale()
