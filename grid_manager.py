# grid_manager.py
import CTkToolTip
import PIL
from CTkToolTip import *
from PIL import Image
import Brique as brq
from utilitaires import next_free_row
import visuel.constantes_couleurs as cv

class GridAccordionManager:
    def __init__(self, icon_open=None, icon_closed=None):
        self.structures = []
        # On stocke des objets CTkImage au lieu de strings
        self.icon_open = icon_open
        self.icon_closed = icon_closed
        

    def register(self, structure):
        if structure in self.structures:
            return
        
        # Mémorise la config du panneau interne (souvent row=1)
        structure.grid_params = structure.panneau_affichable.grid_info()
        # On garde le texte tel quel sans préfixe
        structure.base_text = structure.button_toggle.cget("text")

        self.structures.append(structure)
        
        structure.button_toggle.configure(
            command=lambda s=structure: self._handle_toggle(s)
        )
        self._update_ui(structure)
        
        structure.is_visible = True
        structure.button_toggle.configure(
            command=lambda s=structure: self._handle_toggle(s)
        )
        self._update_ui(structure)

    def unregister(self, structure):
        """Retire la structure et réorganise la grille du parent."""
        if structure in self.structures:
            self.structures.remove(structure)
            self.reorganize_grid()

    def reorganize_grid(self):
        """Recalcule la position 'row' de chaque contenant_global."""
        for index, s in enumerate(self.structures):
            # On force le repositionnement du contenant dans son parent
            s.contenant_global.grid(row=index, column=0, sticky="ew")

    def _handle_toggle(self, target):
        if target.is_visible:
            self._hide(target)
        else:
            for s in self.structures:
                if s.is_visible: self._hide(s)
            self._show(target)

    def _show(self, structure):
        structure.panneau_affichable.grid(**structure.grid_params)
        structure.is_visible = True
        self._update_ui(structure)

    def _hide(self, structure):
        structure.panneau_affichable.grid_forget()
        structure.is_visible = False
        self._update_ui(structure)

    def _update_ui(self, structure):
        # On choisit l'icône selon l'état
        img = self.icon_open if structure.is_visible else self.icon_closed
        
        # On met à jour le bouton avec l'image ET on garde le texte propre
        structure.button_toggle.configure(
            image=img, 
            text=structure.base_text,
            compound="left"  # Place l'image à gauche du texte
        )