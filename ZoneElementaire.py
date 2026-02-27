import customtkinter as ctk
from PIL import Image
from CTkToolTip import CTkToolTip


from  Appareils import Appareil
from grid_manager import GridAccordionManager


import Brique as brq
from utilitaires import next_free_row
import visuel.constantes_couleurs as cv




class ZoneElementaire:
    def __init__(self, parent, titre, on_delete_callback, on_duplicate_callback, update_total_callback, 
                 couleur_header=cv.ZEL_HEADER_BG, couleur_panneau=cv.ZEL_PANEL_BG):
        self.is_visible = False
        self.titre = titre
        self.update_total_callback = update_total_callback

        self.widgets_data = {}
        
        # On initialise le manager  des sous-zones de la zone élémentaire (en particulier les appareils) 
        # avec les icônes personnalisées des accordéons    
        self.manager = GridAccordionManager()
    
        """ # Variable de contrôle pour le volume
        self.volume_var = ctk.StringVar(value="")
        # self.volume_var.trace_add("write", lambda *args: self.update_total_callback())
        self.volume_var.trace_add("write", lambda *args: print(f"Trace activée ! Valeur : {self.volume_var.get()}")) """

        """
        EXPLICATION DE LA TRACE :
        Dans Tkinter (et CustomTkinter), trace_add est une méthode qui dit au programme :
        "Surveille cette variable. Dès que quelqu'un écrit dedans ("write"), déclenche immédiatement cette fonction."

        self.volume_var.trace_add("write", lambda *args: self.update_total_callback()):
        "write" : C'est l'événement surveillé (la modification du texte).
        lambda *args: ... : C'est la réaction. On utilise *args car Tkinter envoie automatiquement trois arguments techniques 
        (le nom de la variable, l'index, le mode) dont nous n'avons généralement pas besoin ici.

        self.update_total_callback() : C'est l'action finale (recalculer les totaux)."""



        

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
        self.tooltip_toggle = CTkToolTip(self.button_toggle, message="Afficher/Masquer les détails de cette Zone Elémentaire")

        ' nom de la zone élémentaire dans le tooltip du header '
        # Nom de la Zone Elémentaire
        label_nom_zele = ctk.CTkLabel(header_frame, text="Nom de la Zone Elémentaire: ")
        label_nom_zele.grid(row=0, column=1, padx=(10, 5), pady=5)
        
        self.nom_zele_var = ctk.StringVar(value="")
        self.widgets_data["nom_zele"] = ctk.CTkEntry(
            header_frame,
            textvariable=self.nom_zele_var,
            font=ctk.CTkFont(weight="bold")
        )
        self.widgets_data["nom_zele"].grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.tooltip_nom_zele = CTkToolTip(self.widgets_data["nom_zele"], message="Saisissez le nom de cette Zone Elémentaire utilisé  dans le plan de retrait ")  

        
        # Bouton ajouter un appareil
        btn_add_zone = ctk.CTkButton(header_frame, text="+ Ajouter un appareil", command=self.ajouter_zone)
        btn_add_zone.grid(row=0, column=3, padx=5, pady=5)
        self.tooltip_add_zone = CTkToolTip(btn_add_zone, message="Ajouter un appareil à cette zone élémentaire")

        duplicate_icon = ctk.CTkImage(dark_image=Image.open(r".\visuel\duplicate.png"), size=(20,20))
        btn_dup = ctk.CTkButton(header_frame, image=duplicate_icon, text="", width=30, command=lambda: on_duplicate_callback(self))
        btn_dup.grid(row=0, column=4, padx=2, pady=5)
        self.tooltip_dup = CTkToolTip(btn_dup, message="Dupliquer cette zone élémentaire et tous ses appareils")

        # suppression avec icône de poubelle
        poubelle = ctk.CTkImage(dark_image=Image.open(r".\visuel\bin.png"), size=(20,20))
        btn_del = ctk.CTkButton(header_frame, image=poubelle, text="", width=30, fg_color=cv.CANCEL_BUTTON_BG, command=lambda: on_delete_callback(self))
        btn_del.grid(row=0, column=5, padx=(2, 5), pady=5)
        self.tooltip_del = CTkToolTip(btn_del, message="Supprimer cette zone élémentaire et tous ses appareils")

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

        # Entrée pour le volume
        self.volume_var = ctk.StringVar(value="")
        self.volume_var.trace_add("write", lambda *args: self.update_total_callback())
              
        self.widgets_data["volume"] = ctk.CTkEntry(
            self.panneau_affichable, 
            placeholder_text="Volume...",
            textvariable=self.volume_var,
            #validate="key", 
            #validatecommand=vcmd  # Réactivez la validation pour éviter les erreurs de conversion int()
        )
        self.widgets_data["volume"].grid(row=1, column=0, pady=5, padx=10)
        self.volume_var.set("15")

        
        # Case à cocher "actif"
        self.actif_var = ctk.BooleanVar(value=False)
        self.actif_var.trace_add("write", lambda *args: self.update_total_callback())

        self.widgets_data["actif"] = ctk.CTkCheckBox(
            self.panneau_affichable, 
            text="Zone Active",
            variable=self.actif_var
        )
        self.widgets_data["actif"].grid(row=2, column=0,pady=5, padx=10)  

        # Conteneur pour les appareils
        self.container_elements = ctk.CTkFrame(self.panneau_affichable, fg_color="transparent")
        self.container_elements.grid(row=next_free_row(self.panneau_affichable), column=0, sticky="nsew", pady=5)
        self.container_elements.grid_columnconfigure(0, weight=1)  

    def rafraichir_affichage(self):
        """
        ce rafraîchissement doit être appelé à chaque modification des  appareils pour assurer le cumul
        des différents débits . 
        
        Mise à jour synchronisée de l'interface.
        - Total des volumes
        - Statut visuel (actif/inactif) de la zone confinée
        # Mise à jour du volume total de la zone confinée (somme des volumes de ses zones élémentaires)
        self.label_total.configure(text=f"Total des volumes : {self.total_volume}")
        
        # Mise à jour du Statut visuel
        if self.au_moins_un_actif:
            self.label_statut.configure(text="● 1 actif au moins", text_color="green")
        else:
            self.label_statut.configure(text="○ Aucun actif", text_color="gray")

        # Mise à jour de la liste textuelle
        texte_liste = f"Les zones élémentaires {self.liste_noms_actifs} sont actives"
        self.label_noms_actifs.configure(text=texte_liste)
            """
        pass

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
            titre = f"Appareil {len(self.manager.structures) + 1}"        
        nouvelle_zone = Appareil(
       parent=self.container_elements,
       titre=titre, 
       on_delete_callback=self.supprimer_zone, 
       on_duplicate_callback=self.dupliquer_zone,
       update_total_callback=self.update_total_callback # Remonte vers ZoneConfinee.rafraichir_affichage
    )
  
        
        if data_initiale:
            nouvelle_zone.set_data(data_initiale)

        self.manager.register(nouvelle_zone)
        self.manager.reorganize_grid()
        self.rafraichir_affichage()
    def _valider_chiffres(self, contenu_futur):
        return (contenu_futur.isdigit() or contenu_futur == "") and len(contenu_futur) <= 3

    
    @property
    def est_active(self):
        return self.actif_var.get()
    
    @property
    def nom_client(self):
        return self.nom_var.get()
    
    @property
    def volume(self):
        val = self.volume_var.get()
        return int(val) if val.isdigit() else 0

    def toggle(self):
        if self.is_visible:
            self.panneau_affichable.grid_forget()
        else:
            self.panneau_affichable.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.is_visible = not self.is_visible

    def get_data(self):
        donnees = {"titre": self.titre, "nom_client": self.nom_client, "volume": self.volume, "actif": self.est_active}
        return donnees

    def set_data(self, data):
        if "nom_client" in data: self.nom_var.set(data["nom_client"])
        if "volume" in data: self.volume_var.set(str(data["volume"]))
        if "actif" in data: self.actif_var.set(data["actif"])
