import customtkinter as ctk
import webbrowser
import re

class GUITools:
    """
    Boîte à outils partagée pour les composants graphiques de l'application.
    Regroupe les fonctions de liens hypertextes et de validation de saisie.
    """

    # --- SECTION 1 : LIENS CLIQUABLES ---

    @staticmethod
    def setup_hyperlinks(textbox):
        """
        Transforme les adresses HTTP/HTTPS d'un CTkTextbox en liens bleus et cliquables.
        """
        # Vérification de sécurité
        if isinstance(textbox, str):
            print("Erreur : Vous avez passé du texte (str) à setup_hyperlinks au lieu du widget Textbox.")
            return
        
        # Configuration visuelle du lien (bleu et souligné)
        textbox.tag_config("link", foreground="#1572e8", underline=True)
        
        # Recherche de toutes les URLs dans le texte
        content = textbox.get("0.0", "end")
        # Cette regex capture les URLs mais s'arrête avant une parenthèse fermante ou un espace
        for match in re.finditer(r"https?://[^\s)]+", content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            textbox.tag_add("link", start, end)

        # Liaison des actions de la souris
        # 1. Le clic gauche ouvre le lien
        textbox.tag_bind("link", "<Button-1>", lambda e: GUITools._ouvrir_url(e, textbox))
        # 2. Le curseur devient une main quand on survole
        textbox.tag_bind("link", "<Enter>", lambda _: textbox.configure(cursor="hand2"))
        # 3. Le curseur redevient normal quand on sort
        textbox.tag_bind("link", "<Leave>", lambda _: textbox.configure(cursor=""))

    @staticmethod
    def _ouvrir_url(event, textbox):
        """Logique interne pour extraire l'URL sous le clic et l'ouvrir."""
        # On trouve l'index (ligne.colonne) sous le pointeur de souris
        index = textbox.index(f"@{event.x},{event.y}")
        # On cherche à quel bloc de lien cet index appartient
        ranges = textbox.tag_ranges("link")
        for i in range(0, len(ranges), 2):
            if textbox.compare(ranges[i], "<=", index) and textbox.compare(index, "<=", ranges[i+1]):
                url = textbox.get(ranges[i], ranges[i+1])
                webbrowser.open(url)
                break

    # --- SECTION 2 : VALIDATION DE SAISIE ---

    @staticmethod
    def validate_numeric(contenu_futur, decimal=True, max_chars=10):
        """
        Valide la saisie dans un CTkEntry pour n'autoriser que les nombres.
        - decimal=True : Autorise un seul séparateur (point ou virgule).
        - max_chars : Limite la longueur de la saisie.
        """
        # Toujours autoriser le champ vide (pour pouvoir effacer)
        if contenu_futur == "":
            return True
        
        # Limite de longueur
        if len(contenu_futur) > max_chars:
            return False

        if decimal:
            # On remplace la virgule par un point pour que Python puisse tester le float
            val_test = contenu_futur.replace(',', '.')
            try:
                float(val_test)
                # Vérifie qu'il n'y a pas deux points (ex: 12.5.2)
                return val_test.count('.') <= 1
            except ValueError:
                return False
        else:
            # Mode entier pur
            return contenu_futur.isdigit()