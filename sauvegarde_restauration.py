import json
from tkinter import filedialog

def sauvegarder_dossier(structures_racines):
    """Prend la liste des ZoneConfinee du manager principal."""
    donnees = [z.get_data() for z in structures_racines if hasattr(z, 'get_data')]
    
    filepath = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Fichiers JSON", "*.json")]
    )
    
    if filepath:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(donnees, f, indent=4, ensure_ascii=False)
        return True
    return False

def charger_dossier():
    filepath = filedialog.askopenfilename(filetypes=[("Fichiers JSON", "*.json")])
    if filepath:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None