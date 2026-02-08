import customtkinter as ctk
from grid_manager import GridAccordionManager

class ZoneConfinee:
    def __init__(self, parent, titre, on_delete_callback, on_duplicate_callback):
        self.is_visible = False
        self.titre = titre
        
        # 1. Conteneur principal
        self.contenant_global = ctk.CTkFrame(parent)
        self.contenant_global.grid_columnconfigure(0, weight=1)

        # 2. Header
        header_frame = ctk.CTkFrame(self.contenant_global, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        # Bouton principal (Toggle)
        self.button_toggle = ctk.CTkButton(header_frame, text=titre, anchor="w", command=self.toggle)
        self.button_toggle.grid(row=0, column=0, sticky="ew", padx=(5, 2), pady=5)

        # Bouton Duplicate
        btn_dup = ctk.CTkButton(header_frame, text="D", width=30, command=lambda: on_duplicate_callback(self))
        btn_dup.grid(row=0, column=1, padx=2, pady=5)

        # Bouton Delete
        btn_del = ctk.CTkButton(header_frame, text="X", width=30, fg_color="#922b21", command=lambda: on_delete_callback(self))
        btn_del.grid(row=0, column=2, padx=(2, 5), pady=5)

        # 3. Panneau affichable (Contenu)
        self.panneau_affichable = ctk.CTkFrame(self.contenant_global, fg_color="gray20")
        # On définit le champ de saisie ICI, dès l'initialisation
        self.input_champ = ctk.CTkEntry(self.panneau_affichable, placeholder_text="Entrez une valeur...")
        self.input_champ.pack(pady=10, padx=10)

    def toggle(self):
        """ Gère l'affichage/masquage du panneau """
        if self.is_visible:
            self.panneau_affichable.grid_forget()
        else:
            self.panneau_affichable.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.is_visible = not self.is_visible

    def get_data(self):
        """ Récupère les données actuelles de la zone """
        return {
            "titre": self.titre,  # <--- On ajoute le titre ici
            "valeur": self.input_champ.get()
        }

    def set_data(self, data):
        """ Remplit la zone avec des données """
        if data and "valeur" in data:
            self.input_champ.delete(0, 'end')
            self.input_champ.insert(0, data["valeur"])

class MonApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x600")
        self.title("Accordéon Dynamique")

        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=1) # Permet au scroll_frame de prendre la hauteur restante

        # Zone de contrôle en haut
        ctrl_frame = ctk.CTkFrame(self)
        ctrl_frame.grid(column=0, row=0, sticky="ew")
        ctrl_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(ctrl_frame, text="+ Ajouter une Zone", command=self.ajouter_zone).pack(pady=5)

        # Container pour les zones
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(column=0, row=1, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Initialisation du Manager
        self.manager = GridAccordionManager()

    def ajouter_zone(self, titre=None, data_initiale=None):
        if titre is None:
            titre = f"Zone {len(self.manager.structures) + 1}"
        
        # On crée l'objet (ce qui exécute le __init__ et crée le CTkEntry)
        nouvelle_zone = ZoneConfinee(self.scroll_frame, titre, self.supprimer_zone, self.dupliquer_zone)
        
        # On injecte les données si elles existent
        if data_initiale:
            nouvelle_zone.set_data(data_initiale)

        self.manager.register(nouvelle_zone)
        self.manager.reorganize_grid()

    def dupliquer_zone(self, zone_a_copier):
        # On récupère les données de la zone source
        donnees_sources = zone_a_copier.get_data()
        # On crée la nouvelle zone avec ces données
        self.ajouter_zone(titre=f"{zone_a_copier.titre} (Copie)", data_initiale=donnees_sources)

        # 1. On récupère le dictionnaire de la zone source
        donnees = zone_a_copier.get_data()
        
        # 2. On récupère le titre (soit dans le dico, soit directement de l'objet)
        # La méthode .get("titre") évite le crash si la clé est absente
        titre_source = donnees.get("titre", zone_a_copier.titre)
        
        nouveau_titre = f"{titre_source} (Copie)"
        
        # 3. On crée la nouvelle zone en passant les données
        self.ajouter_zone(titre=nouveau_titre, data_initiale=donnees)


    def supprimer_zone(self, zone):
        # 1. On le retire du manager
        self.manager.unregister(zone)
        # 2. On détruit le widget
        zone.contenant_global.destroy()

if __name__ == "__main__":
    app = MonApp()
    app.mainloop()