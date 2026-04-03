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


class BriqueSaisieAvecFilles:
    def __init__(self, parent, titre, manager_parent, **kwargs):
        import Brique as brk
        
        # 1. On stocke le manager de l'étage SUPÉRIEUR
        self.manager_parent = manager_parent
        
        # 2. On crée l'interface physique en lui passant le manager parent
        self.interface = brk.Brique(parent, titre, manager_parent, **kwargs)
        
        # 3. On crée un manager INTERNE pour les briques filles
        # On l'appelle self.manager_filles pour éviter toute confusion        
        self.manager_filles = GridAccordionManager()

    def get_data(self):
        # 1. On récupère automatiquement les champs simples
        # Note : on vérifie si la variable a une méthode .get() pour éviter les erreurs avec des types de variables non standard
        data = {cle: (var.get() if hasattr(var, 'get') else var) for cle, var in self.mapping_champs.items()}
        
        # 2. On ajoute les données structurelles fixes
        data["titre"] = self.titre

        # 3. Export des enfants (on utilise une clé dynamique selon le besoin)
        # Si c'est une ZoneConfinee, la clé sera 'zones_elementaires'
        # Si c'est une ZoneElementaire, ce sera 'appareils'
        cle_enfant = getattr(self, "nom_cle_export", "enfants")
        data[cle_enfant] = [enfant.get_data() for enfant in self.manager.structures]
        
        return data


    def get_data(self):
        # Récupération des champs locaux via le mapping
        data = {cle: (var.get() if hasattr(var, 'get') else var) 
                for cle, var in self.mapping_champs.items()}
        
        data["titre"] = self.interface.titre # Utilise le titre de l'interface

        # On demande l'export aux enfants via le manager INTERNE
        cle_enfant = getattr(self, "nom_cle_export", "enfants")
        data[cle_enfant] = [enfant.get_data() for enfant in self.manager_filles.structures]
        
        return data


    def set_data(self, data):
        if not data: return

        # 1. On restaure les champs simples automatiquement
        for cle, var in self.mapping_champs.items():
            if cle in data:
                var.set(data[cle])

        # 2. On restaure les enfants (Partie répétitive)
        if "enfants" in data:
            for enfant_data in data["enfants"]:
                # On appelle votre méthode de création habituelle
                self.ajouter_zone(titre=enfant_data.get("titre"), data_initiale=enfant_data)