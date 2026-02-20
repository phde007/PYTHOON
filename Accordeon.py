import customtkinter as ctk
from grid_manager import GridAccordionManager
import Brique as brq
from utilitaires import next_free_row

class ZoneConfinee:
    def __init__(self, parent, titre, on_delete_callback, on_duplicate_callback, update_total_callback, couleur_header="transparent", couleur_panneau="transparent"):
        self.is_visible = False
        self.titre = titre
        self.update_total_callback = update_total_callback

        self.widgets_data = {}
        
        # Variable de contrôle pour l'âge
        self.age_var = ctk.StringVar(value="")
        self.age_var.trace_add("write", lambda *args: self.update_total_callback())

        vcmd = (parent.register(self._valider_chiffres), '%P')

        # Conteneur principal
        self.contenant_global = ctk.CTkFrame(parent)
        self.contenant_global.grid_columnconfigure(0, weight=1)

        # Header
        header_frame = ctk.CTkFrame(self.contenant_global, fg_color=couleur_header)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        self.button_toggle = ctk.CTkButton(header_frame, text=titre, anchor="w", command=self.toggle)
        self.button_toggle.grid(row=0, column=0, sticky="ew", padx=(5, 2), pady=5)

        btn_dup = ctk.CTkButton(header_frame, text="D", width=30, command=lambda: on_duplicate_callback(self))
        btn_dup.grid(row=0, column=1, padx=2, pady=5)

        btn_del = ctk.CTkButton(header_frame, text="X", width=30, fg_color="#922b21", command=lambda: on_delete_callback(self))
        btn_del.grid(row=0, column=2, padx=(2, 5), pady=5)

        # Panneau affichable
        self.panneau_affichable = ctk.CTkFrame(self.contenant_global, fg_color=couleur_panneau)
        self.panneau_affichable.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.panneau_affichable.grid_columnconfigure(0, weight=1) 
       
        # Variable pour le nom
        self.nom_var = ctk.StringVar(value="")
        self.nom_var.trace_add("write", lambda *args: self.update_total_callback())

        self.widgets_data["nom_client"] = ctk.CTkEntry(
            self.panneau_affichable, 
            placeholder_text="Nom...",
            textvariable=self.nom_var
        )
        self.widgets_data["nom_client"].pack(pady=5, padx=10)   

        self.widgets_data["age"] = ctk.CTkEntry(
            self.panneau_affichable, 
            placeholder_text="Âge...", 
            textvariable=self.age_var,
            validate="key", 
            validatecommand=vcmd
        )
        self.widgets_data["age"].pack(pady=5, padx=10)
        
        # Case à cocher "actif"
        self.actif_var = ctk.BooleanVar(value=False)
        self.actif_var.trace_add("write", lambda *args: self.update_total_callback())

        self.widgets_data["actif"] = ctk.CTkCheckBox(
            self.panneau_affichable, 
            text="Zone Active",
            variable=self.actif_var
        )
        self.widgets_data["actif"].pack(pady=5, padx=10)

    def _valider_chiffres(self, contenu_futur):
        return (contenu_futur.isdigit() or contenu_futur == "") and len(contenu_futur) <= 3

    @property
    def age(self):
        val = self.age_var.get()
        return int(val) if val.isdigit() else 0
    
    @property
    def est_active(self):
        return self.actif_var.get()
    
    @property
    def nom_client(self):
        return self.nom_var.get()

    def toggle(self):
        if self.is_visible:
            self.panneau_affichable.grid_forget()
        else:
            self.panneau_affichable.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.is_visible = not self.is_visible

    def get_data(self):
        donnees = {"titre": self.titre, "nom_client": self.nom_client, "age": self.age, "actif": self.est_active}
        return donnees

    def set_data(self, data):
        if "nom_client" in data: self.nom_var.set(data["nom_client"])
        if "age" in data: self.age_var.set(str(data["age"]))
        if "actif" in data: self.actif_var.set(data["actif"])
                    
class MonApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x700")
        self.title("Accordéon Dynamique")

        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=1)

        self.manager = GridAccordionManager()

        # Frame de contrôle (Haut)
        ctrl_frame = ctk.CTkFrame(self)
        ctrl_frame.grid(column=0, row=0, sticky="ew", padx=10, pady=5)
        ctrl_frame.grid_columnconfigure(0, weight=1)

         # On ajoute une brique d'exemple pour montrer le fonctionnement dès le lancement
        tbric = brq.Brique(ctrl_frame, "Brique Exemple", couleur_header="lightblue", couleur_panneau="white")
        self.manager.register(tbric)
        tbric.contenant_global.grid(row=0, column=0, sticky="ew", padx=10, pady=5)  

        print(f"Prochaine ligne libre dans MonApp: {next_free_row(self)}")
        

        ctk.CTkButton(ctrl_frame, text="+ Ajouter une Zone", command=self.ajouter_zone).grid(row=next_free_row(self), column=0, padx=10, pady=5)
       
        self.label_statut = ctk.CTkLabel(ctrl_frame, text="○ Aucun actif", font=("Arial", 12))
        self.label_statut.grid(row=1, column=0, padx=10, pady=2, sticky="w")
        
        self.label_total = ctk.CTkLabel(ctrl_frame, text="Total des âges : 0", font=("Arial", 14, "bold"))
        self.label_total.grid(row=2, column=0, padx=10, pady=2, sticky="w")     

        self.label_noms_actifs = ctk.CTkLabel(
            self, 
            text="Aucune zone active", 
            font=("Arial", 11, "italic"),
            wraplength=450
        )
        self.label_noms_actifs.grid(column=0, row=2, pady=10, sticky="ew")

        # Zone de défilement (Milieu)
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(column=0, row=1, sticky="nsew", padx=10, pady=5)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

    @property
    def total_ages(self):
        return sum(zone.age for zone in self.manager.structures if hasattr(zone, 'age'))

    @property
    def au_moins_un_actif(self):
        return any(zone.est_active for zone in self.manager.structures if hasattr(zone, 'est_active'))

    @property
    def liste_noms_actifs(self):
        actifs = [zone.nom_client for zone in self.manager.structures if hasattr(zone, 'est_active') and zone.est_active]
        return ", ".join(actifs) if actifs else "Aucune zone active"

    def rafraichir_affichage(self):
        """Mise à jour synchronisée de l'interface."""
        # Mise à jour du Total
        self.label_total.configure(text=f"Total des âges : {self.total_ages}")
        
        # Mise à jour du Statut visuel
        if self.au_moins_un_actif:
            self.label_statut.configure(text="● 1 actif au moins", text_color="green")
        else:
            self.label_statut.configure(text="○ Aucun actif", text_color="gray")

        # Mise à jour de la liste textuelle
        texte_liste = f"Les zones confinées {self.liste_noms_actifs} sont actives"
        self.label_noms_actifs.configure(text=texte_liste)

    def ajouter_zone(self, titre=None, data_initiale=None):
        if titre is None:
            titre = f"Zone {len(self.manager.structures) + 1}"
        
        nouvelle_zone = ZoneConfinee(
            self.scroll_frame, titre, 
            self.supprimer_zone, self.dupliquer_zone,
            update_total_callback=self.rafraichir_affichage,
            couleur_header="lightgreen", couleur_panneau="lightgray"
        )
        
        if data_initiale:
            nouvelle_zone.set_data(data_initiale)

        self.manager.register(nouvelle_zone)
        self.manager.reorganize_grid()
        self.rafraichir_affichage()

    def dupliquer_zone(self, zone_a_copier):
        donnees_sources = zone_a_copier.get_data()
        nouveau_titre = f"{donnees_sources['titre']} (Copie)"
        self.ajouter_zone(titre=nouveau_titre, data_initiale=donnees_sources)

    def supprimer_zone(self, zone):
        self.manager.unregister(zone)
        zone.contenant_global.destroy()
        self.rafraichir_affichage()

if __name__ == "__main__":
    app = MonApp()
    app.mainloop()