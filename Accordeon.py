import customtkinter as ctk
from PIL import Image
from CTkToolTip import CTkToolTip


import customtkinter as ctk
import BriquesSaisieBase as bsb

from grid_manager import GridAccordionManager

import Brique as brq
from utilitaires import next_free_row, good_contrast_font_color
import visuel.constantes_couleurs as cv
from ZoneConfinee import ZoneConfinee

import sauvegarde_restauration as gd

#region Application Principale                    
class MonApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x700")
        self.title("DREETS - Assistant de Contrôle et de validation des Bilans aérauliques - v1.0")

        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=1)

        # self.icon_open = ctk.CTkImage(dark_image=Image.open(r".\visuel\chevron_droite.png"), size=(20,20))
        # self.icon_closed = ctk.CTkImage(dark_image=Image.open(r".\visuel\chevron_bas.png"), size=(20,20))
        # On initialise le manager avec les icônes personnalisées des accordéons    
        self.manager = GridAccordionManager()

        # Frame de contrôle (Haut), destiné à recueillir les boutons d'ajout de zones, de sauvegarde/restauration, et autres contrôles globaux
        ctrl_frame = ctk.CTkFrame(self)
        ctrl_frame.grid(column=0, row=0, sticky="ew", padx=10, pady=5)
        ctrl_frame.grid_columnconfigure(0, weight=1)

       # Titre de l'application dans le frame de contrôle
        label_titre = ctk.CTkLabel(ctrl_frame, text="Assistant de Contrôle et de validation des Bilans aérauliques", font=("Arial", 24, "bold"))
        label_titre.grid(row=0, column=0, columnspan=5, padx=10, pady=5)


       
        
        
        # Boutons de sauvegarde et restauration

        rr= next_free_row(ctrl_frame)
        ctk.CTkButton(ctrl_frame, text="💾 Sauvegarder le dossier en cours", command=self.sauvegarder).grid(row=rr, column=1, padx=5)
        ctk.CTkButton(ctrl_frame, text="📂 Restaurer un dossier enregistré", command=self.restaurer).grid(row=rr, column=2, sticky="w", padx=5)

        ctk.CTkButton(ctrl_frame, text="+ Ajouter une Zone Confinée", command=self.ajouter_zone).grid(row=rr, column=0, padx=10, pady=5)
       
        # self.label_statut = ctk.CTkLabel(ctrl_frame, text="○ Aucun actif", font=("Arial", 12))
        # self.label_statut.grid(row=1, column=0, padx=10, pady=2, sticky="w")
        
        self.label_total = ctk.CTkLabel(ctrl_frame, text="Total des âges : 0", font=("Arial", 14, "bold"))
        self.label_total.grid(row=3, column=0, padx=10, pady=2, sticky="w")     

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


        #region briques Base

        # Ajout d'une brique de test contenant une autre brique de test
        self.brique_test_avec_filles = bsb.BriqueContenanteTest(self.scroll_frame, "Brique avec filles", manager=self.manager)
        self.brique_test_avec_filles.id_restauration = "brique_test_avec_filles" # On quement par la méthode de restauration
        self.manager.register(self.brique_test_avec_filles)




       
        # Ajout d'une brique purement documentaire qui pointe vers la documentation officielle de la méthode de calcul des bilans aérauliques, 


        self.brique_documentation_reglementaire = bsb.BriqueSaisieDocumentationReglementaire(self.scroll_frame, manager=self.manager)
        self
        self.manager.register(self.brique_documentation_reglementaire)

         

        # Ajout d'une brique de saisie spécifique pour l'identification du chantier, 
        # qui héritera de la classe de base de saisie et qui sera utilisée pour les données de chantier

        self.brique_chantier = bsb.BriqueSaisieBaseChantier(self.scroll_frame, manager=self.manager)
        self.brique_chantier.id_restauration = "brique_chantier"
        self.manager.register(self.brique_chantier)
      

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

        """
        # Mise à jour synchronisée de l'interface."
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
        """
        pass

    def ajouter_zone(self, titre=None, data_initiale=None):
        if titre is None:
            titre = f"Zone {len(self.manager.structures) + 1}"
        
        # Masquer tous les éléments rattachés au manager courant
        self.manager.hide_all()

        nouvelle_zone = ZoneConfinee(
            parent=self.scroll_frame, 
            titre=titre, 
            manager=self.manager,  # On passe explicitement le manager de l'app
            on_delete_callback=self.supprimer_zone, 
            on_duplicate_callback=self.dupliquer_zone,
            update_total_callback=self.rafraichir_affichage
        )
        nouvelle_zone.est_zone_dynamique = True # Forcément une zone confinée est une zone dynamique
        
        if data_initiale:
            nouvelle_zone.set_data(data_initiale)

        self.manager.register(nouvelle_zone)
        self.manager.reorganize_grid()
        self.update()
        self.rafraichir_affichage()

    def dupliquer_zone(self, zone_a_copier):
        donnees_sources = zone_a_copier.get_data()
        nouveau_titre = f"{donnees_sources['titre']} (Copie)"
        self.ajouter_zone(titre=nouveau_titre, data_initiale=donnees_sources)

    def supprimer_zone(self, zone):
        self.manager.unregister(zone)
        zone.contenant_global.destroy()
        self.rafraichir_affichage()

        

    def sauvegarder(self):
        data_a_sauver = {
            "infos_globales": self.get_infos_globales(),
            "zones_confinees": []
        }

        for z in self.manager.structures:
            if not hasattr(z, 'get_data'): continue
            
            # Cas 1 : Brique fixe (on crée une clé spécifique dans le dictionnaire)
            if hasattr(z, 'id_restauration'):
                data_a_sauver[z.id_restauration] = z.get_data()
                
            # Cas 2 : Brique dynamique (on l'ajoute à la liste)
            elif getattr(z, 'est_zone_dynamique', False):
                data_a_sauver["zones_confinees"].append(z.get_data())

        gd.sauvegarder_dossier(data_a_sauver)


    def restaurer(self):
        donnees = gd.charger_dossier()
        if not donnees: return

        # --- PARTIE 1 : Restauration des briques fixes ---
        # On boucle sur les structures actuelles du manager
        for z in self.manager.structures:
            # Si la brique a un ID et que cet ID est présent dans le fichier JSON
            restoration_id = getattr(z, 'id_restauration', None)
            if restoration_id and restoration_id in donnees:
                z.set_data(donnees[restoration_id])

        # --- PARTIE 2 : Restauration des zones dynamiques ---
        # On nettoie les zones existantes
        for z in list(self.manager.structures):
            if getattr(z, 'est_zone_dynamique', False):
                self.supprimer_zone(z)

        # On recrée les zones à partir de la liste JSON
        for z_data in donnees.get("zones_confinees", []):
            if z_data:
                self.ajouter_zone(titre=z_data.get("titre"), data_initiale=z_data)

if __name__ == "__main__":
    app = MonApp()
    app.mainloop()