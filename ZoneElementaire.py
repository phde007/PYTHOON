from tkinter import Image

import CTkToolTip
import PIL
import customtkinter as ctk
from grid_manager import GridAccordionManager
from CTkToolTip import *
from PIL import Image
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
        CTkToolTip(self.button_toggle, "Afficher/Masquer les détails de cette Zone Confinée")

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
        CTkToolTip (self.widgets_data["nom_zconf"], "Saisissez le nom de cette Zone Confinée utilisé dans le plan de retrait ")  

        
        # Bouton ajouter Appareil
        btn_add_zone = ctk.CTkButton(header_frame, text="+ Ajouter un Appareil", width=150)
        btn_add_zone.grid(row=0, column=3, padx=5, pady=5)
        CTkToolTip(btn_add_zone, "Ajouter un nouvel appareil")

        duplicate_icon = ctk.CTkImage(dark_image=Image.open(r".\visuel\duplicate.png"), size=(20,20))
        btn_dup = ctk.CTkButton(header_frame, image=duplicate_icon, text="", width=30, command=lambda: on_duplicate_callback(self))
        btn_dup.grid(row=0, column=4, padx=2, pady=5)
        CTkToolTip(btn_dup, "Dupliquer cette zone et toutes ses sous-zones")

        # suppression avec icône de poubelle
        poubelle = ctk.CTkImage(dark_image=PIL.Image.open(r".\visuel\bin.png"), size=(20,20))
        btn_del = ctk.CTkButton(header_frame, image=poubelle, text="", width=30, fg_color=cv.CANCEL_BUTTON_BG, command=lambda: on_delete_callback(self))
        btn_del.grid(row=0, column=5, padx=(2, 5), pady=5)
        CTkToolTip(btn_del, "Supprimer cette zone et toutes ses sous-zones")

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
