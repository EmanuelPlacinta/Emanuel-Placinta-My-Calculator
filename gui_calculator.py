import customtkinter as ctk
from tkinter import messagebox  # messagebox reste pratique

from fonctions import (
    evaluer_expression,
    ajouter_historique,
    obtenir_historique,
    effacer_historique,
    racine_carre,
    sinus_deg,
    cosinus_deg,
    tangente_deg,
    logarithme_base_e,
    logarithme_base_10,
    PI,  # on récupère PI depuis fonctions.py
)

# Apparence globale
ctk.set_appearance_mode("dark")       # "dark" ou "light"
ctk.set_default_color_theme("blue")   # "blue", "green", "dark-blue", etc.

class CalculatriceCTk(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculatrice Python (CustomTkinter)")
        # hauteur augmentée pour éviter que les boutons soient tassés
        self.geometry("600x480")
        self.resizable(False, False)

        # Configuration du grid principal
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        self._creer_widgets()

    def _creer_widgets(self):
        # ====== Zone d'affichage ======
        self.entry = ctk.CTkEntry(
            self,
            width=260,
            height=60,
            font=("Consolas", 24),
            justify="right",
        )
        self.entry.grid(row=0, column=0, columnspan=1, padx=15, pady=15, sticky="nsew")

        # ====== Boutons clear (C / CE) juste sous l'entry ======
        clear_frame = ctk.CTkFrame(self, fg_color="transparent")
        clear_frame.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="nsew")

        clear_frame.grid_columnconfigure((0, 1), weight=1)

        # C = effacer tout le champ
        ctk.CTkButton(
            clear_frame,
            text="C",
            fg_color="#ffb703",
            hover_color="#ff9f1c",
            command=self._clear_all,
        ).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # CE = effacer seulement le dernier caractère
        ctk.CTkButton(
            clear_frame,
            text="CE",
            fg_color="#fb5607",
            hover_color="#e85d04",
            command=self._clear_last_char,
        ).grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # ====== Zone d'historique ======
        self.history_frame = ctk.CTkFrame(self, corner_radius=15)
        self.history_frame.grid(row=0, column=1, rowspan=8, padx=(5, 15), pady=15, sticky="nsew")

        history_label = ctk.CTkLabel(
            self.history_frame,
            text="Historique",
            font=("Arial", 14, "bold")
        )
        history_label.pack(pady=(10, 5))

        self.history_box = ctk.CTkTextbox(
            self.history_frame,
            width=220,
            height=360,
            font=("Consolas", 11),
        )
        self.history_box.pack(padx=10, pady=5, fill="both", expand=True)

        buttons_hist_frame = ctk.CTkFrame(self.history_frame, fg_color="transparent")
        buttons_hist_frame.pack(pady=(5, 10))

        # Bouton "Effacer" l'historique
        self.btn_clear_hist = ctk.CTkButton(
            buttons_hist_frame,
            text="Effacer",
            fg_color="#b81818",
            hover_color="#8a1010",
            width=90,
            command=self._effacer_historique_gui,
        )
        self.btn_clear_hist.pack(side="left", padx=5)

        # ====== Boutons de base (pavé numérique + opérateurs) ======
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, rowspan=3, padx=15, pady=(0, 5), sticky="nsew")

        btn_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        btn_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        boutons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
            ("0", 3, 0), (".", 3, 1), ("=", 3, 2), ("+", 3, 3),
        ]

        for (texte, ligne, col) in boutons:
            action = (lambda t=texte: self._on_button_click(t))
            ctk.CTkButton(
                btn_frame,
                text=texte,
                width=60,
                height=40,
                corner_radius=8,
                font=("Arial", 16),
                command=action,
            ).grid(row=ligne, column=col, padx=4, pady=4, sticky="nsew")

        # ====== Ligne pour les parenthèses sous le pavé ======
        paren_frame = ctk.CTkFrame(self, fg_color="transparent")
        paren_frame.grid(row=5, column=0, padx=15, pady=(0, 5), sticky="nsew")
        paren_frame.grid_columnconfigure((0, 1), weight=1)

        for (texte, col) in [("(", 0), (")", 1)]:
            action = (lambda t=texte: self._on_button_click(t))
            ctk.CTkButton(
                paren_frame,
                text=texte,
                width=60,
                height=30,
                corner_radius=8,
                font=("Arial", 14),
                command=action,
            ).grid(row=0, column=col, padx=4, pady=4, sticky="nsew")

        # ====== Boutons scientifiques ======
        sci_frame = ctk.CTkFrame(self, fg_color="transparent")
        sci_frame.grid(row=6, column=0, rowspan=2, padx=15, pady=(0, 15), sticky="nsew")

        sci_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        sci_frame.grid_rowconfigure((0, 1), weight=1)

        btn_scientifiques = [
            ("√",   0, 0),
            ("sin", 0, 1),
            ("cos", 0, 2),
            ("tan", 0, 3),
            ("ln",  1, 0),
            ("log", 1, 1),
            ("π",   1, 2),
        ]

        for (texte, ligne, col) in btn_scientifiques:
            action = (lambda t=texte: self._on_scientific_button(t))
            ctk.CTkButton(
                sci_frame,
                text=texte,
                width=60,
                height=38,
                corner_radius=10,
                font=("Arial", 14),
                fg_color="#264653",
                hover_color="#2a9d8f",
                command=action,
            ).grid(row=ligne, column=col, padx=4, pady=4, sticky="nsew")

        self._recharger_historique()

    # ========== Gestion des boutons de base ==========

    def _on_button_click(self, char: str):
        if char == "=":
            self._calculer()
        else:
            self.entry.insert("end", char)

    # Efface tout le champ
    def _clear_all(self):
        self.entry.delete(0, "end")

    # Efface seulement le dernier caractère
    def _clear_last_char(self):
        current = self.entry.get()
        if current:
            self.entry.delete(len(current) - 1, "end")

    def _recharger_historique(self):
        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", "end")
        for ligne in obtenir_historique():
            self.history_box.insert("end", ligne + "\n")
        self.history_box.configure(state="disabled")

    def _effacer_historique_gui(self):
        if messagebox.askyesno("Confirmation", "Effacer tout l'historique ?"):
            effacer_historique()
            self._recharger_historique()

    def _calculer(self):
        expr = self.entry.get()
        try:
            resultat = evaluer_expression(expr)
            self.entry.delete(0, "end")
            self.entry.insert(0, str(resultat))
            ajouter_historique(expr, str(resultat))
            self._recharger_historique()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # ========== Gestion des boutons scientifiques ==========

    def _on_scientific_button(self, label: str):
        valeur = self.entry.get().strip()
        try:
            if label == "π":
                self.entry.delete(0, "end")
                # utilisation de PI importé depuis fonctions.py
                self.entry.insert(0, str(PI))
                ajouter_historique("π", str(PI))
                self._recharger_historique()
                return

            if not valeur:
                raise ValueError("Aucune valeur à utiliser.")

            x = float(valeur)

            if label == "√":
                res = racine_carre(x)
                expr_affichee = f"√({valeur})"
            elif label == "sin":
                res = sinus_deg(x)
                expr_affichee = f"sin({valeur})"
            elif label == "cos":
                res = cosinus_deg(x)
                expr_affichee = f"cos({valeur})"
            elif label == "tan":
                res = tangente_deg(x)
                expr_affichee = f"tan({valeur})"
            elif label == "ln":
                res = logarithme_base_e(x)
                expr_affichee = f"ln({valeur})"
            elif label == "log":
                res = logarithme_base_10(x)
                expr_affichee = f"log({valeur})"
            else:
                return

            self.entry.delete(0, "end")
            self.entry.insert(0, str(res))
            ajouter_historique(expr_affichee, str(res))
            self._recharger_historique()

        except Exception as e:
            messagebox.showerror("Erreur scientifique", str(e))

if __name__ == "__main__":
    app = CalculatriceCTk()
    app.mainloop()
