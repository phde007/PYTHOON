class Appareil:
    """Base class for apparatus/equipment."""
    
    def __init__(self, nom, modele):
        """
        Initialize an Appareil instance.
        
        Args:
            nom (str): Name of the apparatus
            modele (str): Model of the apparatus
        """
        self.nom = nom
        self.modele = modele
    
    def __str__(self):
        return f"{self.nom} - {self.modele}"
    
    def __repr__(self):
        return f"Appareil(nom='{self.nom}', modele='{self.modele}')"