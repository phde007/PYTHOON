"""
Module BriqueSaisieAvecFilles : Contient la classe BriqueSaisieAvecFilles, une brique spécialisée pour la saisie de données,
mais ayant en plus des fonctionnalités pour gérer les données filles: soit une autre BriqueDeSaisieSansFilles, 
soit une autre BriqueDeSaisieAvecFilles.

Un exemple d'utilisation de cette classe est la BriqueSaisieZoneConfinee, qui permet de saisir les données d'une zone confinée,
et qui peut contenir des briques de saisie de zones élémentaires (BriqueSaisieZoneElementaire) qui sont des briques filles de 
la zone confinée.

Un exemple d'utilisation de cette classe est un ensemble de briques de saisie d'informations unitaires.

C'est une classe abstraite qui sert de base pour des briques plus spécifiques (ex : BriqueSaisieZoneConfinee, BriqueSaisieEquipement, etc.)
Elle hérite de Brique et ajoute des fonctionnalités spécifiques à la saisie (ex : champs de saisie, validation, etc.)  
Elle est conçue pour être utilisée dans des contextes où l'utilisateur doit entrer des données, comme les zones confinées,
les équipements, etc.
Elle est utilisée également pour les briques de saisie de famille de données utilisées une seule fois dans le programme
comme les briques de saisie d'informations client, d'informations sur le projet, etc.

"""
from numpy import var

from grid_manager import GridAccordionManager
import Brique as brk

class BriqueSaisieAvecFilles:
    def __init__(self, parent, titre, manager_parent, **kwargs):
        self.est_zone_dynamique = True # <--- C'est une brique dynamique, puisqu'elle peut contenir des briques filles 
        
        # 1. On stocke le manager de l'étage SUPÉRIEUR
        self.manager_parent = manager_parent
        
        # 2. On crée l'interface physique en lui passant le manager parent
        self.interface = brk.Brique(parent, titre, manager_parent, **kwargs)
        
        # 3. On crée un manager INTERNE pour les briques filles
        # On l'appelle self.manager_filles pour éviter toute confusion        
        self.manager_filles = GridAccordionManager()

    def get_data(self):
        # Correction : self.persist_vars au lieu de self.self.persist_vars
        data = {cle: (var.get() if hasattr(var, 'get') else var) 
                for cle, var in self.persist_vars.items()} #
        
        data["titre"] = self.interface.titre 

        # Export des enfants
        cle_enfant = getattr(self, "nom_cle_export", "enfants")
        # On appelle get_data sur les objets enregistrés dans le manager de filles
        data[cle_enfant] = [enfant.get_data() for enfant in self.manager_filles.structures 
                            if hasattr(enfant, 'get_data')]
        
        return data


    def set_data(self, data):
        if not data: return

        # 1. On restaure les champs simples automatiquement
        for cle, var in self.mapping_champs.items():
            if cle in data:
                var.set(data[cle])

        # 2. Restaure les enfants
        if "enfants" in data:
            # On boucle sur les structures du manager interne
            for i, enfant in enumerate(self.manager_filles.structures):
                if i < len(data["enfants"]):
                    enfant.set_data(data["enfants"][i])