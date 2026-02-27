import customtkinter as ctk
from PIL import Image
from CTkToolTip import CTkToolTip


from  ZoneElementaire import ZoneElementaire
from grid_manager import GridAccordionManager


import Brique as brq
from utilitaires import next_free_row
import visuel.constantes_couleurs as cv




class ZoneConfinee:
    def __init__(self, parent, titre, on_delete_callback, on_duplicate_callback, update_total_callback, 
                 couleur_header=cv.ZCONF_HEADER_BG, couleur_panneau=cv.ZCONF_PANEL_BG):
        self.is_visible = False
        self.titre = titre
        self.update_total_callback = update_total_callback

        self.widgets_data = {}
        
        # On initialise le manager  des souszones de la zone confinéeavec les icônes personnalisées des accordéons    
        self.manager = GridAccordionManager()

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
        header_frame.grid_columnconfigure(2, weight=3)  # Espace plus grand pour le nom de la zone confinée

        self.button_toggle = ctk.CTkButton(header_frame, text=titre, anchor="w", command=self.toggle)
        self.button_toggle.grid(row=0, column=0, sticky="ew", padx=(5, 2), pady=5)
        self.tooltip_toggle = CTkToolTip(self.button_toggle, message="Afficher/Masquer les détails de cette Zone Confinée")

        ' nom de la zone confinée dans le tooltip du header '
        # Nom de la Zone Confinée
        label_nom_zconf = ctk.CTkLabel(header_frame, text="Nom de la Zone Confinée: ")
        label_nom_zconf.grid(row=0, column=1, padx=(10, 5), pady=5)
        
        self.nom_zconf_var = ctk.StringVar(value="")
        self.widgets_data["nom_zconf"] = ctk.CTkEntry(
            header_frame,
            textvariable=self.nom_zconf_var,
            font=ctk.CTkFont(weight="bold")
        )
        self.widgets_data["nom_zconf"].grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.tooltip_nom_zconf = CTkToolTip(self.widgets_data["nom_zconf"], message="Saisissez le nom de cette Zone Confinée utilisé dans le plan de retrait ")  

        
        # Bouton ajouter zone élémentaire
        btn_add_zone = ctk.CTkButton(header_frame, text="+ Ajouter une Zone élémentaire", command=self.ajouter_zone)
        btn_add_zone.grid(row=0, column=3, padx=5, pady=5)
        self.tooltip_add_zone = CTkToolTip(btn_add_zone, message="Ajouter une nouvelle zone élémentaire")

        duplicate_icon = ctk.CTkImage(dark_image=Image.open(r".\visuel\duplicate.png"), size=(20,20))
        btn_dup = ctk.CTkButton(header_frame, image=duplicate_icon, text="", width=30, command=lambda: on_duplicate_callback(self))
        btn_dup.grid(row=0, column=4, padx=2, pady=5)
        self.tooltip_dup = CTkToolTip(btn_dup, message="Dupliquer cette zone et toutes ses sous-zones")

        # suppression avec icône de poubelle
        poubelle = ctk.CTkImage(dark_image=Image.open(r".\visuel\bin.png"), size=(20,20))
        btn_del = ctk.CTkButton(header_frame, image=poubelle, text="", width=30, fg_color=cv.CANCEL_BUTTON_BG, command=lambda: on_delete_callback(self))
        btn_del.grid(row=0, column=5, padx=(2, 5), pady=5)
        self.tooltip_del = CTkToolTip(btn_del, message="Supprimer cette zone et toutes ses sous-zones")

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
        self.widgets_data["nom_client"].grid(row = 0, column=0, pady=5, padx=10)   

        self.widgets_data["age"] = ctk.CTkEntry(
            self.panneau_affichable, 
            placeholder_text="Âge...", 
            textvariable=self.age_var,
            validate="key", 
            validatecommand=vcmd
        )
        self.widgets_data["age"].grid(row=1, column=0, pady=5, padx=10)
        
        # Case à cocher "actif"
        self.actif_var = ctk.BooleanVar(value=False)
        self.actif_var.trace_add("write", lambda *args: self.update_total_callback())

        self.widgets_data["actif"] = ctk.CTkCheckBox(
            self.panneau_affichable, 
            text="Zone Active",
            variable=self.actif_var
        )
        self.widgets_data["actif"].grid(row=2, column=0,pady=5, padx=10)  

        # Conteneur pour les zones élémentaires
        self.container_elements = ctk.CTkFrame(self.panneau_affichable, fg_color="transparent")
        self.container_elements.grid(row=next_free_row(self.panneau_affichable), column=0, sticky="nsew", pady=5)
        self.container_elements.grid_columnconfigure(0, weight=1)  

        #  Widgets post zones élémentaires
        self.label_total_volume = ctk.CTkLabel(
            self.panneau_affichable, 
            text="Total des volumes : 0", 
            font=("Arial", 14, "bold")
        )   
        self.label_total_volume.grid(row=next_free_row(self.panneau_affichable), column=0, padx=10, pady=5, sticky="w")


    def rafraichir_affichage(self):
        """Mise à jour synchronisée de l'interface.
        - Total des volumes
        - Statut visuel (actif/inactif) de la zone confinée"""
        
        
        # Affichage du total des volumes de la zone confinée (somme des volumes de ses zones élémentaires)
        self.label_total_volume.configure(text=f"Total des volumes : {self.total_volume}")
        
    """ 
            # Mise à jour du Statut visuel
            if self.au_moins_un_actif:
                self.label_statut.configure(text="● 1 actif au moins", text_color="green")
            else:
                self.label_statut.configure(text="○ Aucun actif", text_color="gray")

            # Mise à jour de la liste textuelle
            texte_liste = f"Les zones élémentaires {self.liste_noms_actifs} sont actives"
            self.label_noms_actifs.configure(text=texte_liste)
 """


    def dupliquer_zone(self, zone_a_copier):
        donnees_sources = zone_a_copier.get_data()
        nouveau_titre = f"{donnees_sources['titre']} (Copie)"
        self.ajouter_zone(titre=nouveau_titre, data_initiale=donnees_sources)

    def supprimer_zone(self, zone):
        self.manager.unregister(zone)
        zone.contenant_global.destroy()
        self.rafraichir_affichage()    

    def ajouter_zone(self, titre=None, data_initiale=None):
        if titre is None:
            titre = f"Zone élémentaire {len(self.manager.structures) + 1}"        
    
        nouvelle_zone = ZoneElementaire(
            parent=self.container_elements,
            titre=titre, 
            on_delete_callback=self.supprimer_zone, 
            on_duplicate_callback=self.dupliquer_zone,
            # On crée une fonction intermédiaire qui rafraîchit la ZoneConfinee 
            # PUIS appelle le callback de MonApp
            update_total_callback=lambda: [self.rafraichir_affichage(), self.update_total_callback()]
        )
    
        if data_initiale:
         nouvelle_zone.set_data(data_initiale)

        self.manager.register(nouvelle_zone)
        self.manager.reorganize_grid()
        self.rafraichir_affichage()
    
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
    
    # @property
    # def volume(self):
    #     val = self.volume_var.get()
    #     return int(val) if val.isdigit() else 0

    @property
    def total_volume(self):
        volumes = [zone.volume for zone in self.manager.structures if hasattr(zone, 'volume')]
        total = sum(volumes)
        print(f"DEBUG - Nombre d'éléments: {len(self.manager.structures)}, Premier élément a 'volume': {hasattr(self.manager.structures[0], 'volume') if self.manager.structures else 'N/A'}")
        if volumes:
            print(f"DEBUG - Total volume: {total}, First zone volume: {volumes[0]}")
        else:
            print(f"DEBUG - Total volume: {total}, No zones found")
        return total
        return sum(zone.volume for zone in self.manager.structures if hasattr(zone, 'volume'))
        

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
