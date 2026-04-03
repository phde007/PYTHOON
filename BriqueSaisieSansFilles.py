"""
Module BriqueSaisieSansFilles : Contient la classe BriqueSaisieSansFilles, une brique spécialisée pour la saisie de données.
C'est une classe abstraite qui sert de base pour des briques plus spécifiques (ex : BriqueSaisieZoneConfinee, BriqueSaisieEquipement, etc.)
Elle hérite de Brique et ajoute des fonctionnalités spécifiques à la saisie (ex : champs de saisie, validation, etc.)  
Elle est conçue pour être utilisée dans des contextes où l'utilisateur doit entrer des données, comme les zones confinées,
les équipements, etc.
Elle est utilisée également pour les briques de saisie de famille de données utilisées une seule fois dans le programme
comme les briques de saisie d'informations client, d'informations sur le projet, etc.

"""
class BriqueSaisieSansFilles:
    def __init__(self, parent, titre, manager, **kwargs):
        
        self.est_zone_dynamique = False # Par défaut, on considère que c'est une brique fixe 
        #(une brique de saisie sans filles est par définition une brique fixe, puisqu'elle ne peut pas contenir 
        # de briques filles dynamiques)

        import Brique as brk
        # On crée l'interface physique
        self.interface = brk.Brique(parent, titre, manager, **kwargs)
        self.persist_vars = {}

    def get_data(self):
        """Récupère les données de toutes les variables enregistrées."""
        return {k: v.get() for k, v in self.persist_vars.items()}

    def set_data(self, data):
        """Restaure les données dans les variables."""
        for k, v in data.items():
            if k in self.persist_vars:
                self.persist_vars[k].set(v)