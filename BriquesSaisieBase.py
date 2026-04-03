"""
Dans ce module, on trouve les classes de base pour les briques de saisie de données, utilisées dans la base du programme.
Ces classes sont utilisées pour créer des briques de saisie unitaires (ex : les données d'identification du chantier) 
utilisées une seule fois dans le programme.  Les briques de saisie plus complexes (ex : les zones confinées, les zones 
élémentaires,les équipements, etc.) sont gérées dans des modules spécifiques (ex : ZoneConfinee.py, ZoneElementaire.py,
 Equipement.py, etc.) et héritent de ces classes de base. 



"""

import customtkinter as ctk
import BriqueSaisieSansFilles as bsf # Import de votre classe de base persistante
import BriqueSaisieAvecFilles as baf # Import de votre classe de base avec gestion des filles
from utilitaires_gui import GUITools  


#region Classes test
#_________________________________________________________________________________________________________________________
# Classes de test  pour les briques imbriquées, une brique avec filles contentant une brique sans filles, pour tester la navigation et l'export des données imbriquées
#_________________________________________________________________________________________________________________________
class BriqueSansFillesTest(bsf.BriqueSaisieSansFilles):
    def __init__(self, parent, titre, manager, **kwargs):
        # On initialise la base avec le titre spécifique
        super().__init__(parent, titre, manager, **kwargs)
        
        # On récupère le panneau de l'interface créée par le parent
        panneau = self.interface.get_panneau()
        
        # 1. Définition des variables à sauver
        self.persist_vars = {
            "champ1": ctk.StringVar(value=""),
            "champ2": ctk.StringVar(value=""),
        }
        
        # 2. Placement des widgets dans le panneau
        lbl_champ1=ctk.CTkLabel(panneau, text="Champ 1 :")
        lbl_champ1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_champ1=ctk.CTkEntry(panneau, textvariable=self.persist_vars["champ1"])
        entry_champ1.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        lbl_champ2=ctk.CTkLabel(panneau, text="Champ 2 :")
        lbl_champ2.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_champ2=ctk.CTkEntry(panneau, textvariable=self.persist_vars["champ2"])
        entry_champ2.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Configuration de l'étalement
        panneau.grid_columnconfigure(1, weight=1)



class BriqueContenanteTest(baf.BriqueSaisieAvecFilles):
    def __init__(self, parent, titre, manager, **kwargs): # Ajoutez 'titre'
        super().__init__(parent, titre, manager, **kwargs)
        
        # Initialisation de self.persist_vars (Attention : baf ne le crée pas par défaut)
        self.persist_vars = {} 
        
        panneau = self.interface.get_panneau()
        self.persist_vars["description"] = ctk.StringVar(value="")
            
        lbl_description = ctk.CTkLabel(panneau, text="Description :")
        lbl_description.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_description = ctk.CTkEntry(panneau, textvariable=self.persist_vars["description"])
        entry_description.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        #ajout d'une brique fille de test (une brique sans filles) dans la brique contenante
        self.brique_fille_test = BriqueSansFillesTest(panneau, "Sous-Brique Test", manager=self.manager_filles)
        self.manager_filles.register(self.brique_fille_test.interface)

        # Configuration de l'étalement
        panneau.grid_columnconfigure(1, weight=1)



#region Classes des briques niveau base
class BriqueSaisieBaseChantier(bsf.BriqueSaisieSansFilles):
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



class BriqueSaisieDocumentationReglementaire(bsf.BriqueSaisieSansFilles):
    def __init__(self, parent, manager, **kwargs):
        # On initialise la base avec le titre spécifique
        super().__init__(parent, "Généralités sur les fonctionnalités de l'assistant, et sur la Documentation Réglementaire", manager, **kwargs)
        
        # On récupère le panneau de l'interface créée par le parent
        panneau = self.interface.get_panneau()
        
        # Contenu purement documentaire
        doc_text = (            
            "L'assistant est conçu pour aider les professionnels en charge du contrôle des bilans aérauliques à préparer des réponse circonstanciées " + 
            "aux MOA en retour de l'examen des bilans aérauliques qu'ils leur ont soumis pour approbation, en leur fournissant des ressources et des outils " +
            "pour mieux comprendre les exigences réglementaires et les méthodes de calcul associées et en leur demander éventuellement des précisions ou des " + 
            " informations complémentaires. " +
            "\n\nL'évaluation des bilans aérauliques repose sur le document de référence de l'INRS ED6307 : \n\t[Outil de calcul des bilans aérauliques], " +
            " téléchargeable sur (https://www.inrs.fr/media.html?refINRS=ED%206307)" +
            "\n\n Il est nécessaire de renseigner les données de chantier dans cette application avant de pouvoir utiliser les outils de calcul et d'évaluation des bilans aérauliques, " + 
            "car ces données sont utilisées pour contextualiser les évaluations et les réponses aux MOA." +
            "\nLa meilleure façon de procéder est d'utiliser l'outil de calcul des bilans aérauliques de l'INRS " +
            "ce qui assure de travailler avec un outil conforme à la réglementation et de bénéficier de mises à jour régulières en cas de changements réglementaires." +
             "\n\t- [Outil de calcul des bilans aérauliques](https://www.inrs.fr/publications/outils/amiante-aeraulique/outil.html#/)" +
            "\n\nCet outil de calcul est enrichi par des fiches de définition des appareils couramment utilisés dans les installations confinées, ce qui " +
            "permet de gagner du temps dans la saisie des données et d'assurer une meilleure précision dans les évaluations." +
            "Ensuite, le plus simple est d'exporter les données du bilan aéraulique au format Excel depuis l'outil de calcul de l'INRS et " +
            "de les importer dans cette application. Ensuite, cette application peut être utilisée pour préparer des réponses circonstanciées aux MOA " + 
            "en retour de l'examen des bilans aérauliques qu'ils ont soumis pour approbation"
        )
        
        
                
        # 1. Création du Textbox
        # border_width=0 et fg_color="transparent" pour qu'il ressemble à un label
        self.txt_doc = ctk.CTkTextbox(
            panneau, 
            wrap="word", 
            fg_color="transparent", # Pour se fondre dans le panneau
            border_width=0,
            height=300, # Ajustez la hauteur selon vos besoins (le textbox ne gère pas toujours bien le wrap avec une hauteur auto, donc on fixe une hauteur raisonnable)
            font=("Arial", 12),
            activate_scrollbars=False # Optionnel si le texte est court
        )
        self.txt_doc.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
       

        # Insertion du texte
        self.txt_doc.insert("0.0", doc_text)

         # Détection des liens hypertextes dans le texte et création de tags pour les rendre cliquables
        GUITools.setup_hyperlinks(self.txt_doc)
        self.txt_doc.configure(state="disabled")


        # 3. VERROUILLAGE : On rend le texte non éditable
        self.txt_doc.configure(state="disabled")