import customtkinter as ctk
from grid_manager import GridAccordionManager

class ZoneConfinee:
    def __init__(self, parent, titre, on_delete_callback, on_duplicate_callback, update_total_callback, couleur_header="transparent", couleur_panneau="transparent"):
        self.is_visible = False
        self.titre = titre
        self.update_total_callback = update_total_callback # Stockage de la fonction de mise à jour

        self.widgets_data = {}
        
        # 1. Variable de contrôle pour l'âge avec "trace"
        self.age_var = ctk.StringVar(value="")
        # À chaque modification ("write"), on appelle la fonction de mise à jour du total
        self.age_var.trace_add("write", lambda *args: self.update_total_callback())
        # Enregistrement de la validation (indispensable pour CTkEntry)
        vcmd = (parent.register(self._valider_chiffres), '%P')

        # 2. Conteneur principal
        self.contenant_global = ctk.CTkFrame(parent)
        self.contenant_global.grid_columnconfigure(0, weight=1)

        # 3. Header
        header_frame = ctk.CTkFrame(self.contenant_global, fg_color=couleur_header)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        self.button_toggle = ctk.CTkButton(header_frame, text=titre, anchor="w", command=self.toggle)
        self.button_toggle.grid(row=0, column=0, sticky="ew", padx=(5, 2), pady=5)

        btn_dup = ctk.CTkButton(header_frame, text="D", width=30, command=lambda: on_duplicate_callback(self))
        btn_dup.grid(row=0, column=1, padx=2, pady=5)

        btn_del = ctk.CTkButton(header_frame, text="X", width=30, fg_color="#922b21", command=lambda: on_delete_callback(self))
        btn_del.grid(row=0, column=2, padx=(2, 5), pady=5)

        # 4. Panneau affichable
        self.panneau_affichable = ctk.CTkFrame(self.contenant_global, fg_color=couleur_panneau)
        self.panneau_affichable.grid_columnconfigure(0, weight=1) 
       
        # Champ Nom
        self.widgets_data["nom_client"] = ctk.CTkEntry(self.panneau_affichable, placeholder_text="Nom...")
        self.widgets_data["nom_client"].pack(pady=5, padx=10)

        # Champ Âge (lié à age_var)
        self.widgets_data["age"] = ctk.CTkEntry(
            self.panneau_affichable, 
            placeholder_text="Âge...", 
            textvariable=self.age_var,
            validate="key", 
            validatecommand=vcmd
        )
        self.widgets_data["age"].pack(pady=5, padx=10)
        
        self.widgets_data["actif"] = ctk.CTkCheckBox(self.panneau_affichable, text="Zone Active")
        self.widgets_data["actif"].pack(pady=5, padx=10)

    def _valider_chiffres(self, contenu_futur):
        """Méthode interne pour bloquer les caractères non-numériques."""
        return contenu_futur.isdigit() or contenu_futur == ""

    @property
    def age(self):
        """Propriété qui transforme le texte du widget en entier sécurisé."""
        val = self.age_var.get()
        return int(val) if val.isdigit() else 0

    def toggle(self):
        if self.is_visible:
            self.panneau_affichable.grid_forget()
        else:
            self.panneau_affichable.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.is_visible = not self.is_visible

    def get_data(self):
        donnees = {"titre": self.titre}
        for cle, widget in self.widgets_data.items():
            donnees[cle] = widget.get()
        return donnees

    def set_data(self, data):
        for cle, valeur in data.items():
            if cle in self.widgets_data:
                if cle == "age":
                    self.age_var.set(valeur) # Utilise la StringVar
                else:
                    widget = self.widgets_data[cle]
                    if isinstance(widget, ctk.CTkEntry):
                        widget.delete(0, 'end')
                        widget.insert(0, valeur)
                    elif isinstance(widget, ctk.CTkCheckBox):
                        widget.select() if valeur else widget.deselect()

class MonApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x600")
        self.title("Accordéon Dynamique")

        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=1)

        ctrl_frame = ctk.CTkFrame(self)
        ctrl_frame.grid(column=0, row=0, sticky="ew")
        
        ctk.CTkButton(ctrl_frame, text="+ Ajouter une Zone", command=self.ajouter_zone).pack(pady=5)
        
        # Affichage du Total
        self.label_total = ctk.CTkLabel(ctrl_frame, text="Total des âges : 0", font=("Arial", 14, "bold"))
        self.label_total.pack(pady=5)

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(column=0, row=1, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self.manager = GridAccordionManager()

    @property
    def total_ages(self):
        """Somme dynamique de toutes les propriétés 'age' des zones."""
        return sum(zone.age for zone in self.manager.structures)

    def rafraichir_total(self):
        """Met à jour l'étiquette à l'écran."""
        self.label_total.configure(text=f"Total des âges : {self.total_ages}")

    def ajouter_zone(self, titre=None, data_initiale=None):
        if titre is None:
            titre = f"Zone {len(self.manager.structures) + 1}"
        
        # On passe 'self.rafraichir_total' à chaque zone
        nouvelle_zone = ZoneConfinee(
            self.scroll_frame, titre, 
            self.supprimer_zone, self.dupliquer_zone,
            update_total_callback=self.rafraichir_total,
            couleur_header="lightgreen", couleur_panneau="lightgray"
        )
        
        if data_initiale:
            nouvelle_zone.set_data(data_initiale)

        self.manager.register(nouvelle_zone)
        self.manager.reorganize_grid()
        self.rafraichir_total()

    def dupliquer_zone(self, zone_a_copier):
        donnees_sources = zone_a_copier.get_data()
        nouveau_titre = f"{donnees_sources['titre']} (Copie)"
        self.ajouter_zone(titre=nouveau_titre, data_initiale=donnees_sources)

    def supprimer_zone(self, zone):
        self.manager.unregister(zone)
        zone.contenant_global.destroy()
        self.rafraichir_total() # On recalcule après suppression

if __name__ == "__main__":
    app = MonApp()
    app.mainloop()