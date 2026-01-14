from typing import List

# ================== HISTORIQUE ==================

historique: List[str] = []

def ajouter_historique(entree: str, resultat: str) -> None:
    """Ajoute une opération formatée à l'historique."""
    ligne = f"{entree} = {resultat}"
    historique.append(ligne)

def obtenir_historique() -> List[str]:
    """Retourne une copie de l'historique."""
    return list(historique)

def effacer_historique() -> None:
    """Efface tout l'historique."""
    historique.clear()

# ================== CALCUL DE BASE SANS EVAL ==================

def addition(a: float, b: float) -> float:
    return a + b

def soustraction(a: float, b: float) -> float:
    return a - b

def multiplication(a: float, b: float) -> float:
    return a * b

def division(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Division par zéro interdite.")
    return a / b

OPERATEURS = {
    "+": addition,
    "-": soustraction,
    "*": multiplication,
    "/": division,
}

def calculer_2_nombres(a: float, op: str, b: float) -> float:
    """Calcule a op b en vérifiant l'opérateur."""
    if op not in OPERATEURS:
        raise ValueError(f"Opérateur inconnu : {op}")
    return OPERATEURS[op](a, b)

def tokenizer(expression: str) -> List[str]:
    """Transforme '2+3*(4-1)' en ['2','+','3','*','(','4','-','1',')']."""
    tokens: List[str] = []
    courant = ""

    for ch in expression.replace(" ", ""):
        if ch.isdigit() or ch == ".":
            courant += ch
        elif ch in "+-*/()":
            if courant:
                tokens.append(courant)
                courant = ""
            tokens.append(ch)
        else:
            raise ValueError(f"Caractère invalide : {ch}")

    if courant:
        tokens.append(courant)

    if not tokens:
        raise ValueError("Expression vide.")
    return tokens  # [web:37]

def appliquer_operateur(op: str, a: float, b: float) -> float:
    return calculer_2_nombres(a, op, b)

def evaluer_expression(expression: str) -> float:
    """
    Évalue une expression avec + - * /, décimaux et parenthèses,
    en respectant la priorité * et / avant + et -.
    Exemple : '2+3*4' -> 14, '2*(3+4)' -> 14.
    """
    tokens = tokenizer(expression)

    # Utilisation d'une variante simple de shunting-yard + évaluation en RPN [web:37]
    # 1) Conversion en notation postfixée (RPN)
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
    output: List[str] = []
    op_stack: List[str] = []

    for token in tokens:
        if token.replace(".", "", 1).isdigit():
            output.append(token)
        elif token in precedence:
            while (
                op_stack
                and op_stack[-1] in precedence
                and precedence[op_stack[-1]] >= precedence[token]
            ):
                output.append(op_stack.pop())
            op_stack.append(token)
        elif token == "(":
            op_stack.append(token)
        elif token == ")":
            # dépiler jusqu'à "("
            while op_stack and op_stack[-1] != "(":
                output.append(op_stack.pop())
            if not op_stack:
                raise ValueError("Parenthèses non équilibrées.")
            op_stack.pop()  # enlever "("
        else:
            raise ValueError(f"Token inattendu : {token}")

    while op_stack:
        top = op_stack.pop()
        if top in ("(", ")"):
            raise ValueError("Parenthèses non équilibrées.")
        output.append(top)

    # 2) Évaluation de la RPN
    pile_eval: List[float] = []
    for token in output:
        if token in precedence:
            try:
                b = pile_eval.pop()
                a = pile_eval.pop()
            except IndexError:
                raise ValueError("Expression invalide (opérande manquant).")
            pile_eval.append(appliquer_operateur(token, a, b))
        else:
            try:
                pile_eval.append(float(token))
            except ValueError:
                raise ValueError(f"Nombre invalide : {token}")

    if len(pile_eval) != 1:
        raise ValueError("Expression invalide (reste des valeurs en pile).")

    return pile_eval[0]

# ================== OUTILS NUMÉRIQUES SANS MATH ==================

# approximation de pi (suffisant pour de la trigo "calculatrice")
PI = 3.141592653589793

def puissance(x: float, n: int) -> float:
    """x**n pour n entier (rapide, exponentiation rapide)."""
    if n < 0:
        return 1.0 / puissance(x, -n)
    resultat = 1.0
    base = x
    exposant = n
    while exposant > 0:
        if exposant % 2 == 1:
            resultat *= base
        base *= base
        exposant //= 2
    return resultat

def factorielle(n: int) -> float:
    if n < 0:
        raise ValueError("factorielle définie pour n >= 0.")
    res = 1.0
    for k in range(2, n + 1):
        res *= k
    return res

def degres_vers_radians(a: float) -> float:
    return a * (PI / 180.0)

def racine_carre(a: float) -> float:
    """Racine carrée via la méthode de Newton."""
    if a < 0:
        raise ValueError("Racine carrée d'un nombre négatif interdite.")
    if a == 0:
        return 0.0
    x = a / 2.0
    # quelques itérations suffisent pour de la calculatrice
    for _ in range(20):
        x = 0.5 * (x + a / x)
    return x

def sinus_rad(x: float) -> float:
    """sinus en radians via série de Taylor."""
    # réduction de l'angle dans [-pi, pi] pour limiter l'erreur
    x = ((x + PI) % (2 * PI)) - PI
    res = 0.0
    signe = 1.0
    # 10 termes -> précision correcte pour usage basique
    for n in range(10):
        num = puissance(x, 2 * n + 1)
        den = factorielle(2 * n + 1)
        res += signe * num / den
        signe *= -1.0
    return res

def cosinus_rad(x: float) -> float:
    """cosinus en radians via série de Taylor."""
    x = ((x + PI) % (2 * PI)) - PI
    res = 0.0
    signe = 1.0
    for n in range(10):
        num = puissance(x, 2 * n)
        den = factorielle(2 * n)
        res += signe * num / den
        signe *= -1.0
    return res

def tangente_rad(x: float) -> float:
    c = cosinus_rad(x)
    if c == 0:
        raise ValueError("Tangente non définie pour cet angle.")
    return sinus_rad(x) / c

def ln(a: float) -> float:
    """
    Approximation de ln(a) par méthode de Newton sur exp.
    Suffisant pour une calculatrice scientifique simple.
    """
    if a <= 0:
        raise ValueError("ln défini seulement pour a > 0.")

    # exp(x) ~ série de Taylor
    def exp(x: float) -> float:
        s = 0.0
        for n in range(20):
            s += puissance(x, n) / factorielle(n)
        return s

    # recherche initiale grossière
    x = 0.0
    # quelques itérations de Newton : x_{n+1} = x_n + a/exp(x_n) - 1
    for _ in range(30):
        ex = exp(x)
        x = x + (a / ex) - 1.0
    return x

def log10_impl(a: float) -> float:
    """log base 10 en utilisant ln(a) / ln(10)."""
    ln10 = ln(10.0)
    return ln(a) / ln10

# ================== PARTIE SCIENTIFIQUE (UNE VALEUR) ==================

def sinus_deg(a: float) -> float:
    """sinus en degrés."""
    return sinus_rad(degres_vers_radians(a))

def cosinus_deg(a: float) -> float:
    return cosinus_rad(degres_vers_radians(a))

def tangente_deg(a: float) -> float:
    return tangente_rad(degres_vers_radians(a))

def logarithme_base_e(a: float) -> float:
    return ln(a)

def logarithme_base_10(a: float) -> float:
    return log10_impl(a)
