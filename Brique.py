import customtkinter as ctk


"""
Cette classe représente une "brique" : un frame contenant_global, contenant un header et un panneau affichable.
- Le header contient un bouton toggle pour afficher ou masquer le panneau.
- Le panneau affichable peut contenir n'importe quel widget (ici un label d'exemple est utilisé).
"""


class Brique:
    def __init__(self, parent, titre, couleur_header="transparent", couleur_panneau="transparent"):
        self.is_visible = False
        self.titre = titre
        
        # Conteneur principal
        self.contenant_global = ctk.CTkFrame(parent)
        self.contenant_global.grid_columnconfigure(0, weight=1) #
        self.contenant_global.grid_rowconfigure(1, weight=1)  # Le panneau affichable prendra tout l'espace restant en hauteur
        self.contenant_global.grid(pady=5, padx=5, sticky="ew")  # On laisse le manager gérer la position "row" et "column"
        # cadre autour du contenant_global pour mieux visualiser les bords lors du développement
        self.contenant_global.configure(border_width=2, border_color="#FF0000")
        

        # Header (Uniquement le bouton Toggle)
        header_frame = ctk.CTkFrame(self.contenant_global, fg_color=couleur_header)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        # Bouton Toggle unique (pas de bouton X ou D)
        self.button_toggle = ctk.CTkButton(header_frame, text=titre, anchor="w")
        self.button_toggle.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Panneau affichable
        self.panneau_affichable = ctk.CTkFrame(self.contenant_global, fg_color=couleur_panneau)
        # Par défaut, il n'est pas affiché dans la grille ici, le manager s'en occupe
        self.panneau_affichable.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.panneau_affichable.grid_columnconfigure(0, weight=1)
        #cadre autour du panneau_affichable pour mieux visualiser les bords lors du développement
        self.panneau_affichable.configure(border_width=1, border_color="#167A7A")

        
        # Exemple de contenu pour la brique
        label_info = ctk.CTkLabel(self.panneau_affichable, text=f"Contenu fixe de la {titre}", text_color= "black")
        label_info.grid(row=0, column=0,padx=20,pady=20)