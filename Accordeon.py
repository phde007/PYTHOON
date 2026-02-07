import customtkinter as ctk
from grid_manager import GridAccordionManager

class ZoneConfinee:
    def __init__(self, parent, titre, on_delete_callback):
        self.is_visible = False
        
        # Frame principal de la zone
        self.contenant_global = ctk.CTkFrame(parent)
        self.contenant_global.grid_columnconfigure(0, weight=1)

        # Sous-frame pour le header (Bouton Toggle + Bouton Supprimer)
        header_frame = ctk.CTkFrame(self.contenant_global, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        # Bouton d'affichage
        self.button_toggle = ctk.CTkButton(header_frame, text=titre, anchor="w")
        self.button_toggle.grid(row=0, column=0, sticky="ew", padx=(5, 2), pady=5)

        # Bouton de suppression (X)
        btn_del = ctk.CTkButton(header_frame, text="X", width=30, fg_color="#922b21", 
                                 command=lambda: on_delete_callback(self))
        btn_del.grid(row=0, column=1, padx=(2, 5), pady=5)

        # Panneau affichable
        self.panneau_affichable = ctk.CTkFrame(self.contenant_global, fg_color="gray20")
        self.panneau_affichable.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        ctk.CTkLabel(self.panneau_affichable, text=f"Contenu de {titre}").pack(pady=10)
        self.panneau_affichable.grid_forget()

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

    def ajouter_zone(self):
        nom = f"Zone {len(self.manager.structures) + 1}"
        # On passe la fonction de suppression en callback
        nouvelle_zone = ZoneConfinee(self.scroll_frame, nom, self.supprimer_zone)
        
        # On l'enregistre dans le manager
        self.manager.register(nouvelle_zone)
        # On force le placement initial
        self.manager.reorganize_grid()

    def supprimer_zone(self, zone):
        # 1. On le retire du manager
        self.manager.unregister(zone)
        # 2. On détruit le widget
        zone.contenant_global.destroy()

if __name__ == "__main__":
    app = MonApp()
    app.mainloop()