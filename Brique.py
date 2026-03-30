import customtkinter as ctk
from CTkToolTip import *
import utilitaires 


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


        self.button_toggle = ctk.CTkButton(self.header_frame, text=titre, anchor="w", height=35)
        self.button_toggle.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # --- AJOUT CRUCIAL : Le frame de navigation que le manager cherche ---
        self.frame_nav = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        
        self.btn_prev = ctk.CTkButton(self.frame_nav, text="⟲", width=30, command=self.manager.navigate_back)
        self.btn_prev.grid(row=0, column=0, padx=2)
        
        self.btn_next = ctk.CTkButton(self.frame_nav, text="⟳", width=30, command=self.manager.navigate_forward)
        self.btn_next.grid(row=0, column=1, padx=2)

        #  on ajoute une infobulle sur le bouton de navigation "Précédent" 

        t1=CTkToolTip(self.btn_prev, message="Revenir à la rubrique précédente dans l'historique de navigation", delay=0.5,
                        bg_color="#2B2B2B", text_color="#FFFFFF", border_width=1, border_color="#555555")
        t1.block_update_dimensions_event =lambda:None  # Pallie un bug du DPI Scaling au changement d'écran
        t1.unblock_update_dimensions_event =lambda:None  # Pallie un bug du DPI Scaling au changement d'écran
        #  on ajoute une infobulle sur le bouton de navigation "Suivant" 
        t2=CTkToolTip(self.btn_next, message="Aller à la rubrique suivante dans l'historique de navigation (si disponible)",delay=0.5,
                      bg_color="#2B2B2B", text_color="#FFFFFF", border_width=1, border_color="#555555")
    
        t2.block_update_dimensions_event =lambda:None  # Pallie un bug du DPI Scaling au changement d'écran
        t2.unblock_update_dimensions_event =lambda:None  # Pallie un bug du DPI Scaling au changement d'écran
        #  5. On peut aussi ajouter une infobulle sur le bouton toggle 
        t3=CTkToolTip(self.button_toggle, message="Afficher ou masquer le panneau de saisie de cette rubrique", delay=0.5,
                      bg_color="#2B2B2B", text_color="#FFFFFF", border_width=1, border_color="#555555")
        t3.block_update_dimensions_event =lambda:None  # Pallie un bug du DPI Scaling au changement d'écran# 6. On peut aussi ajouter une infobulle sur le header 
        t4=CTkToolTip(self.header_frame, message="Ceci est le header de la rubrique, contenant le titre et les boutons de navigation", delay=0.5,
                      bg_color="#2B2B2B", text_color="#FFFFFF", border_width=1, border_color="#555555")
        t4.block_update_dimensions_event =lambda:None  # Pallie un bug du DPI Scaling au changement d'écran
        t4.unblock_update_dimensions_event =lambda:None  # Pallie un bug du DPI Scaling au changement d'écran

        # --- Panneau affichable étiré ---
        self.panneau_affichable = ctk.CTkFrame(self.contenant_global, fg_color=couleur_panneau)
        self.panneau_affichable.grid_columnconfigure(0, weight=1)
        # Note : Le manager doit utiliser sticky="ew" lors du .grid() du panneau
        # On ne fait PAS de .grid() ici, c'est le manager qui s'en occupe lors de l'affichage de la brique.
        # La configuration du grid du panneau est stockée par le manager lors du register()
        
        # Gestion des couleurs de texte pour le contraste
        self.couleur_texte_panneau = utilitaires.good_contrast_font_color(couleur_panneau)

    def vider_panneau(self):
        """Supprime tous les widgets à l'intérieur du panneau."""
        for widget in self.panneau_affichable.winfo_children():
            widget.destroy()

    def get_panneau(self):
        """Retourne le frame du panneau pour y ajouter des widgets de l'extérieur."""
        return self.panneau_affichable