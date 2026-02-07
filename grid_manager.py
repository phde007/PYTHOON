# grid_manager.py

class GridAccordionManager:
    def __init__(self, open_prefix="▼ ", closed_prefix="▶ "):
        self.structures = []
        self.open_prefix = open_prefix
        self.closed_prefix = closed_prefix

    def register(self, structure):
        if structure in self.structures:
            return
        
        # Mémorise la config du panneau interne (souvent row=1)
        structure.grid_params = structure.panneau_affichable.grid_info()
        structure.base_text = structure.button_toggle.cget("text")
        
        self.structures.append(structure)
        
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
        prefix = self.open_prefix if structure.is_visible else self.closed_prefix
        structure.button_toggle.configure(text=f"{prefix}{structure.base_text}")