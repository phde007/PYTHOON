import customtkinter as ctk
from PIL import Image
from CTkToolTip import CTkToolTip


from  Appareils import Appareil
from grid_manager import GridAccordionManager


import Brique as brq
from utilitaires import next_free_row
import visuel.constantes_couleurs as cv




class Appareil:
    def __init__(self, parent, titre, on_delete_callback, on_duplicate_callback, update_total_callback, 
                 couleur_header=cv.APP_HEADER_BG, couleur_panneau=cv.APP_PANEL_BG):
        self.is_visible = False
        self.titre = titre
        self.update_total_callback = update_total_callback

        self.widgets_data = {}
        
        
        """ # Variable de contrôle pour le débit
        self.débit_var = ctk.StringVar(value="")
        # self.débit_var.trace_add("write", lambda *args: self.update_total_callback())
        self.débit_var.trace_add("write", lambda *args: print(f"Trace activée ! Valeur : {self.débit_var.get()}")) """

        """
        EXPLICATION DE LA TRACE :
        Dans Tkinter (et CustomTkinter), trace_add est une méthode qui dit au programme :
        "Surveille cette variable. Dès que quelqu'un écrit dedans ("write"), déclenche immédiatement cette fonction."

        self.débit_var.trace_add("write", lambda *args: self.update_total_callback()):
        "write" : C'est l'événement surveillé (la modification du texte).
        lambda *args: ... : C'est la réaction. On utilise *args car Tkinter envoie automatiquement trois arguments techniques 
        (le nom de la variable, l'index, le mode) dont nous n'avons généralement pas besoin ici.

        self.update_total_callback() : C'est l'action finale (recalculer les totaux)."""



        
        # valide que la saisie soit un nombre entier limité à 3 chiffres '
        vcme = (parent.register(self._valider_chiffres), '%P')
        # valide que la saisie  soit un nombre décimal (avec un point ou une virgule)
        vcmd = (parent.register(self._valider_nombre), '%P')
        #valide que la saisie soit un nombre décimal signé (avec un point ou une virgule)
        vcmd_signed = (parent.register(self._valider_nombre_signé), '%P')


        # Conteneur principal
        self.contenant_global = ctk.CTkFrame(parent)
        self.contenant_global.grid_columnconfigure(0, weight=1)

        
        #region Header Appareil

        header_frame = ctk.CTkFrame(self.contenant_global, fg_color=couleur_header)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(2, weight=3)  # Espace plus grand pour le nom de la zone confinée

        self.button_toggle = ctk.CTkButton(header_frame, text=titre, anchor="w", command=self.toggle)
        self.button_toggle.grid(row=0, column=0, sticky="ew", padx=(5, 2), pady=5)
        self.tooltip_toggle = CTkToolTip(self.button_toggle, message="Afficher/Masquer les détails de cet appareil")

        # Type de l'appareil 
        label_type = ctk.CTkLabel(header_frame, text="Type: ")
        label_type.grid(row=0, column=1, padx=(10, 5), pady=5)

        self.type_var = ctk.StringVar(value="")
        self.widgets_data["type"] = ctk.CTkComboBox(
            header_frame,
            values=["Sas Personnel", "Sas Matériel", "EACM", "Extracteur", "EAR"],
            variable=self.type_var,
            font=ctk.CTkFont(weight="bold"),        
            state="readonly"
        )

        self.widgets_data["type"].grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.tooltip_type = CTkToolTip(self.widgets_data["type"], message="Sélectionnez le type d'appareil")
       
        self.nombre_appareils_var = ctk.StringVar(value="1")
        self.widgets_data["nombre_appareils"] = ctk.CTkEntry(
            header_frame,
            width=50,
            textvariable=self.nombre_appareils_var
            validate="key", 
            validatecommand=vcmc  # vérification caractère par caractère du format de nombre entier
        )
        self.widgets_data["nombre_appareils"].grid(row=0, column=3, padx=2, pady=5)

        duplicate_icon = ctk.CTkImage(dark_image=Image.open(r".\visuel\duplicate.png"), size=(20,20))
        btn_dup = ctk.CTkButton(header_frame, image=duplicate_icon, text="", width=30, command=lambda: on_duplicate_callback(self))
        btn_dup.grid(row=0, column=4, padx=2, pady=5)
        self.tooltip_dup = CTkToolTip(btn_dup, message="Dupliquer cet appareil avec les mêmes paramètres")

        # suppression avec icône de poubelle
        poubelle = ctk.CTkImage(dark_image=Image.open(r".\visuel\bin.png"), size=(20,20))
        btn_del = ctk.CTkButton(header_frame, image=poubelle, text="", width=30, fg_color=cv.CANCEL_BUTTON_BG, command=lambda: on_delete_callback(self))
        btn_del.grid(row=0, column=5, padx=(2, 5), pady=5)
        self.tooltip_del = CTkToolTip(btn_del, message="Supprimer cet appareil")

        #region  Panneau Affichable
        self.panneau_affichable = ctk.CTkFrame(self.contenant_global, fg_color=couleur_panneau)
        self.panneau_affichable.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.panneau_affichable.grid_columnconfigure(0, weight=1) 
       
        self.label_debit = ctk.CTkLabel(self.panneau_affichable, text="Débit (m³/h) :")
        # Entrée pour le débit de l'appareil

        self.débit_var = ctk.StringVar(value="")
        self.débit_var.trace_add("write", lambda *args: self.update_total_callback())
              
        self.widgets_data["débit"] = ctk.CTkEntry(
            self.panneau_affichable, 
            placeholder_text="débit...",
            textvariable=self.débit_var,
            validate="key", 
            validatecommand=vcmd  # vérification caractère par caractère du format de nombre décimal (avec point ou virgule)
        )
        self.widgets_data["débit"].grid(row=1, column=0, pady=5, padx=10)
        self.débit_var.set("15")




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

        #  Validation pour n'accepter que des chiffres et un seul point ou une seule virgule (saisie d'un nombre entier limité à 3 chiffres)
    def _valider_chiffres(self, contenu_futur):
        return (contenu_futur.isdigit() or contenu_futur == "") and len(contenu_futur) <= 3
    
    #  Validation pour n'accepter que les chiffres et un seul point ou une seule virgule (saisie d'un nombre décimal)
    def _valider_nombre(self, contenu_futur):
        if contenu_futur == "": return True
        # Autorise les chiffres, un seul point ou une seule virgule
        import re
        return bool(re.match(r"^\d*[.,]?\d*$", contenu_futur))
    
    # validation qu'on n'accepte que des caractères de nombre décimal signé (avec un point ou une virgule)
    def _valider_nombre_signé(self, contenu_futur):
        if contenu_futur == "": return True
        # Autorise les chiffres, un seul point ou une seule virgule, et un signe moins au début
        import re
        return bool(re.match(r"^-?\d*[.,]?\d*$", contenu_futur))

    
    @property
    def est_active(self):
        return self.actif_var.get()
    
    @property
    def nom_client(self):
        return self.nom_var.get()
    
    # Dans ZoneElementaire.py - VERSION CORRIGÉE
    @property
    def débit(self):
        texte = self.débit_var.get().replace(',', '.')
        try:
            return float(texte) if texte else 0.0
        except ValueError:
            return 0.0

    def toggle(self):
        if self.is_visible:
            self.panneau_affichable.grid_forget()
        else:
            self.panneau_affichable.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.is_visible = not self.is_visible

    def get_data(self):
        donnees = {"titre": self.titre, "nom_client": self.nom_client, "débit": self.débit, "actif": self.est_active}
        return donnees

    def set_data(self, data):
    
        if "débit" in data: self.débit_var.set(str(data["débit"]))
        if "type" in data: self.nom_var.set(data["type"])
   
