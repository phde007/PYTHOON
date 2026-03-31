import customtkinter as ctk
from PIL import Image
from CTkToolTip import CTkToolTip


import customtkinter as ctk
from BriquesSaisieBase import BriqueSaisieBaseChantier
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
        self.title("Accordéon Dynamique")

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


          # On ajoute une brique d'exemple pour montrer le fonctionnement dès le lancement
        tbric = brq.Brique(self.scroll_frame, "Brique Exemple", manager =self.manager, couleur_header=cv.BRICK_HEADER_BG, couleur_panneau=cv.BRICK_PANEL_BG)
        self.manager.register(tbric)
        tbric.contenant_global.grid(row=0, column=0, sticky="ew", padx=10, pady=5)  


        # On ajoute une seconde brique d'exemple pour montrer le fonctionnement dès le lancement avec ses fonctions de callback d'affichage et de masquage
        def lors_de_l_ouverture():
            print("La brique est maintenant visible !")
            # Exemple : rafraîchir les étiquettes de l'application
            app.rafraichir_affichage()

        def lors_de_la_fermeture():
            print("La brique a été masquée.")


   
        tbric2 = brq.Brique(self.scroll_frame, "Brique N°2", manager =self.manager, couleur_header=cv.BRICK_HEADER_BG, 
                            couleur_panneau=cv.BRICK_PANEL_BG,on_show_callback=lors_de_l_ouverture,
                            on_hide_callback=lors_de_la_fermeture)
        self.manager.register(tbric2)
        tbric2.contenant_global.grid(row=next_free_row(self.scroll_frame), column=0, sticky="ew", padx=10, pady=5)  
        # 2. AJOUT DANS LE HEADER (après le titre et la navigation)
        # Le titre est en colonne 0, la navigation en colonne 1. On utilise la colonne 2.
        btn_header = ctk.CTkButton(tbric2.header_frame, text="Action Header", width=100, height=24)
        btn_header.grid(row=0, column=2, padx=10)
        # 3. AJOUT DANS LE PANNEAU
        # On récupère le frame du panneau via la méthode dédiée
        self.couleur_texte_panneau = good_contrast_font_color(cv.BRICK_PANEL_BG)
        print(f"Couleur de texte choisie pour le panneau : {self.couleur_texte_panneau}")
        panneau_cible = tbric2.get_panneau()
        panneau_cible.grid_columnconfigure(1, weight=1)
        label_interne = ctk.CTkLabel(panneau_cible, text="Ce widget a été ajouté depuis MonApp !", font=("Arial", 12),text_color=self.couleur_texte_panneau)
        label_interne.grid(row=0, column=0, padx=10, pady=10)
        
        # ajoutons deux champs de saisie dans le panneau de la brique N°2 pour montrer que le panneau peut contenir n'importe quel widget
        # et surtout que le panneau s'étire correctement pour les accueillir grâce au sticky="ew" géré par le manager lors de l'affichage de la brique
        label_champ1 = ctk.CTkLabel(panneau_cible, text="Champ de saisie 1 :", font=("Arial", 12), text_color=self.couleur_texte_panneau)
        label_champ1.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_champ1 = ctk.CTkEntry(panneau_cible)  
        entry_champ1.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        label_champ2 = ctk.CTkLabel(panneau_cible, text="Champ de saisie 2 :", font=("Arial", 12), text_color=self.couleur_texte_panneau)
        label_champ2.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        entry_champ2 = ctk.CTkEntry(panneau_cible)                  
        entry_champ2.grid(row=1, column=4, padx=10, pady=5, sticky="ew")

        # Ajout d'une brique de saisie spécifique pour l'identification du chantier, 
        # qui héritera de la classe de base de saisie et qui sera utilisée pour les données de chantier

        brique_chantier = BriqueSaisieBaseChantier(self.scroll_frame, manager=self.manager)
        self.manager.register(brique_chantier.interface)
      

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
        data_principale = {
            "total_ages": self.total_ages,
            "au_moins_un_actif": self.au_moins_un_actif,
            "liste_noms_actifs": self.liste_noms_actifs,
            "donnees_chantier": self.smc.get_data()  # On récupère les données de la brique de saisie de chantier
        }
        # On passe uniquement les structures gérées par le manager de l'application, 
        # qui sont les zones confinées (et pas les briques de saisie de base qui sont 
        # utilisées pour des données globales du chantier et qui ne sont pas destinées 
        # à être sauvegardées/restaurées dans le cadre de la gestion des zones confinées)
        if gd.sauvegarder_dossier(self.manager.structures):
            print("Sauvegarde réussie")

    def restaurer(self):
        donnees = gd.charger_dossier()
        if donnees:
            # 1. Nettoyer l'existant
            for s in list(self.manager.structures):
                self.supprimer_zone(s)
                
            # 2. Reconstruire
            for z_data in donnees:
                self.ajouter_zone(titre=z_data.get("titre"), data_initiale=z_data)


if __name__ == "__main__":
    app = MonApp()
    app.mainloop()