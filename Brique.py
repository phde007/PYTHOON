import customtkinter as ctk
from CTkToolTip import *
import utilitaires as ut
import visuel.constantes_couleurs as cv

"""
Cette classe représente une "brique" : un frame contenant_global, contenant un header et un panneau affichable.
- Le header contient un bouton toggle pour afficher ou masquer le panneau.
- Le panneau affichable peut contenir n'importe quel widget (ici un label d'exemple est utilisé).
"""


class Brique:
    def __init__(self, parent, titre, manager, couleur_header="transparent", couleur_panneau="transparent", on_show_callback=None, on_hide_callback=None):
        """
        Classe de base pour un élément d'accordéon (Brique).
        :param parent: Le widget scrollable ou frame parent.
        :param titre: Le texte du bouton principal.
        :param manager: L'instance de GridAccordionManager qui gère la logique de navigation 
        :param couleur_header: Couleur de fond du header.
        :param couleur_panneau: Couleur de fond du panneau affichable.  
        :param on_show_callback: Fonction à appeler lorsque la brique est affichée (utile pour le rafraîchissement dynamique).
        :param on_hide_callback: Fonction à appeler lorsque la brique est masquée (utile pour concaténation de briques ou nettoyage avant affichage d'une autre brique)  
            (les briques parcourues successivement)
        """
        self.manager = manager
        self.on_show_callback = on_show_callback
        self.on_hide_callback = on_hide_callback
        self.is_visible = False
        self.titre = titre
        self.base_text = titre 
        
        # --- Conteneur principal étiré---
        self.contenant_global = ctk.CTkFrame(parent)
        self.contenant_global.grid_columnconfigure(0, weight=1)
        # On force l'étalement horizontal immédiat
        self.contenant_global.grid(sticky="ew", padx=5, pady=2)
        
        # --- Header étiré ---
        self.header_frame = ctk.CTkFrame(self.contenant_global, fg_color=couleur_header)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)     # Le titre prend l'espace
        #self.header_frame.configure(fg_color="red") pour le test du header

        # Dans Brique.py, modifiez la création du bouton ainsi :
        self.button_toggle = ctk.CTkButton(
            self.header_frame, 
            text=titre, 
            anchor="w", 
            height=35,
            command=lambda: self.manager.toggle_section(self) # ajout de la commande de bascule au bouton de titre
        )
        self.button_toggle.grid(row=0, column=0, sticky="ew", padx=5, pady=2)

        # --- AJOUT CRUCIAL : Le frame de navigation que le manager cherche ---
        self.frame_nav = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        # self.frame_nav.grid(row=0, column=1, sticky="e", padx=5)  # On place le frame de navigation à droite dans le header
        
        self.btn_prev = ctk.CTkButton(self.frame_nav, text="⟲", width=30, command=self.manager.navigate_back)
        self.btn_prev.grid(row=0, column=0, padx=2)
        
        self.btn_next = ctk.CTkButton(self.frame_nav, text="⟳", width=30, command=self.manager.navigate_forward)
        self.btn_next.grid(row=0, column=1, padx=2)

        # ajout d'une zone de contrôles secondaires dans le header (pour les boutons d'action spécifiques à la brique) que 
        # le manager n'utilise pas mais qui peut être utilisée par l'application pour ajouter des boutons d'action spécifiques à la brique 
        # (ex : un bouton "Ajouter un élément" dans une brique de gestion d'une liste d'éléments), que les classes filles
        # peuvent utiliser pour ajouter des boutons d'action spécifiques à la brique sans interférer avec 
        # les boutons de navigation gérés par le manager)

        self.extra_controls_frame = ctk.CTkFrame(
            self.header_frame, 
            fg_color="transparent",
            height=0,  # Empêche le frame de pousser en hauteur
            width=0    # Empêche le frame de pousser en largeur
        )
        # L'utilisation de sticky="ns" est importante : 
        # elle permettra au frame de s'étirer pour correspondre à la hauteur 
        # du bouton de titre (qui est la référence de hauteur du header).
        self.extra_controls_frame.grid(row=0, column=2, padx=5, sticky="nse")

        #  on ajoute une infobulle sur le bouton de navigation "Précédent" 

        t1=CTkToolTip(self.btn_prev, message="Revenir à la rubrique précédente dans l'historique de navigation", delay=0.5,
                        bg_color=cv.TOOLTIP_BG, text_color=cv.TOOLTIP_FG, border_width=1, border_color=cv.TOOLTIP_BORDER_COLOR)
        t1.block_update_dimensions_event =lambda:None  # Pallie un bug du DPI Scaling au changement d'écran
        t1.unblock_update_dimensions_event =lambda:None  # Pallie un bug du DPI Scaling au changement d'écran
        
        #  Ajout des infobulles sur les éléments du header existant dans toutes les briques (boutons de navigation et bouton toggle)
        
        ut.create_tooltip(self.btn_prev, "Revenir à la rubrique précédente dans l'historique de navigation")
        ut.create_tooltip(self.btn_next, "Aller à la rubrique suivante dans l'historique de navigation (si disponible)")
        ut.create_tooltip(self.button_toggle, "Afficher ou masquer le panneau de saisie de cette rubrique")
        ut.create_tooltip(self.header_frame, "Ceci est le header de la rubrique, contenant le titre et les boutons de navigation")

        # --- Panneau affichable étiré ---
        self.panneau_affichable = ctk.CTkFrame(self.contenant_global, fg_color=couleur_panneau)
        self.panneau_affichable.grid_columnconfigure(0, weight=1)
        # Note : Le manager doit utiliser sticky="ew" lors du .grid() du panneau
        # On ne fait PAS de .grid() ici, c'est le manager qui s'en occupe lors de l'affichage de la brique.
        # La configuration du grid du panneau est stockée par le manager lors du register()
        
        # Gestion des couleurs de texte pour le contraste
        self.couleur_texte_panneau = ut.good_contrast_font_color(couleur_panneau)

    def vider_panneau(self):
        """Supprime tous les widgets à l'intérieur du panneau."""
        for widget in self.panneau_affichable.winfo_children():
            widget.destroy()

    def get_panneau(self):
        """Retourne le frame du panneau pour y ajouter des widgets de l'extérieur."""
        return self.panneau_affichable