# grid_manager.py
import customtkinter as ctk
from PIL import Image

class GridAccordionManager:
    def __init__(self):
        self.structures = []
        # Icones pour le bouton toggle
        self.icon_open = ctk.CTkImage(dark_image=Image.open(r".\visuel\chevron_droite.png"), size=(20,20))
        self.icon_closed = ctk.CTkImage(dark_image=Image.open(r".\visuel\chevron_bas.png"), size=(20,20))
        
        # --- Gestion de l'historique ---
        self.history_back = []     # Pile des briques précédentes
        self.history_forward = []  # Pile pour le bouton "Suivant"
        self.current_active = None # La brique actuellement dépliée

    def register(self, structure):
        if structure in self.structures:
            return
        
        # Mémorise la configuration de grille du panneau interne
        structure.grid_params = structure.panneau_affichable.grid_info()
        # On s'assure que la brique connaît son nom d'origine pour l'affichage
        if not hasattr(structure, 'base_text'):
            structure.base_text = structure.button_toggle.cget("text")

        self.structures.append(structure)
        
        # On lie le clic sur le titre à la gestion du manager
        structure.button_toggle.configure(
            command=lambda s=structure: self._handle_toggle(s)
        )
        
        # Initialisation de l'UI (fermé par défaut)
        self._hide(structure)

    def unregister(self, structure):
        if structure in self.structures:
            self.structures.remove(structure)
        # Nettoyage de l'historique pour éviter de pointer vers une brique détruite
        self.history_back = [s for s in self.history_back if s != structure]
        self.history_forward = [s for s in self.history_forward if s != structure]
        if self.current_active == structure:
            self.current_active = None

    def _handle_toggle(self, target):
        if target.is_visible:
            self._hide(target)
            self.current_active = None
        else:
            # Si on ouvre une nouvelle brique, on archive l'ancienne
            if self.current_active and self.current_active != target:
                self.history_back.append(self.current_active)
                self.history_forward.clear() # On casse la chaîne "Suivant" si clic manuel
            
            self.hide_all()
            self._show(target)
            self.current_active = target
            self._scroll_to_item(target)

    def navigate_back(self):
        """Action du bouton ⟲"""
        if self.history_back:
            prev = self.history_back.pop()
            if self.current_active:
                self.history_forward.append(self.current_active)
            self._force_open(prev)

    def navigate_forward(self):
        """Action du bouton ⟳"""
        if self.history_forward:
            nxt = self.history_forward.pop()
            if self.current_active:
                self.history_back.append(self.current_active)
            self._force_open(nxt)

    def _force_open(self, target):
        """Ouvre une brique sans modifier l'historique de création"""
        self.hide_all()
        self._show(target)
        self.current_active = target
        self._scroll_to_item(target)

    def hide_all(self):
        for s in self.structures:
            if s.is_visible:
                self._hide(s)

    def _show(self, structure):
        # On ajoute explicitement sticky="ew" lors de l'affichage du panneau pour garantir l'étirement horizontal
        structure.panneau_affichable.grid(**structure.grid_params, sticky="ew") 
        structure.is_visible = True
        self._update_ui(structure)
        # DÉCLENCHEMENT DU CALLBACK D'AFFICHAGE
        if hasattr(structure, 'on_show_callback') and structure.on_show_callback:
            structure.on_show_callback()

    def _hide(self, structure):
        structure.panneau_affichable.grid_forget()
        structure.is_visible = False
        self._update_ui(structure)
        # DÉCLENCHEMENT DU CALLBACK DE MASQUAGE
        if hasattr(structure, 'on_hide_callback') and structure.on_hide_callback:
            structure.on_hide_callback()

    def _update_ui(self, structure):
        # 1. Mise à jour de l'icône de l'accordéon
        img = self.icon_open if structure.is_visible else self.icon_closed
        structure.button_toggle.configure(image=img, text=structure.base_text, compound="left")
        
        # 2. Gestion des boutons de navigation contextuels
        if structure.is_visible:
            # On affiche le frame de navigation (colonne 1 du header)
            structure.frame_nav.grid(row=0, column=1, padx=5)
            
            # On grise les boutons si l'historique est vide
            state_back = "normal" if self.history_back else "disabled"
            state_fwd = "normal" if self.history_forward else "disabled"
            structure.btn_prev.configure(state=state_back)
            structure.btn_next.configure(state=state_fwd)
        else:
            # On masque totalement la navigation si la brique est fermée
            structure.frame_nav.grid_forget()

    def _scroll_to_item(self, structure):
        """Centre l'affichage sur la brique activée"""
        structure.contenant_global.update_idletasks()
        parent = structure.contenant_global.master
        
        # Si le parent est un CTkScrollableFrame, on accède au canvas interne
        if hasattr(parent, "_parent_canvas"):
            canvas = parent._parent_canvas
            y_pos = structure.contenant_global.winfo_y()
            
            # Calcul de la position relative (0.0 à 1.0)
            # On récupère la hauteur totale du contenu du canvas
            total_height = canvas.bbox("all")[3]
            
            if total_height > 0:
                # On positionne le scroll pour que la brique soit en haut
                canvas.yview_moveto(y_pos / total_height)

    def reorganize_grid(self):
        for index, s in enumerate(self.structures):
            # On s'assure que le contenant_global occupe toute la largeur (sticky="ew")
            s.contenant_global.grid(row=index, column=0, sticky="ew", padx=5, pady=2)