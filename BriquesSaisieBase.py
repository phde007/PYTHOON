"""
Dans ce module, on trouve les classes de base pour les briques de saisie de données, utilisées dans la base du programme.
Ces classes sont utilisées pour créer des briques de saisie unitaires (ex : les données d'identification du chantier) 
utilisées une seule fois dans le programme.  Les briques de saisie plus complexes (ex : les zones confinées, les zones 
élémentaires,les équipements, etc.) sont gérées dans des modules spécifiques (ex : ZoneConfinee.py, ZoneElementaire.py,
 Equipement.py, etc.) et héritent de ces classes de base. 



"""

import customtkinter as ctk
import BriqueSaisie as bs # Import de votre classe de base persistante

import customtkinter as ctk
import BriqueSaisie as bs

class BriqueSaisieBaseChantier(bs.BriqueSaisie):
    def __init__(self, parent, manager, **kwargs):
        # On initialise la base avec le titre spécifique
        super().__init__(parent, "Identification du Chantier", manager, **kwargs)
        
        # On récupère le panneau de l'interface créée par le parent
        panneau = self.interface.get_panneau()
        
        # 1. Définition des variables à sauver
        self.persist_vars = {
            "nom_chantier": ctk.StringVar(value=""),
            "adresse_chantier": ctk.StringVar(value=""),
            "ville_chantier": ctk.StringVar(value=""),
            "code_postal_chantier": ctk.StringVar(value=""),
        }
        
        # 2. Placement des widgets dans le panneau
        # Note: on sépare la création et le .grid() pour éviter le retour "None"
        #En Python, widget = CTkEntry(...).grid() assigne None à la variable car .grid() ne renvoie rien. 
        # En séparant les deux ou en ne stockant pas le widget (puisque vous avez déjà la StringVar), 
        # vous évitez des crashs futurs.
        lbl_nom_du_chantier=ctk.CTkLabel(panneau, text="Nom du chantier :")
        lbl_nom_du_chantier.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_nom_du_chantier=ctk.CTkEntry(panneau, textvariable=self.persist_vars["nom_chantier"])
        entry_nom_du_chantier.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        lbl_adresse=ctk.CTkLabel(panneau, text="Adresse :")
        lbl_adresse.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_adresse=ctk.CTkEntry(panneau, textvariable=self.persist_vars["adresse_chantier"])
        entry_adresse.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        lbl_ville=ctk.CTkLabel(panneau, text="Ville :")
        lbl_ville.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_ville=ctk.CTkEntry(panneau, textvariable=self.persist_vars["ville_chantier"])
        entry_ville.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        lbl_code_postal=ctk.CTkLabel(panneau, text="Code Postal :")
        lbl_code_postal.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        entry_code_postal=ctk.CTkEntry(panneau, textvariable=self.persist_vars["code_postal_chantier"])
        entry_code_postal.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Configuration de l'étalement
        panneau.grid_columnconfigure(1, weight=1)


