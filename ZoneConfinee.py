import customtkinter as ctk
import Brique as brq
from CTkToolTip import *
import ZoneElementaire
import visuel.constantes_couleurs as cv
import utilitaires as ut

class ZoneConfinee(brq.Brique): # Héritage de Brique
    def __init__(self, parent, titre, manager, on_delete_callback, on_duplicate_callback, update_total_callback):
        # 1. Appel du constructeur de Brique
        super().__init__(
            parent=parent,
            titre=titre,
            manager=manager, # On utilise le manager passé en paramètre
            couleur_header=cv.ZCONF_HEADER_BG,
            couleur_panneau=cv.ZCONF_PANEL_BG,
            on_show_callback=self._au_deploiement
        )
        
        self.on_delete_callback = on_delete_callback
        self.on_duplicate_callback = on_duplicate_callback
        self.update_total_callback = update_total_callback

        
        # 3. Ajout des boutons spécifiques dans le header
        self._setup_header_buttons()
        
        # 4. Remplissage du panneau (le contenu)
        self._construire_contenu()

    def _setup_header_buttons(self):
        """Ajoute les boutons 📂 et 🗑️ dans la zone réservée du header."""
        # Bouton Dupliquer
        self.btn_dup = ctk.CTkButton(self.extra_controls_frame, text="📂", width=30, 
                                     command=lambda: self.on_duplicate_callback(self))
        self.btn_dup.pack(side="right", padx=2)
        ut.create_tooltip(self.btn_dup, "Dupliquer la Zone Confinée affichée")

        # Bouton Supprimer
        self.btn_del = ctk.CTkButton(self.extra_controls_frame, text="🗑️", width=30, 
                                     fg_color="#CC0000", hover_color="#AA0000",
                                     command=lambda: self.on_delete_callback(self))
        self.btn_del.pack(side="right", padx=2)
        ut.create_tooltip(self.btn_del, "Supprimer la Zone Confinée affichée")
       

    def _construire_contenu(self):
        """Remplit self.panneau_affichable avec les widgets de la zone."""
        # Exemple : Label de titre interne
        self.label_info = ctk.CTkLabel(self.panneau_affichable, text="Paramètres de la Zone Confinée", 
                                       font=("Arial", 14, "bold"))
        self.label_info.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        
        # Bouton pour ajouter une Zone Elementaire
        self.btn_add_ze = ctk.CTkButton(self.panneau_affichable, text="+ Ajouter Zone Élémentaire",
                                        command=self.ajouter_zone_elementaire)
        self.btn_add_ze.grid(row=1, column=0, pady=5, padx=10)

    def _au_deploiement(self):
        """Méthode appelée automatiquement par le manager quand on ouvre cette brique."""
        print(f"Ouverture de la zone : {self.titre}")
        # Ici on peut rafraîchir les calculs de volumes totaux
        self.update_total_callback()

    def ajouter_zone_elementaire(self):
        # Logique pour ajouter une ZoneElementaire (qui sera aussi une Brique !)
        # Elle sera enregistrée dans self.manager (le manager interne de cette ZoneConfinee)
        pass

    # ---------------------------------------------------------------------------------------------
    # Méthodes pour l'export/import de données (sauvegarde/restauration) et pour la duplication
    # ---------------------------------------------------------------------------------------------
        
    def get_data(self):
        return {
            "titre": self.titre,
            # compléter avec les données spécifiques de la Zone Confinée (ex : paramètres, champs de saisie, etc.)

            # On demande aux enfants de s'exporter
            "zones_elementaires": [z.get_data() for z in self.manager.structures if isinstance(z, ZoneElementaire.ZoneElementaire)]
        }

    def set_data(self, data):
        # restauration des widgets appartenant en propre à la Zone Confinée
        if "nom_client" in data: self.nom_var.set(data["nom_client"])
        if "age" in data: self.age_var.set(str(data["age"]))
        if "actif" in data: self.actif_var.set(data["actif"])


            # Restauration des enfants
        if "zones_elementaires" in data:
            for z_data in data["zones_elementaires"]:
                self.ajouter_zone(titre=z_data.get("titre"), data_initiale=z_data)






